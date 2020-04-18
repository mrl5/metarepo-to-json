#!/usr/bin/env python3

from re import match

from metarepo2json.metarepo2json.interfaces import CategoriesInterface


def __init__(hub):
    global HUB
    global categories_subpath

    global fetcher
    global get_raw_file_uri
    global get_category

    HUB = hub
    categories_subpath = hub.OPT.metarepo2json.categories_subpath

    fetcher = hub.metarepo2json.http_fetcher.fetch_html
    get_raw_file_uri = hub.metarepo2json.utils.get_raw_file_uri
    get_category = hub.metarepo2json.utils.get_category


class CategoriesFromWeb(CategoriesInterface):
    def __init__(self, kit_location=None):
        self.hub = HUB
        self.fetch = fetcher
        self.kit_location = kit_location
        self.categories_subpath = categories_subpath
        self.categories_location = None
        self.cat_list = None
        self.categories = None

    def _set_locations(self):
        self.categories_location = get_raw_file_uri(
            self.kit_location, self.categories_subpath
        )

    def _set_session(self, session):
        self.session = session

    def set_fetcher(self, fetcher):
        self.fetch = fetcher

    async def _set_cat_list(self, session):
        self.cat_list = (
            await self.fetch(self.categories_location, session)
        ).splitlines()

    async def _load_data(self, session):
        await self._set_cat_list(session)

    def _throw_on_invalid_cat_list(self):
        if not all([match(r"[a-z\-]+", c) for c in self.cat_list]):
            raise ValueError("Malformed web content")

    async def load_data(self, location=None, **kwargs):
        if location is not None:
            self.kit_location = location
        session = kwargs["session"] if "session" in kwargs else None
        self._set_locations()
        await self._load_data(session)
        self._throw_on_invalid_cat_list()

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
