# Copyright 2017-2023 Posit Software, PBC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ---------------------------------------------------------------------------
# Why this file still exists
# ---------------------------------------------------------------------------
# pyproject.toml drives the build, but setuptools still needs a place to
# attach the custom build_py command (BUILD_GUILD_VIEW npm step) and to
# read dynamic metadata from guildai.dist-info/METADATA.
#
# Once setuptools adds first-class support for arbitrary build hooks in
# pyproject.toml you can delete this file entirely.
# ---------------------------------------------------------------------------

import email.parser
import os
import platform
import subprocess

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

GUILD_DIST_INFO = "guildai.dist-info"
GUILD_METADATA_FILE = os.path.join(GUILD_DIST_INFO, "METADATA")
GUILD_ENTRY_POINTS_FILE = os.path.join(GUILD_DIST_INFO, "entry_points.txt")

NPM_CMD = "npm.cmd" if platform.system() == "Windows" else "npm"


# ---------------------------------------------------------------------------
# Metadata helpers — pure stdlib, no pkg_resources, no import of guild
# ---------------------------------------------------------------------------

def _read_metadata():
    """Parse guildai.dist-info/METADATA using stdlib email parser."""
    with open(GUILD_METADATA_FILE, encoding="utf-8") as f:
        return email.parser.HeaderParser().parse(f)


def _read_entry_points():
    """
    Parse guildai.dist-info/entry_points.txt into the dict format that
    setuptools.setup(entry_points=...) expects:

        {"console_scripts": ["guild = guild.main_bootstrap:main"], ...}
    """
    if not os.path.isfile(GUILD_ENTRY_POINTS_FILE):
        return {}

    entry_points = {}
    current_group = None
    with open(GUILD_ENTRY_POINTS_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[") and line.endswith("]"):
                current_group = line[1:-1]
                entry_points[current_group] = []
            elif current_group is not None:
                entry_points[current_group].append(line)
    return entry_points


def _read_version():
    """
    Read __version__ from guild/__init__.py without importing the guild
    package (which may have C extensions or dependencies that aren't
    available yet at build time).
    """
    version_file = os.path.join("guild", "__init__.py")
    with open(version_file, encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                # Handles:  __version__ = "0.9.1"  or  __version__ = '0.9.1'
                return line.split("=", 1)[1].strip().strip("\"'")
    raise RuntimeError("__version__ not found in {}".format(version_file))


# ---------------------------------------------------------------------------
# Custom build command
# ---------------------------------------------------------------------------

class Build(build_py):
    """Extension of default build with optional npm pre-processing.

    Set the environment variable BUILD_GUILD_VIEW=1 to trigger an npm
    build of the Guild AI web view before the Python build runs.

    See MANIFEST.in for the complete list of data files included in the
    Guild distribution.
    """

    def run(self):
        if os.getenv("BUILD_GUILD_VIEW") == "1":
            _check_npm()
            _build_view_dist()
        build_py.run(self)


def _check_npm():
    try:
        subprocess.check_output([NPM_CMD, "--version"])
    except OSError as e:
        raise SystemExit("error checking npm: {}".format(e)) from e


def _build_view_dist():
    subprocess.check_call([NPM_CMD, "install"], cwd="./guild/view")
    subprocess.check_call([NPM_CMD, "run", "build"], cwd="./guild/view")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

PKG_INFO = _read_metadata()
ENTRY_POINTS = _read_entry_points()
VERSION = _read_version()


def _get_all(msg, key):
    """Return all values for a multi-value header (e.g. Classifier)."""
    return msg.get_all(key) or []


setup(
    # Hook in our custom build step
    cmdclass={"build_py": Build},

    # Core identity — read from dist-info so there is a single source of truth
    name="guildai",
    version=VERSION,
    description=PKG_INFO.get("Summary"),
    long_description=PKG_INFO.get_payload(),
    long_description_content_type="text/markdown",

    # Contact / project URLs
    url=PKG_INFO.get("Home-page"),
    maintainer=PKG_INFO.get("Author"),
    maintainer_email=PKG_INFO.get("Author-email"),

    # Packaging metadata
    license=PKG_INFO.get("License"),
    keywords=PKG_INFO.get("Keywords"),
    classifiers=_get_all(PKG_INFO, "Classifier"),
    install_requires=_get_all(PKG_INFO, "Requires-Dist"),
    python_requires=PKG_INFO.get("Requires-Python") or ">=3.7",

    # Entry points read from dist-info
    entry_points=ENTRY_POINTS,

    # Package discovery
    packages=find_packages(exclude=["guild.tests", "guild.tests.*"]),
    include_package_data=True,

    # Scripts
    scripts=["./guild/scripts/guild-env"],

    zip_safe=False,
)
