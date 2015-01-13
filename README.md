=================
Easy Lausanne
=================

This is an extremely stripped-down version of the connectome mapper,
all it does is create the Lausanne2008 parcellations from an 
existing FreeSurfer directory and align them to a target volume (BOLD or B0)
using bbregister. 

Prerequisites:
---------------
 * FreeSurfer
 * FSL
 * numpy/scipy/nibabel

*All the hard work was done by the LTS5 folks and they 
should be credited if you use these atlases in your work.*

> A. Daducci, S. Gerhard, A. Griffa, A. Lemkaddem, L. Cammoun, X. Gigandet, 
> R. Meuli, P. Hagmann and J.-P. Thiran The Connectome Mapper: An Open-Source 
> Processing Pipeline to Map Connectomes with MRI. Plos One 7(12):e48121 (2012)

Installation
--------------

```bash
$ git clone https://github.com/mattcieslak/easy_lausanne.git
$ cd easy_lausanne
$ python setup.py install
```
This installs the ``easy_lausanne`` executable on your path. 

Example use
--------------

Assuming FreeSurfer is installed, you've run the Freesurfer setup script,
and recon-all has completely finished for "SUBJECT",
you use easy_lausanne to create the Lausanne2008 atlases aligned to 
VOLUME.nii.gz for "SUBJECT"

```bash
$ easy_lausanne \
     --subject_id SUBJECT \
     --target_volume /path/to/VOLUME.nii.gz \
     --target_type diffusion OR bold \
     --output_dir /where/you/want/results
```

Proof of usability
===================

I ran a DSI dataset through the connectomemapper and resampled the Lausanne2008
labels into native B0 space.  easy_lausanne was then used on a clean copy of
this data to generate the atlases directly in B0 space.  Here are plots of 
the overlap in voxels and the relative sizes of each region for the cmp-generated
and easy_lausanne-generated atlases.

Voxelwise labeling analysis (blue)
---------------------------------
Here each non-zero voxel was compared between the two atlases. The label value
in each voxel is plotted.

Region size comparison (red)
-------------------------------
The proportion of nonzero voxels for each region label is plotted for both versions 
of the Lausanne2008 atlas.

Plots
--------

![scale33 Voxelwise](doc/scale33.voxelwise_corr.png)

![scale33 percent](doc/scale33.region_percentage.png)

![scale60 Voxelwise](doc/scale60.voxelwise_corr.png)

![scale60 percent](doc/scale60.region_percentage.png)

![scale125Voxelwise](doc/scale125.voxelwise_corr.png)

![scale125 percent](doc/scale125.region_percentage.png)

![scale250Voxelwise](doc/scale250.voxelwise_corr.png)

![scale250 percent](doc/scale250.region_percentage.png)

