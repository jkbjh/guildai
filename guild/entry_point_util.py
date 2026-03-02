# Copyright 2017-2023 Posit Software, PBC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import sys
import importlib
import json
import urllib
import importlib.metadata
from pathlib import Path
log = logging.getLogger("guild")


class _Map:
    _module_to_pkg = None
    _distname_to_dists = None

    @classmethod
    def refresh(cls):
        cls._module_to_pkg = None
        cls._distname_to_dists = None

    @classmethod
    def _ensure_module_to_pkg(cls):
        if cls._module_to_pkg is None:
            cls._module_to_pkg = importlib.metadata.packages_distributions()

    @classmethod
    def _ensure_distname_to_dists(cls):
        if cls._distname_to_dists is not None:
            return
        cls._distname_to_dists = {}
        for dist in importlib.metadata.distributions():
            cls._distname_to_dists[dist.name] = cls._distname_to_dists.get(
                dist.name, set()
            )
            cls._distname_to_dists[dist.name].add(dist)

    @classmethod
    def modules_to_packagelist(cls, modules):
        cls._ensure_module_to_pkg()
        for module in modules:
            if module in cls._module_to_pkg:
                yield (module, cls._module_to_pkg[module])

    @classmethod
    def distname_to_distributions(cls, distname):
        cls._ensure_distname_to_dists()
        return cls._distname_to_dists[distname]


class _InstalledDist:
    """Wraps an importlib.metadata Distribution to expose get_entry_map(),
    matching the interface that WorkingSet.iter_entry_points relies on.
    """

    def __init__(self, dist):
        self._dist = dist

    @property
    def location(self):
        return str(self._dist.locate_file("."))

    @property
    def project_name(self):
        return self._dist.metadata["Name"]

    @property
    def version(self):
        return self._dist.metadata["Version"]

    def get_metadata_lines(self, name):
        """Replaces pkg_resources.Distribution.get_metadata_lines.

        Reads a metadata file (e.g. 'RECORD') and yields its non-empty,
        non-comment lines, matching the pkg_resources interface.
        """
        text = self._dist.read_text(name)
        if text is None:
            raise IOError(f"No {name} metadata found for {self.project_name}")
        for line in text.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                yield line

    def get_entry_map(self, group=None):
        eps = self._dist.entry_points
        if group is not None:
            eps = [ep for ep in eps if ep.group == group]
        result = {}
        for ep in eps:
            result[ep.name] = _InstalledEntryPoint(ep)
        if group is not None:
            return result
        # group=None: return {group: {name: ep, ...}, ...}
        by_group = {}
        for ep in self._dist.entry_points:
            by_group.setdefault(ep.group, {})[ep.name] = _InstalledEntryPoint(ep)
        return by_group


class _InstalledEntryPoint:
    """Wraps importlib.metadata.EntryPoint to match the pkg_resources
    EntryPoint interface: .name, .dist, resolve().
    """

    def __init__(self, ep):
        self._ep = ep

    @property
    def name(self):
        return self._ep.name

    @property
    def dist(self):
        raw = getattr(self._ep, "dist", None)
        return _InstalledDist(raw) if raw is not None else None

    def resolve(self):
        return self._ep.load()

    def __str__(self):
        return str(self._ep)


def _get_importer(path_item):
    """Replaces pkg_resources.get_importer: invoke sys.path_hooks and cache."""
    try:
        return sys.path_importer_cache[path_item]
    except KeyError:
        for path_hook in sys.path_hooks:
            try:
                importer = path_hook(path_item)
                sys.path_importer_cache.setdefault(path_item, importer)
                return importer
            except ImportError:
                pass
        sys.path_importer_cache[path_item] = None
        return None




def _find_distributions_for_path(path_item):
    """Yield distributions for a single path entry.

    For path entries handled by a custom importer (e.g. ModelImporter),
    yields the synthetic distribution directly from importer.dist.
    For ordinary directories, yields _InstalledDist wrappers from
    importlib.metadata.
    """
    pl_path_item = Path(path_item)
    importer = _get_importer(path_item)
    # Custom importer with a synthetic dist (e.g. GuildfileDistribution)
    dist = getattr(importer, "dist", None)
    if dist is not None:
        yield dist
        return
    # Ordinary directory: find installed dists whose location matches
    location_match = False
    for dist in importlib.metadata.distributions():
        if str(dist.locate_file(".")) == path_item:  # this does not work.
            yield _InstalledDist(dist)
            location_match = True
        else:
            try:
                direct_url_json = dist.read_text("direct_url.json") or ""
                url = json.loads(direct_url_json)["url"]
                path = urllib.parse.urlparse(url).path
                if path == path_item:
                    yield _InstalledDist(dist)
                    location_match = True
            except (AttributeError, json.JSONDecodeError, KeyError):
                pass

    # if all fails, it might be a distribution not in the search path:
    # (this holds for PackageModels)
    if not location_match and path_item not in sys.path:
        context = importlib.metadata.DistributionFinder.Context(path=[pl_path_item])
        for dist in importlib.metadata.MetadataPathFinder.find_distributions(
            context=context
        ):
            if dist.locate_file(".") == pl_path_item:
                yield _InstalledDist(dist)


class WorkingSet:
    """Replacement for pkg_resources.WorkingSet.

    Maintains a list of path entries and a corresponding set of
    distributions, exactly mirroring the pkg_resources structure.
    Distributions are discovered eagerly on construction, both from
    custom path-hook importers (for local guildfiles) and from
    importlib.metadata (for installed packages).
    """

    def __init__(self, entries=None):
        self.entries = []
        self._dists = []
        self._dist_keys = set()
        if entries is None:
            entries = sys.path
        for entry in entries:
            self.add_entry(entry)

    def add_entry(self, entry):
        self.entries.append(entry)
        for dist in _find_distributions_for_path(entry):
            key = getattr(dist, "project_name", None) or id(dist)
            if key not in self._dist_keys:
                self._dist_keys.add(key)
                self._dists.append(dist)

    def iter_entry_points(self, group, name=None):
        """Yield entry points from group across all distributions.

        Mirrors pkg_resources.WorkingSet.iter_entry_points exactly:
        calls dist.get_entry_map(group).values() on each distribution.
        """
        for dist in self._dists:
            for ep in dist.get_entry_map(group).values():
                if name is None or name == ep.name:
                    yield ep


# Global working set singleton, equivalent to pkg_resources.working_set
working_set = WorkingSet()


class Resource:
    def __init__(self, ep):
        self._ep = ep
        self._inst = None

    def inst(self):
        if self._inst is None:
            self._inst = self._ep.resolve()(self._ep)
        return self._inst

    def __str__(self):
        return f"'{self._ep}' in {self._ep.dist}"


class EntryPointResources:
    def __init__(self, group, desc="resource"):
        self.group = group
        self.desc = desc
        self.__working_set = None
        self.__resources = None

    def __str__(self):
        return (
            "<guild.entry_point_utils.EntryPointResources "
            f"group={self.group} desc={self.desc}>"
        )

    @property
    def _resources(self):
        if self.__resources is None:
            self.__resources = self._init_resources()
        return self.__resources

    @property
    def _working_set(self):
        if self.__working_set is not None:
            return self.__working_set
        return working_set

    def _init_resources(self):
        resources = {}
        for ep in self._working_set.iter_entry_points(self.group):
            res_list = resources.setdefault(ep.name, [])
            res_list.append(Resource(ep))
        return resources

    def __iter__(self):
        for name in self._resources:
            for res_inst in self.for_name(name):
                yield name, res_inst

    def one_for_name(self, name):
        try:
            return next(self.for_name(name))
        except StopIteration as e:
            raise LookupError(name) from e

    def for_name(self, name):
        try:
            name_resources = self._resources[name]
        except KeyError as e:
            raise LookupError(name) from e
        else:
            for res in name_resources:
                try:
                    inst = res.inst()
                except Exception as e:
                    if log.getEffectiveLevel() <= logging.DEBUG:
                        log.exception("error initializing %s", res)
                    else:
                        log.error("error initializing %s: %s", res, e)
                else:
                    yield inst

    def path(self):
        return self._working_set.entries

    def set_path(self, val, clear_cache=False):
        if clear_cache:
            self._clear_path_importer_cache(val)
        self.__working_set = WorkingSet(val)
        self.__resources = None

    @staticmethod
    def _clear_path_importer_cache(paths):
        for path in paths:
            try:
                del sys.path_importer_cache[path]
            except KeyError:
                pass
