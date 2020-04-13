#!/usr/bin/env python3

import pop.hub
import pytest
from jsonschema import validate
from tests.utils import stub_metarepos

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="metarepo2json", omit_class=False)
KitsFromFileSystem = hub.metarepo2json.kits.kits_fs.KitsFromFileSystem


@pytest.fixture(scope="function")
def kits_valid_repo(stub_metarepos):
    kits = KitsFromFileSystem(stub_metarepos["valid_metarepo"])
    return kits


@pytest.fixture(scope="function")
def kits_invalid_repo(stub_metarepos):
    kits = KitsFromFileSystem(stub_metarepos["invalid_metarepo"])
    return kits


@pytest.fixture(scope="function")
def kits_corrupted_repo(stub_metarepos):
    kits = KitsFromFileSystem(stub_metarepos["corrupted_metarepo"])
    return kits


@pytest.fixture(scope="function")
def get_kit_schema():
    return hub.metarepo2json.factory.get_kit_schema


@pytest.mark.asyncio
async def test_load_data(kits_invalid_repo, kits_corrupted_repo):
    with pytest.raises(hub.metarepo2json.errors.InvalidMetarepoStructureError):
        await kits_invalid_repo.load_data()
    with pytest.raises(hub.metarepo2json.errors.CorruptedMetarepoError):
        await kits_corrupted_repo.load_data()


@pytest.mark.asyncio
async def test_get_result(kits_valid_repo, get_kit_schema):
    kit_schema = get_kit_schema()
    kits = await kits_valid_repo.get_result()
    for kit in kits:
        validate(instance=kit, schema=kit_schema)
