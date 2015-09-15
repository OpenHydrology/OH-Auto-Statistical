# -*- coding: utf-8 -*-

import sys
import os
from datetime import date
import autostatistical


autodoc_mock_imports = [
    'numpy',
    'scipy', 'scipy.misc', 'scipy.stats', 'scipy.stats._continuous_distns', 'scipy.special',
    'floodestimation'
]
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../autostatistical'))

# -- General configuration ------------------------------------------------

needs_sphinx = '1.3'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
]
source_suffix = '.rst'
master_doc = 'index'
project = 'OH Auto Statistical'
copyright = '2014‒{}, Open Hydrology contributors'.format(date.today().year)
release = autostatistical.__version__
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
