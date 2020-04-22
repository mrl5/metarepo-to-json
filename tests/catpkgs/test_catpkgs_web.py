#!/usr/bin/env python3

import pop.hub
import pytest
from aiohttp import ClientSession
from jsonschema import validate

from tests.mocks.async_http_fetch import stub_get_page
from tests.utils import (bitbucket_repos, custom_branch, funtoo_stash_netlocs,
                         funtoo_stash_uris, get_schema, github_netlocs,
                         github_repos, github_uris, invalid_git_service_uri)

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="metarepo2json", omit_class=False)
CatPkgsFromWeb = hub.metarepo2json.catpkgs.catpkgs_web.CatPkgsFromWeb
commit = "5932b921ba48f44e9c19d19301ae9448bb3fd912"


@pytest.fixture(scope="function")
def valid_catpkgs(funtoo_stash_uris):
    uris = funtoo_stash_uris
    catpkgs = CatPkgsFromWeb(uris[0])
    return catpkgs


@pytest.fixture(scope="function")
def invalid_catpkgs(invalid_git_service_uri):
    catpkgs = CatPkgsFromWeb(invalid_git_service_uri)
    return catpkgs


@pytest.mark.asyncio
async def test_load_data(invalid_catpkgs, valid_catpkgs, github_uris, funtoo_stash_uris):
    category = "www-none"
    with pytest.raises(ValueError):
        await invalid_catpkgs.load_data()
    with pytest.raises(ValueError):
        await invalid_catpkgs.load_data(invalid_catpkgs.kit_location)
    with pytest.raises(hub.metarepo2json.errors.GitServiceError):
        await invalid_catpkgs.load_data(invalid_catpkgs.kit_location, category=category)
    with pytest.raises(hub.metarepo2json.errors.CorruptedKitError):
        valid_catpkgs.set_fetcher(stub_get_page)
        async with ClientSession() as session:
            uris = github_uris
            await valid_catpkgs.load_data(uris[0], session=session, category=category, commit=commit)
    with pytest.raises(hub.metarepo2json.errors.CorruptedKitError):
        valid_catpkgs.set_fetcher(stub_get_page)
        async with ClientSession() as session:
            uris = funtoo_stash_uris
            await valid_catpkgs.load_data(uris[0], session=session, category=category, commit=commit)


@pytest.mark.asyncio
async def test_get_result_github(valid_catpkgs, github_uris, get_schema):
    category = "www-client"
    valid_catpkgs.set_fetcher(stub_get_page)
    package_schema = get_schema("package")
    uri = github_uris[0]
    async with ClientSession() as session:
        await valid_catpkgs.load_data(
            uri, session=session, category=category, commit=commit
        )
    await valid_catpkgs.process_data()
    catpkgs = await valid_catpkgs.get_result()
    for package in catpkgs:
        validate(instance=package, schema=package_schema)


@pytest.mark.asyncio
async def test_get_result_funtoo_stash(valid_catpkgs, funtoo_stash_uris, get_schema):
    category = "www-client"
    valid_catpkgs.set_fetcher(stub_get_page)
    package_schema = get_schema("package")
    uri = funtoo_stash_uris[0]
    async with ClientSession() as session:
        await valid_catpkgs.load_data(
            uri, session=session, category=category, commit=commit
        )
    await valid_catpkgs.process_data()
    catpkgs = await valid_catpkgs.get_result()
    for package in catpkgs:
        validate(instance=package, schema=package_schema)
