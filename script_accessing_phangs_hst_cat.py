r"""
script with an example how to access PHANGS-HST catalogs.
This is a simple script version of the jupyter notebook example
"""

import numpy as np
import matplotlib.pyplot as plt
import helper_func
import os
from urllib3 import PoolManager

import tarfile


from astropy.visualization import SqrtStretch

from astropy.visualization import SinhStretch
#
# dst_path = 'path/to/my/destination'


galaxy_name = 'ngc1566'

# download the HST catalog
cluster_catalog_url = 'https://archive.stsci.edu/hlsps/phangs-cat/dr4/bundles/hlsp_phangs-cat_hst_acs-uvis_%s_multi_v1_cats.tar.gz'
url = 'https://archive.stsci.edu/hlsps/phangs-cat/dr4/bundles/hlsp_phangs-cat_hst_acs-uvis_ngc1566_multi_v1_cats.tar.gz'
catalog_zip_name = 'hlsp_phangs-cat_hst_acs-uvis_%s_multi_v1_cats.tar.gz' % galaxy_name


# download file
http = PoolManager()
r = http.request('GET', url, preload_content=False)


with open(catalog_zip_name, 'wb') as out:
    while True:
        data = r.read()
        if not data:
            break
        out.write(data)



pwd = os.getcwd()

src_path = pwd + '/' + catalog_zip_name

print(src_path)
print(pwd)

if src_path.endswith('tar.gz'):
    tar = tarfile.open(src_path, 'r:gz')
    tar.extractall(pwd)
    tar.close()
