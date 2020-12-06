#!/usr/bin/env python3

# python3 scripts/get_catpkgs_json.py -c 5932b921ba48f44e9c19d19301ae9448bb3fd912

import asyncio
import json
import logging
import sys

import pop.hub
from aiohttp import ClientSession, TCPConnector

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="metarepo2json", omit_class=False)

ALLOWED_SOURCES = ["fs", "web"]

category = hub.OPT.metarepo2json.category
commit = hub.OPT.metarepo2json.commit
branch = hub.OPT.metarepo2json.branch


async def print_catpkgs(instance):
    catpkgs = None
    if type(instance) is hub.metarepo2json.catpkgs.catpkgs_fs.CatPkgsFromFileSystem:
        await instance.load_data(category=category, branch=branch)
    if type(instance) is hub.metarepo2json.catpkgs.catpkgs_web.CatPkgsFromWeb:
        uri = hub.OPT.metarepo2json.repo_web
        conn = TCPConnector(limit=10)
        async with ClientSession(connector=conn) as session:
            await instance.load_data(
                uri, session=session, category=category, commit=commit
            )
            await instance.process_data()
    catpkgs = await instance.get_result()
    print(json.dumps(catpkgs))


def process_errors(errors):
    sys.stderr.write("\n\n")
    for e in errors:
        logging.error(repr(e))
    sys.stderr.write("\n\nErrors encountered.\n")


def exit_on_invalid_source(source):
    if source not in ALLOWED_SOURCES:
        sys.exit(f"Invalid source: {source}")


if __name__ == "__main__":
    source = hub.OPT.metarepo2json.data_source
    kit = hub.OPT.metarepo2json.kit
    exit_on_invalid_source(source)
    instance = hub.metarepo2json.factory.get_catpkgs_instance(kit=kit, source=source)
    expected_errors = [
        hub.metarepo2json.errors.InvalidStructureError,
        hub.metarepo2json.errors.CorruptedKitError,
        hub.metarepo2json.errors.GitServiceError,
        hub.metarepo2json.errors.GitHubRepoURIError,
        hub.metarepo2json.errors.FuntooStashRepoURIError,
        ValueError,
    ]
    try:
        errors = asyncio.run(print_catpkgs(instance))
        if errors:
            process_errors(errors)
            sys.exit(1)
    except Exception as e:
        if type(e) in expected_errors:
            sys.exit(f"{type(e).__name__}: {str(e)}")
        else:
            raise e
