#!/usr/bin/env python3

import json
from pathlib import Path

import aiofiles

from metarepo2json.metarepo2json.interfaces import KitsInterface


def __init__(hub):
    global HUB
    global repo_fs
    global commit
    global kitinfo_subpath
    global kitsha1_subpath
    global version_subpath

    global throw_on_corrupted_metarepo
    global get_kit
    global get_fs_file_from_commit
    global sort_kits
    global InvalidStructureError

    HUB = hub
    repo_fs = hub.OPT.metarepo2json.repo_fs
    commit = hub.OPT.metarepo2json.commit
    kitinfo_subpath = hub.OPT.metarepo2json.kitinfo_subpath
    kitsha1_subpath = hub.OPT.metarepo2json.kitsha1_subpath
    version_subpath = hub.OPT.metarepo2json.version_subpath

    throw_on_corrupted_metarepo = hub.metarepo2json.utils.throw_on_corrupted_metarepo
    get_kit = hub.metarepo2json.utils.get_kit
    get_fs_file_from_commit = hub.metarepo2json.utils.get_fs_file_from_commit
    sort_kits = hub.metarepo2json.utils.sort_list_of_dicts_by_key_values
    InvalidStructureError = hub.metarepo2json.errors.InvalidStructureError


class KitsFromFileSystem(KitsInterface):
    def __init__(self, metarepo_location=None):
        self.hub = HUB
        self.metarepo_location = (
            metarepo_location if metarepo_location is not None else repo_fs
        )
        self.commit = commit
        self.kitinfo_location = None
        self.kitsha1_location = None
        self.kitinfo = None
        self.kitsha1 = None
        self.kits = None

    def _set_locations(self):
        self.kitinfo_location = Path(self.metarepo_location).joinpath(kitinfo_subpath)
        self.kitsha1_location = Path(self.metarepo_location).joinpath(kitsha1_subpath)

    async def _load_data(self):
        if self.commit is None:
            async with aiofiles.open(self.kitinfo_location) as f:
                self.kitinfo = json.loads(await f.read())
            async with aiofiles.open(self.kitsha1_location) as f:
                self.kitsha1 = json.loads(await f.read())
        else:
            self.kitinfo = json.loads(
                get_fs_file_from_commit(
                    self.metarepo_location, self.commit, kitinfo_subpath
                )
            )
            self.kitsha1 = json.loads(
                get_fs_file_from_commit(
                    self.metarepo_location, self.commit, kitsha1_subpath
                )
            )

    def _is_repo_fs_structure_valid(self):
        try:
            return (
                Path.is_dir(Path(self.metarepo_location).joinpath(".git"))
                and Path.is_file(self.kitinfo_location)
                and Path.is_file(self.kitsha1_location)
                and Path.is_file(Path(self.metarepo_location).joinpath(version_subpath))
            )
        except Exception:
            return False

    async def load_data(self, location=None, **kwargs):
        if location is not None:
            self.metarepo_location = location
        self._set_locations()
        if not self._is_repo_fs_structure_valid():
            errmsg = "Invalid meta-repo structure"
            raise InvalidStructureError(errmsg)
        await self._load_data()
        throw_on_corrupted_metarepo(self.kitinfo, self.kitsha1)

    async def process_data(self):
        kits = []
        for kit_name, branches in self.kitinfo["release_defs"].items():
            kit_settings = self.kitinfo["kit_settings"][kit_name]
            kitsha1 = self.kitsha1[kit_name]
            kits.append(get_kit(kit_name, kit_settings, branches, kitsha1))
        self.kits = kits

    async def get_result(self) -> list:
        if self.kitinfo is None or self.kitsha1 is None:
            await self.load_data()
        if self.kits is None:
            await self.process_data()
        return sort_kits(self.kits, "name", self.kitinfo["kit_order"])
