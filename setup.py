#!/usr/bin/env python
import os
import sys
from setuptools import setup,find_packages

package_data = {'':
                ['data/colortable_and_gcs/*.txt',
                 'data/colortable_and_gcs/my_atlas_gcs/*.gcs',
                 'data/parcellation/lausanne2008/*.*',
                 'data/parcellation/lausanne2008/resolution83/*.*',
                 'data/parcellation/lausanne2008/resolution150/*.*',
                 'data/parcellation/lausanne2008/resolution258/*.*',
                 'data/parcellation/lausanne2008/resolution500/*.*',
                 'data/parcellation/lausanne2008/resolution1015/*.*',
                 
                 ]}
    
setup(name='Easy Lausanne',
      version="0.5",
      description="A minimal set of code to produce the Lausanne atlases",
      author='Matt Cieslak',
      author_email='matthew.cieslak at psych.ucsb.edu',
      url='',
      scripts = ['scripts/easy_lausanne', 'scripts/atlas_dilate'],
      packages = find_packages(),
      package_data = package_data,
      include_package_data=True
     )
