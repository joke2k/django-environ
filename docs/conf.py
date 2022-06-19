# This file is part of the django-environ.
#
# Copyright (c) 2021-2022, Serghei Iakovlev <egrep@protonmail.ch>
# Copyright (c) 2013-2021, Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE.txt file that was distributed with this source code.

#
# -- Utils ---------------------------------------------------------
#

import codecs
import os
import sys
import re

from datetime import date


PROJECT_DIR = os.path.abspath('..')
sys.path.insert(0, PROJECT_DIR)


def read_file(filepath):
    """Read content from a UTF-8 encoded text file."""
    with codecs.open(filepath, 'rb', 'utf-8') as file_handle:
        return file_handle.read()


def find_version(meta_file):
    """Extract ``__version__`` from meta_file."""
    contents = read_file(os.path.join(PROJECT_DIR, meta_file))
    meta_match = re.search(
        r"^__version__\s+=\s+['\"]([^'\"]*)['\"]",
        contents,
        re.M
    )

    if meta_match:
        return meta_match.group(1)
    raise RuntimeError(
        "Unable to find __version__ string in package meta file")


#
# -- Project information -----------------------------------------------------
#

# General information about the project.
project = "django-environ"
copyright = f'2013-{date.today().year}, Daniele Faraglia and other contributors'
author = u"Daniele Faraglia \\and Serghei Iakovlev"

#
# -- General configuration ---------------------------------------------------
#

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "notfound.extension",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = ".rst"

# Allow non-local URIs so we can have images in CHANGELOG etc.
suppress_warnings = [
    "image.nonlocal_uri",
]

# The master toctree document.
master_doc = "index"

# The version info
# The short X.Y version.
release = find_version(os.path.join("environ", "__init__.py"))
version = release.rsplit(u".", 1)[0]
# The full version, including alpha/beta/rc tags.

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build"]

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = "any"

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

#
# -- Options for autodoc ---------------------------------------------------
#

# This value selects if automatically documented members are sorted alphabetical
# (value 'alphabetical'), by member type (value 'groupwise') or by source order
# (value 'bysource'). The default is alphabetical.
#
# Note that for source order, the module must be a Python module with the
# source code available.
autodoc_member_order = 'bysource'

#
# -- Options for linkcheck ---------------------------------------------------
#

linkcheck_ignore = [
    # We run into GitHub's rate limits.
    r"https://github.com/.*/(issues|pull)/\d+",
    # Do not check links to compare tags.
    r"https://github.com/joke2k/django-environ/compare/.*",
]

#
# -- Options for nitpick -----------------------------------------------------
#

# In nitpick mode (-n), still ignore any of the following "broken" references
# to non-types.
nitpick_ignore = [
    ('py:func', 'str.rfind'),
    ('py:func', 'str.find'),
]

#
# -- Options for extlinks ----------------------------------------------------
#

extlinks = {
    "pypi": ("https://pypi.org/project/%s/", ""),
}

#
# -- Options for intersphinx -------------------------------------------------
#

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}

#
# -- Options for TODOs -------------------------------------------------------
#

todo_include_todos = True

# -- Options for HTML output -------------------------------------------------

# html_favicon = None

html_theme = "furo"
html_title = project

html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# If false, no module index is generated.
html_domain_indices = True

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_openserver = ''

# Output file base name for HTML help builder.
htmlhelp_basename = "django-environ-doc"

#
# -- Options for manual page output ------------------------------------------
#

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ("index", project, "django-environ Documentation", [author], 1)
]

#
# -- Options for Texinfo output ----------------------------------------------
#

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        "index",
        project,
        "django-environ Documentation",
        author,
        project,
        "Configure Django made easy.",
        "Miscellaneous",
    )
]
