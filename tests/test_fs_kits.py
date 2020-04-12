#!/usr/bin/env python3

import pytest
import json
import pop.hub
from jsonschema import validate
from os import path
from pathlib import Path
from .tests_conf import config as conf
from .mocks.metadata.kit_info import KIT_INFO as kitinfo_mock
from .mocks.metadata.kit_sha1 import KIT_SHA1 as kitsha1_mock

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="metarepo2json", omit_class=False)

FILE_DIR = path.dirname(path.realpath(__file__))
SCHEMAS_PATH = path.join(path.dirname(FILE_DIR), conf["schemas"]["SCHEMAS_DIR"])

KitsFromFileSystem = hub.metarepo2json.kits_fs.KitsFromFileSystem


def mkdirs(tmpdir, subdirs):
    for d in subdirs:
        Path.mkdir(tmpdir / d)


def touch(tmpdir, files):
    for f in files:
        Path(tmpdir / f).touch(mode=0o664)


def write(paths, content):
    for p in paths:
        with open(p, 'w') as f:
            f.write(content)


@pytest.fixture(scope="session")
def stub_metarepos(tmp_path_factory):
    test_subpaths = {
        "valid_metarepo": "meta-repo",
        "invalid_metarepo": "meta-repo-invalid",
        "corrupted_metarepo": "meta-repo-corrupted"
    }

    metarepos = {
        "valid_metarepo": tmp_path_factory.mktemp(test_subpaths["valid_metarepo"]),
        "invalid_metarepo": tmp_path_factory.mktemp(test_subpaths["invalid_metarepo"]),
        "corrupted_metarepo": tmp_path_factory.mktemp(test_subpaths["corrupted_metarepo"])
    }
    mkdirs(metarepos["valid_metarepo"], [".git", "kits", "metadata"])
    mkdirs(metarepos["invalid_metarepo"], ["kits", "metadata"])
    mkdirs(metarepos["corrupted_metarepo"], [".git", "kits", "metadata"])
    touch(metarepos["valid_metarepo"], [
        hub.OPT.metarepo2json.kitinfo_subpath,
        hub.OPT.metarepo2json.kitsha1_subpath,
        hub.OPT.metarepo2json.version_subpath
    ])
    touch(metarepos["corrupted_metarepo"], [
        hub.OPT.metarepo2json.kitinfo_subpath,
        hub.OPT.metarepo2json.kitsha1_subpath,
        hub.OPT.metarepo2json.version_subpath
    ])
    write([metarepos["valid_metarepo"]/hub.OPT.metarepo2json.kitinfo_subpath],
          json.dumps(kitinfo_mock))
    write([metarepos["valid_metarepo"]/hub.OPT.metarepo2json.kitsha1_subpath],
          json.dumps(kitsha1_mock))
    write([
        metarepos["corrupted_metarepo"]/hub.OPT.metarepo2json.kitinfo_subpath,
        metarepos["corrupted_metarepo"]/hub.OPT.metarepo2json.kitsha1_subpath,
        metarepos["corrupted_metarepo"]/hub.OPT.metarepo2json.version_subpath,
        ], "{}")
    return metarepos


@pytest.fixture(scope="function")
def fskit_valid_repo(stub_metarepos):
    fskit = KitsFromFileSystem(stub_metarepos["valid_metarepo"])
    return fskit


@pytest.fixture(scope="function")
def fskit_invalid_repo(stub_metarepos):
    fskit = KitsFromFileSystem(stub_metarepos["invalid_metarepo"])
    return fskit


@pytest.fixture(scope="function")
def fskit_corrupted_repo(stub_metarepos):
    fskit = KitsFromFileSystem(stub_metarepos["corrupted_metarepo"])
    print(fskit.metarepo_dir)
    return fskit


def test_load_data_source(fskit_invalid_repo, fskit_corrupted_repo):
    with pytest.raises(hub.metarepo2json.kits_fs.InvalidMetarepoStructureError):
        fskit_invalid_repo.load_data_source()
    with pytest.raises(hub.metarepo2json.kits_fs.CorruptedMetarepoError):
        fskit_corrupted_repo.load_data_source()


def test_get_kits_data(fskit_valid_repo):
    schema_path = path.join(SCHEMAS_PATH, conf["schemas"]["KIT"])
    with open(schema_path) as f:
        kit_schema = json.load(f)
    fskit_valid_repo.load_data_source()
    for kit in fskit_valid_repo.get_kits_data():
        validate(instance=kit, schema=kit_schema)
