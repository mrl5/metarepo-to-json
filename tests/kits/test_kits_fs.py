#!/usr/bin/env python3

import pop.hub
import pytest
from jsonschema import validate
from tests.utils import stub_metarepos, get_schema

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="metarepo2json", omit_class=False)
KitsFromFileSystem = hub.metarepo2json.kits.kits_fs.KitsFromFileSystem


@pytest.fixture(scope="function")
def valid_metarepo(stub_metarepos):
    kits = KitsFromFileSystem(stub_metarepos["valid_metarepo"])
    return kits


@pytest.fixture(scope="function")
def invalid_metarepo(stub_metarepos):
    kits = KitsFromFileSystem(stub_metarepos["invalid_metarepo"])
    return kits


@pytest.fixture(scope="function")
def corrupted_metarepo(stub_metarepos):
    kits = KitsFromFileSystem(stub_metarepos["corrupted_metarepo"])
    return kits


@pytest.mark.asyncio
async def test_load_data(invalid_metarepo, corrupted_metarepo):
    with pytest.raises(hub.metarepo2json.errors.InvalidStructureError):
        await invalid_metarepo.load_data()
    with pytest.raises(hub.metarepo2json.errors.CorruptedMetarepoError):
        await corrupted_metarepo.load_data()


@pytest.mark.asyncio
async def test_get_result(valid_metarepo, get_schema):
    kit_schema = get_schema("kit")
    kits = await valid_metarepo.get_result()
    for kit in kits:
        validate(instance=kit, schema=kit_schema)
