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
KitsFromWeb = hub.metarepo2json.kits.kits_web.KitsFromWeb


@pytest.fixture(scope="function")
def valid_metarepo(funtoo_stash_uris):
    uris = funtoo_stash_uris
    kits = KitsFromWeb(uris[0])
    return kits


@pytest.fixture(scope="function")
def invalid_metarepo(invalid_git_service_uri):
    kits = KitsFromWeb(invalid_git_service_uri)
    return kits


@pytest.mark.asyncio
async def test_load_data(invalid_metarepo):
    with pytest.raises(hub.metarepo2json.errors.GitServiceError):
        await invalid_metarepo.load_data()


@pytest.mark.asyncio
async def test_get_result(valid_metarepo, funtoo_stash_uris, get_schema):
    uri = funtoo_stash_uris[0]
    valid_metarepo.set_fetcher(stub_get_page)
    kit_schema = get_schema("kit")
    async with ClientSession() as session:
        await valid_metarepo.load_data(uri, session=session)
    await valid_metarepo.process_data()
    kits = await valid_metarepo.get_result()
    for kit in kits:
        validate(instance=kit, schema=kit_schema)
