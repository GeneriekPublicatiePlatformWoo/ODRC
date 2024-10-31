# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
import os
import sys

import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "woo_publications.conf.ci")
sys.path.insert(0, os.path.abspath("../src"))

import woo_publications  # noqa isort:skip

from woo_publications.setup import setup_env  # noqa isort:skip

setup_env()
django.setup()

# -- Project information -----------------------------------------------------

project = "WOO Publications"
copyright = "Maykin B.V. 2024"
author = woo_publications.__author__

# The full version, including alpha/beta/rc tags
release = woo_publications.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.graphviz",
    "sphinx.ext.todo",
    # "sphinx_tabs.tabs",
    # "recommonmark",
    # "sphinx_markdown_tables",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# source_suffix = [".rst", ".md"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_logo = "logo.png"
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = [
    "theme_overrides.css",  # override wide tables with word wrap
]

todo_include_todos = True

linkcheck_ignore = [
    r"https?://.*\.example\.com*",
    r"https?://.*\.gemeente\.nl*",
    r"http://localhost:\d+/",
    r"https://.*sentry.*",
    r"https://www\.miniwebtool\.com/django-secret-key-generator",
]


def generate_schema_diagram(app):
    dot_file = os.path.join(app.srcdir, "developers/_assets/db_schema.dot")

    # generate graphviz dot file
    call_command(
        "graph_models",
        group_models=True,
        all_applications=True,
        output=dot_file,
    )


def setup(app):
    app.connect("builder-inited", generate_schema_diagram)
