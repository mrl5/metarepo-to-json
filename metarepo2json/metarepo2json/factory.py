#!/usr/bin/env python3

import json
from pathlib import Path


def __init__(hub):
    global schemas_subpath
    schemas_subpath = "schemas"


def get_kits_instance(hub, source="fs"):
    """ factory design pattern """
    kits = {
        "fs": hub.metarepo2json.kits.kits_fs.KitsFromFileSystem(),
        "web": hub.metarepo2json.kits.kits_web.KitsFromWeb(),
    }
    return kits[source]


def get_categories_instance(hub, source="fs"):
    categories = {
        "fs": hub.metarepo2json.categories.categories_fs.CategoriesFromFileSystem(),
        "web": hub.metarepo2json.categories.categories_web.CategoriesFromWeb(),
    }
    return categories[source]


def get_schema(hub, schema) -> dict:
    schemas = {
        "kit": "kit.schema.json",
        "category": "category.schema.json",
        "package": "package.schema.json",
    }
    schema_json = schemas[schema]
    file_path = Path(__file__).resolve()
    schema_path = file_path.parent.joinpath(schemas_subpath).joinpath(schema_json)
    with open(schema_path) as f:
        schema = json.load(f)
    return schema
