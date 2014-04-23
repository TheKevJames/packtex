# -*- coding: utf-8 -*-
# -- General configuration ------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

master_doc = 'index'
source_suffix = '.rst'
pygments_style = 'sphinx'

exclude_patterns = ['_build']

project = u'packtex'
copyright = u'2014, @TheKevJames (auto-generated)'
show_authors = True

version = '0'
release = '0'

add_module_names = False

# -- Options for HTML output ----------------------------------------------
html_theme = 'agogo'

htmlhelp_basename = 'Packtex Docs'
