# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os, sys, glob

project = 'guild'
copyright = '2025, re:guild Team'
author = 're:guild Team'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    # other extensions
]

# Optional: If you want to use specific MyST features, you can configure them here too.
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


# Specify MYST_DEBUG for troubleshooting
# os.environ["MYST_DEBUG"] = "1"

# Get a list of all Markdown files up to 5 directories deep
markdown_files = glob.glob('pages/**/*.md', recursive=True)

# Example of generating a master index file
with open('pages.rst', 'w') as index_file:
    index_file.write('.. toctree::\n')
    index_file.write('   :maxdepth: 2\n\n')
    for md_file in markdown_files:
        # Add the path to the index
        index_file.write(f'   {md_file}\n')
