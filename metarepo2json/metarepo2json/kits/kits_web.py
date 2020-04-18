#!/usr/bin/env python3

import asyncio
import json

from metarepo2json.metarepo2json.interfaces import KitsInterface


def __init__(hub):
    global HUB
    global repo_web
    global kitinfo_subpath
    global kitsha1_subpath
    global version_subpath

    global fetcher
    global get_raw_file_uri
    global throw_on_corrupted_metarepo
    global get_kit
    global sort_kits

    HUB = hub
    repo_web = hub.OPT.metarepo2json.repo_web
    kitinfo_subpath = hub.OPT.metarepo2json.kitinfo_subpath
    kitsha1_subpath = hub.OPT.metarepo2json.kitsha1_subpath
    version_subpath = hub.OPT.metarepo2json.version_subpath

    fetcher = hub.metarepo2json.http_fetcher.fetch_html
    get_raw_file_uri = hub.metarepo2json.utils.get_raw_file_uri
    throw_on_corrupted_metarepo = (
        hub.metarepo2json.utils.throw_on_corrupted_metarepo
    )
    get_kit = hub.metarepo2json.utils.get_kit
    sort_kits = hub.metarepo2json.utils.sort_list_of_dicts_by_key_values


class KitsFromWeb(KitsInterface):
    def __init__(self, metarepo_location=None):
        self.hub = HUB
        self.fetch = fetcher
        self.metarepo_location = (
            metarepo_location
            if metarepo_location is not None
            else repo_web
        )
        self.kitinfo_location = None
        self.kitsha1_location = None
        self.kitinfo = None
        self.kitsha1 = None
        self.kits = None

    def _set_locations(self):
        self.kitinfo_location = get_raw_file_uri(
            self.metarepo_location, kitinfo_subpath
        )
        self.kitsha1_location = get_raw_file_uri(
            self.metarepo_location, kitsha1_subpath
        )

    def _set_session(self, session):
        self.session = session

    def set_fetcher(self, fetcher):
        self.fetch = fetcher

    async def _set_kitinfo(self, session):
        self.kitinfo = json.loads(await self.fetch(self.kitinfo_location, session))

    async def _set_kitsha1(self, session):
        self.kitsha1 = json.loads(await self.fetch(self.kitsha1_location, session))

    async def _load_data(self, session):
        await asyncio.wait([self._set_kitinfo(session), self._set_kitsha1(session)])

    async def load_data(self, location=None, **kwargs):
        if location is not None:
            self.metarepo_location = location
        session = kwargs["session"] if "session" in kwargs else None
        self._set_locations()
        await self._load_data(session)
        throw_on_corrupted_metarepo(self.kitinfo, self.kitsha1)

    async def process_data(self):
        kits = []
        for kit_name, branches in self.kitinfo["release_defs"].items():
            kit_settings = self.kitinfo["kit_settings"][kit_name]
            kitsha1 = self.kitsha1[kit_name]
            kits.append(get_kit(kit_name, kit_settings, branches, kitsha1))
        self.kits = kits

    async def get_result(self) -> dict:
        if self.kitinfo_location is None or self.kitsha1_location is None:
            await self.load_data()
        if self.kits is None:
            await self.process_data()
        return sort_kits(self.kits, "name", self.kitinfo["kit_order"])
