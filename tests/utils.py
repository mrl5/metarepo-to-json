#!/usr/bin/env python3

import json
from pathlib import Path

import pop.hub
import pytest

from tests.mocks.categories import CATEGORIES as categories
from tests.mocks.kit_info import KIT_INFO as kitinfo_mock
from tests.mocks.kit_sha1 import KIT_SHA1 as kitsha1_mock

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="metarepo2json", omit_class=False)


def mkdirs(tmpdir, subdirs):
    for d in subdirs:
        Path.mkdir(tmpdir / d, parents=True)


def touch(tmpdir, files):
    for f in files:
        Path(tmpdir / f).touch(mode=0o664)


def write(paths, content):
    for p in paths:
        with open(p, "w") as f:
            f.write(content)


@pytest.fixture(scope="session")
def stub_metarepos(tmp_path_factory):
    test_subpaths = {
        "valid_metarepo": "meta-repo",
        "invalid_metarepo": "meta-repo-invalid",
        "corrupted_metarepo": "meta-repo-corrupted",
    }

    metarepos = {
        "valid_metarepo": tmp_path_factory.mktemp(test_subpaths["valid_metarepo"]),
        "invalid_metarepo": tmp_path_factory.mktemp(test_subpaths["invalid_metarepo"]),
        "corrupted_metarepo": tmp_path_factory.mktemp(
            test_subpaths["corrupted_metarepo"]
        ),
    }
    mkdirs(metarepos["valid_metarepo"], [".git", "kits", "metadata"])
    mkdirs(metarepos["invalid_metarepo"], ["kits", "metadata"])
    mkdirs(metarepos["corrupted_metarepo"], [".git", "kits", "metadata"])
    touch(
        metarepos["valid_metarepo"],
        [
            hub.OPT.metarepo2json.kitinfo_subpath,
            hub.OPT.metarepo2json.kitsha1_subpath,
            hub.OPT.metarepo2json.version_subpath,
        ],
    )
    touch(
        metarepos["corrupted_metarepo"],
        [
            hub.OPT.metarepo2json.kitinfo_subpath,
            hub.OPT.metarepo2json.kitsha1_subpath,
            hub.OPT.metarepo2json.version_subpath,
        ],
    )
    write(
        [metarepos["valid_metarepo"] / hub.OPT.metarepo2json.kitinfo_subpath],
        json.dumps(kitinfo_mock),
    )
    write(
        [metarepos["valid_metarepo"] / hub.OPT.metarepo2json.kitsha1_subpath],
        json.dumps(kitsha1_mock),
    )
    write(
        [
            metarepos["corrupted_metarepo"] / hub.OPT.metarepo2json.kitinfo_subpath,
            metarepos["corrupted_metarepo"] / hub.OPT.metarepo2json.kitsha1_subpath,
            metarepos["corrupted_metarepo"] / hub.OPT.metarepo2json.version_subpath,
        ],
        "{}",
    )
    return metarepos


@pytest.fixture(scope="session")
def stub_kits(stub_metarepos):
    metarepos = stub_metarepos
    kits = {
        "valid_kit": metarepos["valid_metarepo"]
        / hub.OPT.metarepo2json.kits_subpath
        / "test-kit-valid",
        "invalid_kit": metarepos["valid_metarepo"]
        / hub.OPT.metarepo2json.kits_subpath
        / "test-kit-invalid",
        "corrupted_kit": metarepos["valid_metarepo"]
        / hub.OPT.metarepo2json.kits_subpath
        / "test-kit-corrupted",
    }
    profiles = Path(hub.OPT.metarepo2json.categories_subpath).parent
    mkdirs(kits["valid_kit"], [profiles, *categories])
    mkdirs(kits["invalid_kit"], categories)
    mkdirs(kits["corrupted_kit"], [profiles, *categories[:-1]])
    touch(kits["valid_kit"], [hub.OPT.metarepo2json.categories_subpath])
    touch(kits["corrupted_kit"], [hub.OPT.metarepo2json.categories_subpath])
    write(
        [
            kits["valid_kit"] / hub.OPT.metarepo2json.categories_subpath,
            kits["corrupted_kit"] / hub.OPT.metarepo2json.categories_subpath,
        ],
        str("\n".join(categories)),
    )
    return kits


@pytest.fixture(scope="function")
def github_netlocs():
    return [
        "github.com",
        "github.com:443",
        "www.github.com",
    ]


@pytest.fixture(scope="function")
def funtoo_stash_netlocs():
    return [
        "code.funtoo.org",
        "code.funtoo.org:443",
    ]


@pytest.fixture(scope="function")
def custom_branch():
    return "develop"


@pytest.fixture(scope="function")
def github_repos():
    return ["/funtoo/meta-repo"]


@pytest.fixture(scope="function")
def bitbucket_repos():
    return [
        "/bitbucket/projects/AUTO/repos/meta-repo",
        "/bitbucket/projects/AUTO/repos/meta-repo/browse",
        "/bitbucket/users/drobbins/repos/funtoo-metatools",
    ]


@pytest.fixture(scope="function")
def invalid_github_paths():
    return ["", "/", "/cats"]


@pytest.fixture(scope="function")
def invalid_funtoo_stash_paths():
    return [
        "",
        "/",
        "/cats",
        "/bitbucket/projects",
        "/bitbucket/projects/AUTO",
        "/bitbucket/projects/AUTO/repos",
    ]


@pytest.fixture(scope="function")
def github_uris(github_netlocs, github_repos):
    netlocs = github_netlocs
    repos = github_repos
    return [
        f"{netlocs[0]}{repos[0]}",
        f"{netlocs[0]}{repos[0]}",
        f"{netlocs[1]}{repos[0]}",
        f"{netlocs[2]}{repos[0]}",
        f"https://{netlocs[0]}{repos[0]}",
    ]


@pytest.fixture(scope="function")
def funtoo_stash_uris(funtoo_stash_netlocs, bitbucket_repos, custom_branch):
    netlocs = funtoo_stash_netlocs
    repos = bitbucket_repos
    branch = custom_branch
    return [
        f"{netlocs[0]}{repos[0]}",
        f"{netlocs[0]}{repos[0]}",
        f"{netlocs[0]}{repos[1]}",
        f"{netlocs[0]}{repos[2]}",
        f"https://{netlocs[0]}{repos[0]}",
        f"{netlocs[0]}{repos[0]}?at=refs%2Fheads%2F{branch}",
        f"{netlocs[0]}{repos[1]}?at=refs%2Fheads%2F{branch}",
    ]


@pytest.fixture(scope="function")
def invalid_git_service_uri():
    return "https://nonexisting.gitservice.com/foo/bar"


@pytest.fixture(scope="function")
def get_schema():
    return hub.metarepo2json.factory.get_schema
