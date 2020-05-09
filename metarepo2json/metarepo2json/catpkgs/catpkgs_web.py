#!/usr/bin/env python3

import asyncio
import json
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlunparse

from metarepo2json.metarepo2json.interfaces import CatPkgsInterface


def __init__(hub):
    global HUB
    global GitServiceError
    global CorruptedKitError

    global fetcher
    global parse_uri
    global is_github
    global is_github_api_blob
    global is_funtoo_stash
    global get_github_tree_uri
    global get_funtoo_stash_tree_uri
    global get_raw_file_uri
    global get_ebuild_version
    global get_ebuild_properties
    global get_package
    global get_coroutine_results

    HUB = hub
    GitServiceError = hub.metarepo2json.errors.GitServiceError
    CorruptedKitError = hub.metarepo2json.errors.CorruptedKitError

    fetcher = hub.metarepo2json.http_fetcher.fetch_html
    parse_uri = hub.metarepo2json.utils.parse_uri
    is_github = hub.metarepo2json.utils.is_github
    is_github_api_blob = hub.metarepo2json.utils.is_github_api_blob
    is_funtoo_stash = hub.metarepo2json.utils.is_funtoo_stash
    get_github_tree_uri = hub.metarepo2json.utils.get_github_tree_uri
    get_funtoo_stash_tree_uri = hub.metarepo2json.utils.get_funtoo_stash_tree_uri
    get_raw_file_uri = hub.metarepo2json.utils.get_raw_file_uri
    get_ebuild_version = hub.metarepo2json.utils.get_ebuild_version
    get_ebuild_properties = hub.metarepo2json.utils.get_ebuild_properties
    get_package = hub.metarepo2json.utils.get_package
    get_coroutine_results = hub.metarepo2json.utils.get_coroutine_results


class CatPkgsFromWeb(CatPkgsInterface):
    def __init__(self, kit_location=None, category=None):
        self.hub = HUB
        self.session = None
        self.fetch = fetcher
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

    def _get_github_category_uri(self, tree):
        try:
            uri = list(
                filter(
                    lambda x: x["type"] == "tree" and x["path"] == self.category,
                    tree["tree"],
                )
            ).pop()["url"]
            return uri
        except IndexError:
            errmsg = f"{self.category} is not present in the kit tree"
            raise CorruptedKitError(errmsg)

    def _get_github_catpkgs(self, tree):
        return list(
            map(
                lambda x: {"name": x["path"], "url": x["url"]},
                filter(lambda x: x["type"] == "tree", tree["tree"]),
            )
        )

    async def _enrich_github_catpkg_with_ebuilds(self, catpkg):
        tree = json.loads(await self.fetch(catpkg["url"], self.session))
        ebuilds = list(
            map(
                lambda x: {"name": x["path"], "uri": x["url"]},
                filter(
                    lambda x: x["type"] == "blob" and x["path"].endswith(".ebuild"),
                    tree["tree"],
                ),
            )
        )
        return {**catpkg, "ebuilds": sorted(ebuilds, key=lambda x: x["name"])}

    async def _get_catpkgs_from_github(self, branch, commit):
        uri = get_github_tree_uri(self.kit_location, branch=branch, commit=commit)
        tree = json.loads(await self.fetch(uri, self.session))
        uri = self._get_github_category_uri(tree)
        category_tree = json.loads(await self.fetch(uri, self.session))
        catpkgs = self._get_github_catpkgs(category_tree)
        done_tasks, _ = await asyncio.wait(
            tuple(self._enrich_github_catpkg_with_ebuilds(catpkg) for catpkg in catpkgs)
        )
        return get_coroutine_results(done_tasks)

    def _get_funtoo_stash_category_uri(self, uri, tree):
        o = parse_uri(uri)
        try:
            node = list(
                map(
                    lambda x: x["node"],
                    filter(
                        lambda x: x["type"] == "DIRECTORY"
                        and x["path"]["name"] == self.category,
                        tree["children"]["values"],
                    ),
                )
            ).pop()
            ref = {"at": [node]}
            return urlunparse(o._replace(query=urlencode(ref, doseq=True)))
        except IndexError:
            raise CorruptedKitError(f"{self.category} is not present in the kit tree")

    def _get_funtoo_stash_catpkgs(self, category_tree):
        return list(
            map(
                lambda x: {
                    "name": x["path"]["name"],
                    "path": Path(self.category).joinpath(x["path"]["name"]),
                    "node": x["node"],
                },
                filter(
                    lambda x: x["type"] == "DIRECTORY", category_tree["children"]["values"]
                ),
            )
        )

    async def _enrich_funtoo_stash_catpkg_with_ebuilds(
        self, catpkg, parsed_uri, commit
    ):
        ref = {"at": [catpkg["node"]]}
        uri = urlunparse(parsed_uri._replace(query=urlencode(ref, doseq=True)))
        tree = json.loads(await self.fetch(uri, self.session))
        ebuilds = list(
            map(
                lambda x: {
                    "name": x["path"]["name"],
                    "uri": get_raw_file_uri(
                        self.kit_location,
                        str(catpkg["path"] / x["path"]["name"]),
                        commit=commit,
                    ),
                },
                filter(
                    lambda x: x["type"] == "FILE"
                    and x["path"]["name"].endswith(".ebuild"),
                    tree["children"]["values"],
                ),
            )
        )
        return {**catpkg, "ebuilds": sorted(ebuilds, key=lambda x: x["name"])}

    async def _get_catpkgs_from_funtoo_stash(self, branch, commit):
        uri = get_funtoo_stash_tree_uri(self.kit_location, branch=branch, commit=commit)
        tree = json.loads(await self.fetch(uri, self.session))
        uri = self._get_funtoo_stash_category_uri(uri, tree)
        category_tree = json.loads(await self.fetch(uri, self.session))
        catpkgs = self._get_funtoo_stash_catpkgs(category_tree)
        o = parse_uri(uri)
        done_tasks, _ = await asyncio.wait(
            tuple(
                self._enrich_funtoo_stash_catpkg_with_ebuilds(catpkg, o, commit)
                for catpkg in catpkgs
            )
        )
        return get_coroutine_results(done_tasks)

    async def _load_data(self, branch, commit):
        o = parse_uri(self.kit_location)
        if is_github(o.netloc):
            self._raw_catpkgs = await self._get_catpkgs_from_github(branch, commit)
        elif is_funtoo_stash(o.netloc):
            self._raw_catpkgs = await self._get_catpkgs_from_funtoo_stash(branch, commit)
        else:
            errmsg = f"Invalid Git service: {o.netloc}"
            raise GitServiceError(errmsg)

    def set_fetcher(self, fetcher):
        self.fetch = fetcher

    async def load_data(self, location=None, category=None, **kwargs):
        self.session = kwargs["session"] if "session" in kwargs else None
        branch = kwargs["branch"] if "branch" in kwargs else self.hub.OPT.metarepo2json.branch
        commit = kwargs["commit"] if "commit" in kwargs else self.hub.OPT.metarepo2json.commit
        self._set_location(location)
        self._set_category(category)
        await self._load_data(branch, commit)

    async def _process_catpkg(self, catpkg):
        versions = list(map(lambda x: get_ebuild_version(x["name"]), catpkg["ebuilds"]))
        uri = catpkg["ebuilds"].pop()["uri"]
        if is_github_api_blob(uri):
            headers = {"accept": "application/vnd.github.v3.raw"}
            ebuild = await self.fetch(uri, self.session, headers=headers)
        else:
            ebuild = await self.fetch(uri, self.session)
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
        done_tasks, _ = await asyncio.wait(
            tuple(self._process_catpkg(catpkg) for catpkg in self._raw_catpkgs)
        )
        catpkgs = get_coroutine_results(done_tasks)
        self.catpkgs = sorted(catpkgs, key=lambda x: x["name"])

    async def get_result(self) -> list:
        if self.kit_location is None:
            await self.load_data()
        if self.catpkgs is None:
            await self.process_data()
        return self.catpkgs
