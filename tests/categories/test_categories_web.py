#!/usr/bin/env python3

import pop.hub
import pytest
from jsonschema import validate
from aiohttp import ClientSession
from tests.mocks.async_http_fetch import stub_get_page
from tests.utils import funtoo_stash_uris, invalid_git_service_uri, \
        funtoo_stash_netlocs, bitbucket_repos, custom_branch, get_schema

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="metarepo2json", omit_class=False)
CategoriesFromWeb = hub.metarepo2json.categories.categories_web.CategoriesFromWeb


@pytest.fixture(scope="function")
def valid_categories(funtoo_stash_uris):
    uris = funtoo_stash_uris
    categories = CategoriesFromWeb(uris[0])
    return categories


@pytest.fixture(scope="function")
def invalid_categories(invalid_git_service_uri):
    categories = CategoriesFromWeb(invalid_git_service_uri)
    return categories


@pytest.mark.asyncio
async def test_load_data(invalid_categories):
    with pytest.raises(hub.metarepo2json.errors.GitServiceError):
        await invalid_categories.load_data()


@pytest.mark.asyncio
async def test_get_result(valid_categories, funtoo_stash_uris, get_schema):
    uri = funtoo_stash_uris[0]
    valid_categories.set_fetcher(stub_get_page)
    category_schema = get_schema("category")
    async with ClientSession() as session:
        await valid_categories.load_data(uri, session=session)
    await valid_categories.process_data()
    categories = await valid_categories.get_result()
    for category in categories:
        validate(instance=category, schema=category_schema)
