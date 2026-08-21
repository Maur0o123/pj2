# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = 'Geoadmin'
copyright = '2025, Isamax'
author = 'Isamax'
release = 'Versión Web'

# -- General configuration ---------------------------------------------------

extensions = ["sphinx.ext.todo","sphinx.ext.viewcode","sphinx.ext.autodoc","sphinx.ext.napoleon",
    "sphinx.ext.intersphinx","sphinx_autodoc_typehints",'sphinx_copybutton',]

todo_include_todos = True
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'es'

gettext_compact = False
locale_dirs = ['locale/']  # Carpeta donde estarán los archivos .po

# -- Options for HTML output -------------------------------------------------
html_show_sourcelink = False
html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
html_logo = "_static/logobg.png"
html_theme_options = {
    "repository_url": "https://github.com/Cconelli/Geoadmin",  # URL de tu repositorio
    "use_repository_button": True,
    
}
