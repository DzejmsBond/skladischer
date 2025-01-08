# Configuration file for the Sphinx documentation builder.

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../../'))  # Path to project.

# -- Project information -----------------------------------------------------
project = 'Skladischer'
author = 'DBond'

# -- General configuration ---------------------------------------------------
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.napoleon',
              'sphinx.ext.intersphinx']
templates_path = ['_templates']

# -- Options for HTML output -------------------------------------------------
html_permalinks_icon = '<span>#</span>'
html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']

html_theme_options = {
    "show_nav_level": 2,  # Show up to level 2 headings in the navigation sidebar.
    "navigation_depth": 4,  # Include deeper levels like functions, classes, etc.
    "collapse_navigation": False,  # Keep all sections expanded in the sidebar.
    "show_prev_next": True,  # Show "Previous" and "Next" buttons.
    "secondary_sidebar_items": ["page-toc", "sourcelink"]
}

html_sidebars = {
  "**": []
}

html_show_sourcelink = False

# -- Autogeneration ----------------------------------------------------------
autodoc_default_options = {
    "members": True,
    "undoc-members": True,  # Include members without docstrings.
    "imported-members": True,  # Include imported members.
    "show-inheritance": True,
}

