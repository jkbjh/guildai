# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
import glob
from docutils import nodes
from sphinx.util.docutils import SphinxDirective, SphinxRole
import re
from pathlib import Path

sys.path.insert(0, os.path.abspath("../source"))
sys.path.append(str(Path("_ext").resolve()))

import command_help

project = "guild"
copyright = "2025, re:guild Team; 2017-2023 Posit Software, PBC"
author = "re:guild Team"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Custom Directive to handle {em-code} with <em> tags
# class CodeDirectiveWithEm(SphinxDirective):


class CodeDirectiveWithEm(SphinxDirective):
    has_content = True

    def run(self):
        # Combine the content into one string
        content = "\n".join(self.content)

        # Create the literal block node
        literal_block = nodes.literal_block(classes=["highlighted-code"])

        # Position to keep track of parsing
        position = 0

        # Regex pattern to find all <em>...</em> matches
        pattern = re.compile(r'<em>(.*?)</em>')

        # Iterate over all matches
        for match in pattern.finditer(content):
            # Add text before the <em> tag
            if match.start() > position:
                text_part = content[position:match.start()]
                if text_part:
                    literal_block += nodes.Text(text_part)

            # Add emphasized text within <em></em>
            bold_text = match.group(1)
            emphasis_node = nodes.inline('', bold_text, classes=["emphasis-code"])
            literal_block += emphasis_node

            # Update the position marker
            position = match.end()

        # Add any remaining text after the last <em> tag
        if position < len(content):
            remaining_text = content[position:]
            if remaining_text:
                literal_block += nodes.Text(remaining_text)

        return [literal_block]


class EmCodeRole(SphinxRole):
    @staticmethod
    def parse_highlighted_code(text):
        """
        Replace <em>...</em> with bold formatting inside a single inline node.
        Returns a list of text elements, ensuring seamless integration.
        """
        parts = []
        last_end = 0

        for match in re.finditer(r"<em>(.*?)</em>", text):
            # Literal text before <em>
            if match.start() > last_end:
                raw = text[last_end:match.start()]
                parts.append(nodes.Text(raw))

            # Bold (strong) part: Add the text, wrapped in strong
            bold_text = match.group(1)
            strong_node = nodes.strong('', bold_text)
            parts.append(strong_node)

            last_end = match.end()

        # Remaining literal text after last <em>
        if last_end < len(text):
            raw = text[last_end:]
            parts.append(nodes.Text(raw))

        return parts

    def run(self):
        """
        Process the role content and return a node with consistent monospace and 
        bold formatting across the inline element.
        """
        try:
            children = self.parse_highlighted_code(self.text)
            # Wrap all parts in a single literal node to ensure consistent style
            node = nodes.literal("", "", *children, classes=["mycode"])
            return [node], []
        except Exception as e:
            msg = self.inliner.reporter.error(
                f"MyCode role error: {e}", line=self.lineno
            )
            problematic = self.inliner.problematic(self.rawtext, self.rawtext, msg)
            return [problematic], [msg]


# Register the custom directive for {em-code}
def setup(app):
    app.add_directive("em-code", CodeDirectiveWithEm)
    app.add_directive("emcode", CodeDirectiveWithEm)
    app.add_role("emcode", EmCodeRole())
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


extensions = [
    "myst_parser",
    # other extensions
    "sphinx_rtd_theme",
    #'sphinx.ext.autosectionlabel',
    "sphinx_sitemap",
    "todo",  # local
]

html_baseurl = """import os; print("file://" + os.path.normpath(os.getcwd() + "/../build/html/"))"""
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
    "attrs_inline",
]
myst_heading_anchors = 5
# set external link schemes, so that absolute links work.
myst_url_schemes = {"http": None, "https": None, "mailto": None, "ftp": None}
templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"  #'alabaster'
html_static_path = ["_static"]

# Specify MYST_DEBUG for troubleshooting
# os.environ["MYST_DEBUG"] = "1"

# Generate Help pages from the command line interface command descriptions
if False:
    command_help.generate_command_help()  # need to add a cache for this.

# Get a list of all Markdown files up to 5 directories deep
markdown_files = list(sorted(glob.glob("pages/**/*.md", recursive=True)))

# # Example of generating a master index file
# with open('sitemap.rst', 'w') as index_file:
#     index_file.write('.. toctree::\n')
#     index_file.write('   :maxdepth: 5\n\n')
#     for md_file in markdown_files:
#         # Add the path to the index
#         index_file.write(f'   /{md_file}\n')
