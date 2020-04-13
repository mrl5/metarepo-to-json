#!/usr/bin/env python3

import asyncio
import pop.hub
import pytest
from jsonschema import validate
from aiohttp import ClientSession
from tests.mocks.async_http_fetch import stub_get_page
from tests.utils import funtoo_stash_uris, invalid_git_service_uri, \
        funtoo_stash_netlocs, bitbucket_repos, custom_branch

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="metarepo2json", omit_class=False)
KitsFromWeb = hub.metarepo2json.kits.kits_web.KitsFromWeb


@pytest.fixture(scope="function")
def kits_valid_repo(funtoo_stash_uris):
    uris = funtoo_stash_uris
    kits = KitsFromWeb(uris[0])
    return kits


@pytest.fixture(scope="function")
def kits_invalid_repo(invalid_git_service_uri):
    kits = KitsFromWeb(invalid_git_service_uri)
    return kits


@pytest.fixture(scope="function")
def get_kit_schema():
    return hub.metarepo2json.factory.get_kit_schema


@pytest.mark.asyncio
async def test_load_data(kits_invalid_repo):
    with pytest.raises(hub.metarepo2json.errors.GitServiceError):
        await kits_invalid_repo.load_data()


@pytest.mark.asyncio
async def test_get_result(kits_valid_repo, funtoo_stash_uris, get_kit_schema):
    uri = funtoo_stash_uris[0]
    kits_valid_repo._set_fetcher(stub_get_page)
    kit_schema = get_kit_schema()
    async with ClientSession() as session:
        await kits_valid_repo.load_data(uri, session=session)
    await kits_valid_repo.process_data()
    kits = await kits_valid_repo.get_result()
    for kit in kits:
        validate(instance=kit, schema=kit_schema)
