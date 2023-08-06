# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dinosar',
 'dinosar.archive',
 'dinosar.archive.asf',
 'dinosar.archive.plot',
 'dinosar.cli',
 'dinosar.isce']

package_data = \
{'': ['*']}

install_requires = \
['geopandas>=0.8,<0.9',
 'lxml>=4.4,<5.0',
 'matplotlib>=3.1,<4.0',
 'pandas>=1.0,<2.0',
 'pyyaml>=5.2,<6.0',
 'requests>=2.22,<3.0',
 'shapely>=1.6,<2.0']

extras_require = \
{'docs': ['sphinx>=2.3,<3.0',
          'sphinx_rtd_theme>=0.4,<0.5',
          'sphinxcontrib-apidoc>=0.3,<0.4'],
 'vis': ['cartopy>=0.18,<0.19']}

entry_points = \
{'console_scripts': ['get_inventory_asf = dinosar.cli.get_inventory_asf:main',
                     'plot_inventory_asf = dinosar.cli.plot_inventory_asf:main',
                     'prep_topsApp_local = '
                     'dinosar.cli.prep_topsApp_local:main']}

setup_kwargs = {
    'name': 'dinosar',
    'version': '0.1.4',
    'description': 'SAR processing on the Cloud',
    'long_description': "![Action Status](https://github.com/scottyhq/dinosar/workflows/Package/badge.svg)\n[![Documentation Status](https://readthedocs.org/projects/dinosar/badge/?version=latest)](https://dinosar.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/scottyhq/dinosar/branch/master/graph/badge.svg)](https://codecov.io/gh/scottyhq/dinosar)\n\n# dinoSAR\n\ndinoSAR facilitates processesing InSAR data on the Cloud.\n\ndinoSAR is software that enables on-demand processing of single interferograms and sets of interferograms for a given area of interest on the Cloud. Processing is done with [ISCE2 Software](https://github.com/isce-framework/isce2) that is [Dockerized](https://docs.docker.com) and run on [AWS Batch](https://aws.amazon.com/batch). So for now we have *dinoSARaws*.\n\nCurrently, dinoSAR works with [Sentinel-1](http://www.esa.int/Our_Activities/Observing_the_Earth/Copernicus/Sentinel-1) data, which is provided by the European Space Agency (ESA). dinoSAR utilities for searching for data [via the Alaska Satellite Facility (ASF)](https://www.asf.alaska.edu/) and setting up processing to either run locally or on the Cloud. Why run on the Cloud? SAR imagery takes up a lot of disk space and because data is being stored on AWS, running on the Cloud circumvents the need to download data. Furthermore, we can take advantage of scalable parallel processing!\n\ndinoSAR enables Cloud-native processing of output imagery by creating [Cloud-Optimized Geotiffs](http://www.cogeo.org) with accompanying [STAC metadata](https://github.com/radiantearth/stac-spec). You can find examples of postprocessing workflows on the [Pangeo website](http://pangeo.io).\n\n\n## acknowledgments\n\nThis project got started with funding from the University of Washington [eScience Institute](http://escience.washington.edu) and the [Washington Research Foundation](http://www.wrfseattle.org). Additionally, financial support has come from Amazon 'Earth on AWS' [Grants program](https://aws.amazon.com/earth/research-credits/) and the [NASA ACCESS program](https://earthdata.nasa.gov/community/community-data-system-programs/access-projects/community-tools-for-analysis-of-nasa-earth-observation-system-data-in-the-cloud).\n",
    'author': 'Scott Henderson',
    'author_email': 'scotty@uw.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scottyhq/dinosar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
