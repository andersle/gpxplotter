# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('./extensions'))
from datetime import date
import warnings
import gpxplotter
from sphinx_gallery.sorting import FileNameSortKey


# Disable matplotlib warnings for generation of gallery:
warnings.filterwarnings(
    'ignore',
    category=UserWarning,
    message='Matplotlib is currently using agg, which is a'
            ' non-GUI backend, so cannot show the figure.'
)

# -- Project information -----------------------------------------------------
master_doc = 'index'
project = 'gpxplotter'

year = date.today().year
if year > 2020:
    copyright = '2020-{}, Anders Lervik'.format(year)
else:
    copyright = '2020, Anders Lervik'
author = 'Anders Lervik'

rst_prolog = '.. |gpxplotter| replace:: gpxplotter'
# The full version, including alpha/beta/rc tags
version = gpxplotter.version.SHORT_VERSION
release = gpxplotter.version.VERSION

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx_gallery.gen_gallery',
    'thumbnail_updater',
]

# Napoleon settings
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_ivar = False
napoleon_use_keyword = False
napoleon_use_param = False
napoleon_use_rtype = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

intersphinx_mapping = {
    'python': (
        'https://docs.python.org/{.major}'.format(sys.version_info), None
    ),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference', None),
    'matplotlib': ('https://matplotlib.org/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable', None),
}

# Settings for gallery:
sphinx_gallery_conf = {
    'examples_dirs': ['gallery/maps', 'gallery/plots'],
    'gallery_dirs': ['auto_examples_maps', 'auto_examples_plots'],
    'download_all_examples': False,
    'within_subsection_order': FileNameSortKey,
}

# Settings for thumbnail-updater:
thumbnail_updater_conf = {
    'thumbnail_dir': 'gallery_thumbs'
}
