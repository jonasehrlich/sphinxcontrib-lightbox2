# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from sphinxcontrib.lightbox2 import __version__

project = "sphinxcontrib-lightbox2"
copyright = "2024, Jonas Ehrlich"
author = "Jonas Ehrlich"
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "sphinx_design", "sphinxcontrib.lightbox2", "sphinxcontrib.plantuml"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]


# -- Options for myst-parser -------------------------------------------------
# https://myst-parser.readthedocs.io/en/latest/configuration.html

myst_enable_extensions = ["colon_fence"]

# -- Options for sphinxcontrib.lightbox2 -------------------------------------

# The time it takes for the Lightbox container and overlay to fade in and out, in milliseconds
lightbox2_fade_duration = 100
lightbox2_image_fade_duration = 100
