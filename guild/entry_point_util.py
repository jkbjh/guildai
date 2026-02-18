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

import importlib.metadata
import importlib.util
import logging
import os
import sys
import threading

log = logging.getLogger("guild")


class _EntryPointShim:
    """Wraps importlib.metadata.EntryPoint to provide a resolve() method
    and a .dist attribute, matching the pkg_resources.EntryPoint interface
    that Resource.inst() and Resource.__str__() rely on.
    """

    def __init__(self, ep):
        self._ep = ep

    @property
    def name(self):
        return self._ep.name

    @property
    def dist(self):
        return getattr(self._ep, "dist", None)

    def resolve(self):
        """Return the class/callable this entry point refers to.

        Matches pkg_resources.EntryPoint.resolve() — returns the object
        that the entry point points to (e.g. a class), not an instance.
        Callers then invoke it themselves, passing self as the argument:
            ep.resolve()(ep)
        """
        return self._ep.load()

    def __str__(self):
        return str(self._ep)


class _PathWorkingSet:
    """Lightweight replacement for pkg_resources.WorkingSet.

    Scans *entries* (a list of sys.path-style directories) for installed
    distributions and exposes iter_entry_points(group), mirroring the
    subset of the pkg_resources.WorkingSet API used by EntryPointResources.

    For the global (unscoped) case we delegate directly to
    importlib.metadata, which already reflects the running environment.
    """

    def __init__(self, entries):
        self.entries = list(entries)

    def iter_entry_points(self, group):
        """Yield _EntryPointShim instances for *group* found in self.entries."""
        # Build a custom metadata path that only includes dist-info
        # directories reachable from our entries list.
        meta_path = self._meta_path()
        eps = importlib.metadata.entry_points(
            group=group,
            # path= was added in Python 3.12; for 3.8–3.11 we temporarily
            # patch sys.path instead (see _iter_with_path_patch).
        ) if self._supports_path_kwarg() else self._iter_with_path_patch(group)
        for ep in eps:
            yield _EntryPointShim(ep)

    def _supports_path_kwarg(self):
        import inspect
        sig = inspect.signature(importlib.metadata.entry_points)
        return "path" in sig.parameters

    def _meta_path(self):
        """Collect dist-info / egg-info directories under self.entries."""
        meta = []
        for entry in self.entries:
            if not os.path.isdir(entry):
                continue
            try:
                for name in os.listdir(entry):
                    if name.endswith((".dist-info", ".egg-info")):
                        meta.append(os.path.join(entry, name))
            except OSError:
                pass
        return meta

    def _iter_with_path_patch(self, group):
        """Python 3.8–3.11: temporarily replace sys.path to scope the search.

        Serialised with _path_patch_lock so concurrent calls from different
        threads don't observe each other's scoped sys.path.
        """
        with _path_patch_lock:
            old_path = sys.path[:]
            sys.path[:] = self.entries
            try:
                return list(importlib.metadata.entry_points(group=group))
            finally:
                sys.path[:] = old_path


class _GlobalWorkingSet:
    """Thin wrapper around the global importlib.metadata state.

    Used when no custom path has been set, equivalent to
    pkg_resources.working_set.
    """

    @property
    def entries(self):
        return sys.path

    def iter_entry_points(self, group):
        for ep in importlib.metadata.entry_points(group=group):
            yield _EntryPointShim(ep)


# Module-level singleton, equivalent to pkg_resources.working_set
_global_working_set = _GlobalWorkingSet()

# Lock serialising sys.path mutations in _iter_with_path_patch on Python
# 3.8-3.11, where entry_points() has no path= kwarg and we must temporarily
# swap sys.path to scope distribution discovery. Without this, concurrent
# calls from different threads would see each other's scoped path.
_path_patch_lock = threading.Lock()


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
        return _global_working_set

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
        self.__working_set = _PathWorkingSet(val)
        self.__resources = None

    @staticmethod
    def _clear_path_importer_cache(paths):
        for path in paths:
            try:
                del sys.path_importer_cache[path]
            except KeyError:
                pass
