# Copyright (C) 2009-2011, Ecole Polytechnique Federale de Lausanne (EPFL) and
# Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland
# All rights reserved.
#
#  This software is distributed under the open-source license Modified BSD.

import os, os.path as op
import sys
from time import time
from glob import glob
import subprocess
import shutil
from command import *
from maskcreation import lausanne_spec


def apply_lin_registration(subject_id, output_dir,target_volume,include500):

    log.info("Apply the linear REGISTRATION TRANSFORM to the output of FreeSurfer (WM+GM)")
    log.info("===========================================================================")
    log.info("(i.e. fsmask_1mm.*, scale33/ROI_HR_th.* etc)")

    subjects_dir = os.getenv("SUBJECTS_DIR")
    fs_dir = op.join(subjects_dir, subject_id)
    fs_label_dir = op.join(fs_dir, 'label')
    tracto_masks_path = fs_label_dir
    tracto_masks_path_out = output_dir
    
    if not op.exists(tracto_masks_path):
        msg = "Path does not exists but it should after the mask creation module: %s" % tracto_masks_path
        log.error(msg)
        raise Exception(msg)  

    orig_mat = op.join(output_dir, 'orig-TO-b0.mat')
    out_mat = op.join(tracto_masks_path_out, 'tmp_premat.mat')
    try:
        shutil.copy(orig_mat, out_mat)
    finally:
        log.info("Copied file %s to %s." % (orig_mat, out_mat))

    log.info("Apply linear registration...")

    # warp fsmask_1mm and parcellations
    warp_files = []
    scales = ["scale33", "scale60", "scale125", "scale250"]
    if include500: scales +=  [ "scale500"]
    thicks = ["ROI", "ROIv"]
    for scale in scales:
        for thick in thicks:
            warp_files.append(thick + "_" + scale + '.nii.gz')
    
    for infile in warp_files:
        log.info("Warp file: %s" % infile)
        flirt_cmd = 'flirt -applyxfm -init %s -in %s -ref %s -out %s -interp nearestneighbour' % (
                    out_mat,
                    op.join(tracto_masks_path, infile),
                    target_volume,
                    op.join(tracto_masks_path_out, infile)
                    )
        
        runCmd( flirt_cmd, log )
        
        if not op.exists(op.join(tracto_masks_path_out, infile)):
            msg = "An error occurred. File %s not generated." % op.join(tracto_masks_path_out, infile)
            log.error(msg)
            raise Exception(msg)
        
        log.info("[ DONE ]")              
        
    log.info("Chain of registrations applied. [ DONE ]")
    log.info("[ Saved in %s ]" % tracto_masks_path_out)
    