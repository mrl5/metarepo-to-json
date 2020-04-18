#!/usr/bin/env python3


import asyncio
import json
import logging
import sys

import pop.hub
from aiohttp import ClientSession

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="metarepo2json", omit_class=False)

ALLOWED_SOURCES = ["fs", "web"]


def process_errors(errors):
    sys.stderr.write("\n\n")
    for e in errors:
        logging.error(repr(e))
    sys.stderr.write("\n\nErrors encountered.\n")


async def print_categories(instance):
    categories = None
    if (
        type(instance)
        is hub.metarepo2json.categories.categories_fs.CategoriesFromFileSystem
    ):
        path = hub.OPT.metarepo2json.repo_fs
        await instance.load_data(path)
        await instance.process_data()
    if type(instance) is hub.metarepo2json.categories.categories_web.CategoriesFromWeb:
        uri = hub.OPT.metarepo2json.repo_web
        async with ClientSession() as session:
            await instance.load_data(uri, session=session)
        await instance.process_data()
    categories = await instance.get_result()
    print(json.dumps(categories))


def exit_on_invalid_source(source):
    if source not in ALLOWED_SOURCES:
        sys.exit(f"Invalid source: {source}")


if __name__ == "__main__":
    source = hub.OPT.metarepo2json.data_source
    exit_on_invalid_source(source)
    instance = hub.metarepo2json.factory.get_categories_instance(source)
    expected_errors = [
        hub.metarepo2json.errors.InvalidStructureError,
        hub.metarepo2json.errors.CorruptedKitError,
        hub.metarepo2json.errors.GitServiceError,
        hub.metarepo2json.errors.GitHubRepoURIError,
        hub.metarepo2json.errors.FuntooStashRepoURIError,
    ]
    try:
        errors = asyncio.run(print_categories(instance))
        if errors:
            process_errors(errors)
            sys.exit(1)
    except Exception as e:
        if type(e) in expected_errors:
            sys.exit(str(e))
        else:
            raise e
