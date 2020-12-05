#!/usr/bin/env python3

from os import walk
from pathlib import Path

from git import Repo

from metarepo2json.metarepo2json.interfaces import CatPkgsInterface


def __init__(hub):
    global HUB
    global CorruptedKitError

    global get_fs_file_from_commit
    global get_ebuild_version
    global get_ebuild_properties
    global get_package

    HUB = hub
    CorruptedKitError = hub.metarepo2json.errors.CorruptedKitError

    get_fs_file_from_commit = hub.metarepo2json.utils.get_fs_file_from_commit
    get_ebuild_version = hub.metarepo2json.utils.get_ebuild_version
    get_ebuild_properties = hub.metarepo2json.utils.get_ebuild_properties
    get_package = hub.metarepo2json.utils.get_package


class CatPkgsFromFileSystem(CatPkgsInterface):
    def __init__(self, kit_location=None, category=None):
        self.hub = HUB
        self.kit_location = kit_location
        self.category = category
        self._raw_catpkgs = None
        self.catpkgs = None

    def _set_location(self, location):
        if location is not None:
            self.kit_location = location
        else:
            raise ValueError("kit location is not specified")

    def _set_category(self, category):
        if category is not None:
            self.category = category
        else:
            raise ValueError("category is not specified")

    def _get_catpkg(self, name, path, ebuilds, commit):
        catpkg = {
            "name": name,
            "path": path,
            "ebuilds": sorted(
                list(map(lambda x: {"name": x, "path": path.joinpath(x)}, ebuilds,)),
                key=lambda x: x["name"],
            ),
        }
        if commit is not None:
            catpkg["commit"] = commit
        return catpkg

    def _walk_fs(self):
        path = Path(self.kit_location).joinpath(self.category)
        if not path.is_dir():
            errmsg = f"{self.category} is not present in the kit tree"
            raise CorruptedKitError(errmsg)
        raw_catpkgs = []
        tree = [d for d in walk(str(path))]
        for leafs in tree:
            if len(leafs) > 2:
                files = leafs[2]
                ebuilds = list(filter(lambda x: x.endswith(".ebuild"), files))
                if len(ebuilds) > 0:
                    package_path = Path(leafs[0])
                    raw_catpkgs.append(
                        self._get_catpkg(package_path.name, package_path, ebuilds, None)
                    )
        self._raw_catpkgs = raw_catpkgs

    def _walk_git_repo(self, branch, commit):
        raw_catpkgs = []
        if commit is None:
            commit = (
                list(filter(lambda x: x.name == branch, Repo(self.kit_location).heads))
                .pop()
                .object.hexsha
            )
        trees = Repo(self.kit_location).commit(commit).tree.trees
        tree_stack = list(filter(lambda x: x.name == self.category, trees))
        if not len(tree_stack) > 0:
            errmsg = f"{self.category} is not present in the kit tree"
            raise CorruptedKitError(errmsg)
        while len(tree_stack) > 0:
            tree = tree_stack.pop()
            ebuilds = list(
                map(
                    lambda x: x.name,
                    filter(lambda x: x.name.endswith(".ebuild"), tree.blobs),
                )
            )
            if len(ebuilds) > 0:
                package_path = Path(self.kit_location).joinpath(tree.path)
                raw_catpkgs.append(
                    self._get_catpkg(tree.name, package_path, ebuilds, commit)
                )
            else:
                tree_stack.extend(tree.trees)
        self._raw_catpkgs = raw_catpkgs

    def _load_data(self, branch, commit):
        if branch is None and commit is None:
            self._walk_fs()
        else:
            self._walk_git_repo(branch, commit)

    async def load_data(self, location=None, category=None, **kwargs):
        branch = kwargs["branch"] if "branch" in kwargs else self.hub.OPT.metarepo2json.branch
        commit = kwargs["commit"] if "commit" in kwargs else self.hub.OPT.metarepo2json.commit
        self._set_location(location)
        self._set_category(category)
        self._load_data(branch, commit)

    def _process_catpkg(self, catpkg):
        versions = list(map(lambda x: get_ebuild_version(catpkg["name"], x["name"]), catpkg["ebuilds"]))
        if "commit" in catpkg and catpkg["commit"] is not None:
            subpath = str(catpkg["ebuilds"].pop()["path"].relative_to(self.kit_location))
            ebuild = get_fs_file_from_commit(
                self.kit_location, catpkg["commit"], subpath
            )
        else:
            path = catpkg["ebuilds"].pop()["path"]
            with open(path) as f:
                ebuild = f.read()
        properties = get_ebuild_properties(ebuild)
        return get_package(
            catpkg["name"],
            versions,
            description=properties["description"],
            homepages=properties["homepages"],
            licenses=properties["licenses"],
        )

    async def process_data(self):
        catpkgs = []
        if self._raw_catpkgs is None:
            raise ValueError("no data is loaded")
        catpkgs = [self._process_catpkg(catpkg) for catpkg in self._raw_catpkgs]
        self.catpkgs = sorted(catpkgs, key=lambda x: x["name"])

    async def get_result(self) -> list:
        if self.kit_location is None:
            await self.load_data()
        if self.catpkgs is None:
            await self.process_data()
        return self.catpkgs
