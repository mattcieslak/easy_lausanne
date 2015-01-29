# Copyright (C) 2009-2011, Ecole Polytechnique Federale de Lausanne (EPFL) and
# Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland
# All rights reserved.
#
#  This software is distributed under the open-source license Modified BSD.

import os, os.path as op
from glob import glob
from time import time
from os import environ
import subprocess
import sys
import shutil 

from command import runCmd, getLog
log = getLog("test.log")

SUBJECTS_DIR=os.getenv("SUBJECTS_DIR")

    
def bb_regT12b0(subject_id, target_volume, output_directory, target_type):
    FS_DIR = op.join(os.environ["SUBJECTS_DIR"],subject_id)
    log.info("T1 -> b0: BBREGISTER linear registration")
    log.info("========================================")

    # Linear register "T1" onto "b0_resampled"
    log.info("Started FreeSurfer bbregister to find 'T1 --> b0' linear transformation")

    additional_bbreg_args = '--init-fsl '
    if target_type == "diffusion":
        additional_bbreg_args += '--dti'
    elif target_type == "bold":
        additional_bbreg_args += '--bold'
    elif target_type == "anisotropy":
        additional_bbreg_args += '--t1'
        
        

    # Necessary file paths
    xform_dat = op.join(output_directory,"b0-TO-orig.dat")
    xform_mat = op.join(output_directory, 'b0-TO-orig.mat')


    bbregister_cmd = 'bbregister --s %s --mov %s --reg %s --fslmat %s %s' % (
        subject_id,
        target_volume,
        xform_dat,
        xform_mat,
        additional_bbreg_args)
    runCmd(bbregister_cmd, log)

    convert_xfm_command = 'convert_xfm -inverse %s -omat %s' % (
        op.join(output_directory, 'b0-TO-orig.mat'),
        op.join(output_directory, 'orig-TO-b0.mat'),
    )
    runCmd(convert_xfm_command, log)

    tkregister2_command = 'tkregister2 --regheader --mov %s --targ %s --regheader --reg %s --fslregout %s --noedit' % (
        op.join(FS_DIR, 'mri', 'rawavg.mgz'),
        op.join(FS_DIR, 'mri', 'orig.mgz'),
        op.join(output_directory, 'T1-TO-orig.dat'),
        op.join(output_directory, 'T1-TO-orig.mat'),
    )
    runCmd(tkregister2_command, log)

    convert_xfm_command = 'convert_xfm -omat %s -concat %s %s' % (
        op.join(output_directory, 'T1-TO-b0.mat'),
        op.join(output_directory, 'orig-TO-b0.mat'),
        op.join(output_directory, 'T1-TO-orig.mat'),
    )
    runCmd(convert_xfm_command, log)

    if not op.exists(op.join(output_directory, 'T1-TO-b0.mat')):
        msg = "An error occurred. Linear transformation file %s not generated." % op.join(
            output_directory, 'T1-TO-b0.mat')
        log.error(msg)
        raise Exception(msg)

    log.info("[ DONE ]")