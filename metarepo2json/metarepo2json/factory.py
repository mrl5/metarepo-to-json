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


def get_kit_schema(hub) -> dict:
    kit_schema_json = "kit.schema.json"
    file_path = Path(__file__).resolve()
    kit_schema_path = file_path.parent.joinpath(schemas_subpath).joinpath(
        kit_schema_json
    )
    with open(kit_schema_path) as f:
        kit_schema = json.load(f)
    return kit_schema
