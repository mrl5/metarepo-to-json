#!/usr/bin/env python3

from pathlib import Path

from metarepo2json.metarepo2json.interfaces import CategoriesInterface


def __init__(hub):
    global HUB
    global categories_subpath
    global commit

    global get_category
    global get_fs_file_from_commit
    global InvalidStructureError
    global CorruptedKitError

    HUB = hub
    categories_subpath = hub.OPT.metarepo2json.categories_subpath
    commit = hub.OPT.metarepo2json.commit

    get_category = hub.metarepo2json.utils.get_category
    get_fs_file_from_commit = hub.metarepo2json.utils.get_fs_file_from_commit
    InvalidStructureError = hub.metarepo2json.errors.InvalidStructureError
    CorruptedKitError = hub.metarepo2json.errors.CorruptedKitError


class CategoriesFromFileSystem(CategoriesInterface):
    def __init__(self, kit_location=None):
        self.hub = HUB
        self.kit_location = kit_location
        self.commit = commit
        self.categories_subpath = categories_subpath
        self.categories_location = None
        self.cat_list = None
        self.categories = None

    def _set_locations(self):
        self.categories_location = Path(self.kit_location).joinpath(
            self.categories_subpath
        )

    def _throw_on_invalid_repo(self):
        if not Path.is_file(self.categories_location):
            errmsg = "Invalid kit structure"
            raise InvalidStructureError(errmsg)

    async def _load_data(self):
        if self.commit is None:
            with open(self.categories_location) as f:
                self.cat_list = f.read().splitlines()
        else:
            self.cat_list = get_fs_file_from_commit(
                self.kit_location, self.commit, self.categories_subpath
            ).splitlines()

    def _is_repo_fs_structure_valid(self):
        try:
            return (
                all([Path.is_dir(Path(f"{self.kit_location}/{c}"))
                    for c in self.cat_list])
                )
        except Exception:
            return False

    def _throw_on_corrupted_repo(self):
        if not self._is_repo_fs_structure_valid():
            errmsg = "Categories mismatch"
            raise CorruptedKitError(errmsg)

    async def load_data(self, location=None, **kwargs):
        if location is not None:
            self.kit_location = location
        self._set_locations()
        self._throw_on_invalid_repo()
        await self._load_data()
        self._throw_on_corrupted_repo()

    async def process_data(self):
        categories = []
        for cat in self.cat_list:
            categories.append(get_category(cat))
        self.categories = categories

    async def get_result(self) -> dict:
        if self.kit_location is None or self.categories_location is None:
            await self.load_data()
        if self.categories is None:
            await self.process_data()
        return self.categories
