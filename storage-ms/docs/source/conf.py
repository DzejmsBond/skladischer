# Configuration file for the Sphinx documentation builder.

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../../'))  # Path to project.

# -- Project information -----------------------------------------------------
project = 'Skladischer'
author = 'DBond'
release = '12.01.2025'

# -- General configuration ---------------------------------------------------
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.napoleon',
              'sphinx.ext.intersphinx']
templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_permalinks_icon = '<span>#</span>'
html_theme = 'sphinxawesome_theme'
html_static_path = ['_static']

# -- Autogeneration ----------------------------------------------------------
autodoc_default_options = {
    "members": True,
    "undoc-members": True,  # Include members without docstrings.
    "imported-members": True,  # Include imported members.
    "show-inheritance": True,
}
