#!/usr/bin/env python3

import pop.hub
import pytest
from jsonschema import validate
from tests.utils import stub_metarepos, stub_kits, get_schema

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="metarepo2json", omit_class=False)
CategoriesFromFileSystem = hub.metarepo2json.categories.categories_fs.CategoriesFromFileSystem


@pytest.fixture(scope="function")
def valid_categories(stub_kits):
    categories = CategoriesFromFileSystem(stub_kits["valid_kit"])
    return categories


@pytest.fixture(scope="function")
def invalid_categories(stub_kits):
    categories = CategoriesFromFileSystem(stub_kits["invalid_kit"])
    return categories


@pytest.fixture(scope="function")
def corrupted_categories(stub_kits):
    categories = CategoriesFromFileSystem(stub_kits["corrupted_kit"])
    return categories


@pytest.mark.asyncio
async def test_load_data(invalid_categories, corrupted_categories):
    with pytest.raises(hub.metarepo2json.errors.InvalidStructureError):
        await invalid_categories.load_data()
    with pytest.raises(hub.metarepo2json.errors.CorruptedKitError):
        await corrupted_categories.load_data()


@pytest.mark.asyncio
async def test_get_result(valid_categories, get_schema):
    category_schema = get_schema("category")
    categories = await valid_categories.get_result()
    for category in categories:
        validate(instance=category, schema=category_schema)
