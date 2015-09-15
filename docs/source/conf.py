# -*- coding: utf-8 -*-

import sys
import os
from datetime import date


autodoc_mock_imports = [
    'numpy',
    'scipy', 'scipy.misc', 'scipy.stats', 'scipy.stats._continuous_distns', 'scipy.special',
    'floodestimation'
]
print('working dir: ' + os.getcwd())
os.chdir('../..')
print('working dir: ' + os.getcwd())
print('sys argv[0]: ' + sys.argv[0])

# -- General configuration ------------------------------------------------

needs_sphinx = '1.3'
extensions = [
#    'sphinx.ext.autodoc',
#    'sphinx.ext.doctest',
]
source_suffix = '.rst'
master_doc = 'index'
project = 'OH Auto Statistical'
copyright = '2014‒{}, Open Hydrology contributors'.format(date.today().year)

# import imp
# fp, pathname, description = imp.find_module('versioneer')
# print(pathname)
# versioneer = imp.load_module('versioneer', fp, pathname, description)
# del imp
import versioneer
release = versioneer.get_version()
version = '.'.join(release.split('.')[:2])
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_static_path = ['_static']
html_last_updated_fmt = '%d/%m/%Y'
html_show_sphinx = False
htmlhelp_basename = 'doc'
