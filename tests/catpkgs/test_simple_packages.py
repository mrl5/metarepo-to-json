from pathlib import Path

import pop.hub
import pytest
from jsonschema import validate

import tests.mocks.ebuilds.brave_bin as brave_bin
import tests.mocks.ebuilds.firefox as firefox
import tests.mocks.ebuilds.gjs as gjs
import tests.mocks.ebuilds.iTeML as iTeML
import tests.mocks.ebuilds.jbuilder as jbuilder
import tests.mocks.ebuilds.nicotine_plus as nicotine_plus
import tests.mocks.ebuilds.ppx_bench as ppx_bench
import tests.mocks.ebuilds.w3m as w3m
from tests.utils import (bitbucket_repos, custom_branch, funtoo_stash_netlocs,
                         funtoo_stash_uris, get_schema, github_netlocs,
                         github_repos, github_uris, invalid_funtoo_stash_paths,
                         invalid_git_service_uri, invalid_github_paths,
                         stub_kits, stub_metarepos, stub_packages)

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="metarepo2json", omit_class=False)


@pytest.fixture(scope="function")
def get_fs_packages():
    return hub.metarepo2json.catpkgs.simple_packages.get_fs_packages


def test_get_fs_packages(stub_packages, get_fs_packages, get_schema):
    cat = stub_packages / "www-client"
    package_schema = get_schema("package")
    packages = get_fs_packages(str(Path(cat)))
    for package in packages:
        validate(instance=package, schema=package_schema)
    assert packages == [
        firefox.PACKAGE_INFO,
        brave_bin.PACKAGE_INFO,
    ]
    package = stub_packages / "www-client" / "firefox"
    assert get_fs_packages(str(Path(package))) == [firefox.PACKAGE_INFO]
    package = stub_packages / "virtual" / "gjs"
    print(get_fs_packages(str(Path(package))))
    assert get_fs_packages(str(Path(package))) == [gjs.PACKAGE_INFO]
    package = stub_packages / "virtual" / "iTeML"
    assert get_fs_packages(str(Path(package))) == [iTeML.PACKAGE_INFO]
    package = stub_packages / "virtual" / "jbuilder"
    assert get_fs_packages(str(Path(package))) == [jbuilder.PACKAGE_INFO]
    package = stub_packages / "virtual" / "nicotine+"
    assert get_fs_packages(str(Path(package))) == [nicotine_plus.PACKAGE_INFO]
    package = stub_packages / "virtual" / "ppx_bench"
    assert get_fs_packages(str(Path(package))) == [ppx_bench.PACKAGE_INFO]
    package = stub_packages / "virtual" / "w3m"
    assert get_fs_packages(str(Path(package))) == [w3m.PACKAGE_INFO]
