# -- SpatialAIFlow documentation build configuration --
# Full Sphinx configuration reference: https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add source directory to path for autodoc
sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -----------------------------------------------------
project = "SpatialAIFlow"
copyright = "2025, SpatialAIFlow Contributors"
author = "SpatialAIFlow Contributors"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",          # NumPy/Google-style docstrings
    "sphinx.ext.intersphinx",       # Cross-reference external docs
    "sphinx.ext.viewcode",          # Add source links to API docs
    "sphinx_autodoc_typehints",     # Type hints in API docs
    "myst_parser",                  # Markdown support
    "nbsphinx",                     # Notebook rendering
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- Intersphinx mapping -----------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "anndata": ("https://anndata.readthedocs.io/en/stable/", None),
    "scanpy": ("https://scanpy.readthedocs.io/en/stable/", None),
    "squidpy": ("https://squidpy.readthedocs.io/en/stable/", None),
}

# -- Napoleon settings -------------------------------------------------------
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True

# -- nbsphinx settings -------------------------------------------------------
nbsphinx_execute = "never"  # Do not re-execute notebooks during build
