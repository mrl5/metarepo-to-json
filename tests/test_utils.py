#!/usr/bin/env python3

import pop.hub
import pytest

from tests.mocks.kit_info import KIT_INFO
from tests.mocks.kit_sha1 import KIT_SHA1
from tests.utils import (bitbucket_repos, custom_branch, funtoo_stash_netlocs,
                         funtoo_stash_uris, github_netlocs, github_repos,
                         github_uris, invalid_funtoo_stash_paths,
                         invalid_git_service_uri, invalid_github_paths)

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="metarepo2json", omit_class=False)


@pytest.fixture(scope="function")
def get_raw_file_uri():
    return hub.metarepo2json.utils.get_raw_file_uri


@pytest.fixture(scope="function")
def get_github_raw_file_uri():
    return hub.metarepo2json.utils.get_github_raw_file_uri


@pytest.fixture(scope="function")
def get_funtoo_stash_raw_file_uri():
    return hub.metarepo2json.utils.get_funtoo_stash_raw_file_uri


@pytest.fixture(scope="function")
def is_metarepo_corrupted():
    return hub.metarepo2json.utils.is_metarepo_corrupted


@pytest.fixture(scope="function")
def sort_kits():
    return hub.metarepo2json.utils.sort_list_of_dicts_by_key_values


def test_is_github(github_netlocs, funtoo_stash_netlocs):
    valid_netlocs = github_netlocs
    invalid_netlocs = funtoo_stash_netlocs
    is_git_provider = hub.metarepo2json.utils.is_github
    for netloc in valid_netlocs:
        assert is_git_provider(netloc) is True
    for netloc in invalid_netlocs:
        assert is_git_provider(netloc) is False


def test_is_funtoo_stash(github_netlocs, funtoo_stash_netlocs):
    valid_netlocs = funtoo_stash_netlocs
    invalid_netlocs = github_netlocs
    is_git_provider = hub.metarepo2json.utils.is_funtoo_stash
    for netloc in valid_netlocs:
        assert is_git_provider(netloc) is True
    for netloc in invalid_netlocs:
        assert is_git_provider(netloc) is False


def test_is_github_repo_given(github_repos, invalid_github_paths):
    is_git_repo_given = hub.metarepo2json.utils.is_github_repo_given
    valid_paths = github_repos
    invalid_paths = invalid_github_paths
    for path in invalid_paths:
        assert is_git_repo_given(path) is False
    for path in valid_paths:
        assert is_git_repo_given(path) is True


def test_is_funtoo_stash_repo_given(bitbucket_repos, invalid_funtoo_stash_paths):
    is_git_repo_given = hub.metarepo2json.utils.is_bitbucket_repo_given
    valid_paths = bitbucket_repos
    invalid_paths = invalid_funtoo_stash_paths
    for path in invalid_paths:
        assert is_git_repo_given(path) is False
    for path in valid_paths:
        assert is_git_repo_given(path) is True


def test_is_github_tree_given(github_repos, custom_branch):
    validator = hub.metarepo2json.utils.is_github_tree_given
    assert validator(github_repos[0]) is False
    assert validator(f"github_repos[0]/tree/{custom_branch}") is True


def test_is_bitbucket_refs_given(github_repos, custom_branch):
    validator = hub.metarepo2json.utils.is_bitbucket_refs_given
    assert validator("stuff=1") is False
    assert validator(f"at=refs%2Fheads%2F{custom_branch}") is True
    assert validator(f"at=refs%2Fheads%2F{custom_branch}&stuff=1") is True
    assert validator(f"stuff=1&at=refs%2Fheads%2F{custom_branch}") is True


def test_get_github_raw_file_uri(
    get_github_raw_file_uri,
    funtoo_stash_netlocs,
    github_netlocs,
    github_repos,
    invalid_github_paths,
    github_uris,
    custom_branch,
):
    default_protocol = hub.OPT.metarepo2json.net_protocol
    default_branch = hub.OPT.metarepo2json.branch
    file_subpath = "metadata/kit-info.json"
    get_raw_file_uri = get_github_raw_file_uri
    uris = github_uris
    funtoo_stash_netlocs = funtoo_stash_netlocs
    with pytest.raises(hub.metarepo2json.errors.GitServiceError):
        get_raw_file_uri(funtoo_stash_netlocs[0], file_subpath)
    with pytest.raises(hub.metarepo2json.errors.GitHubRepoURIError):
        get_raw_file_uri(github_netlocs[0], file_subpath)
        get_raw_file_uri(f"{github_netlocs[0]}", file_subpath)
    base_uri = hub.OPT.metarepo2json.github_raw_netloc
    results = [
        get_raw_file_uri(uris[0], file_subpath),
        get_raw_file_uri(uris[1], file_subpath, branch=custom_branch),
        get_raw_file_uri(uris[2], file_subpath, branch=default_branch),
        get_raw_file_uri(uris[3], file_subpath, branch=default_branch),
        get_raw_file_uri(uris[4], file_subpath),
    ]
    expected_results = [
        f"{default_protocol}://{base_uri}{github_repos[0]}/{default_branch}/{file_subpath}",
        f"{default_protocol}://{base_uri}{github_repos[0]}/{custom_branch}/{file_subpath}",
        f"{default_protocol}://{base_uri}{github_repos[0]}/{default_branch}/{file_subpath}",
        f"{default_protocol}://{base_uri}{github_repos[0]}/{default_branch}/{file_subpath}",
        f"{default_protocol}://{base_uri}{github_repos[0]}/{default_branch}/{file_subpath}",
    ]
    assert len(results) == len(expected_results)
    for i, result in enumerate(results):
        assert result == expected_results[i]


def test_get_funtoo_stash_raw_file_uri(
    get_funtoo_stash_raw_file_uri,
    funtoo_stash_netlocs,
    github_netlocs,
    bitbucket_repos,
    invalid_funtoo_stash_paths,
    funtoo_stash_uris,
    custom_branch,
):
    default_protocol = hub.OPT.metarepo2json.net_protocol
    default_branch = hub.OPT.metarepo2json.branch
    file_subpath = "metadata/kit-info.json"
    get_raw_file_uri = get_funtoo_stash_raw_file_uri
    uris = funtoo_stash_uris
    with pytest.raises(hub.metarepo2json.errors.GitServiceError):
        get_raw_file_uri(github_netlocs[0], file_subpath)
    with pytest.raises(hub.metarepo2json.errors.FuntooStashRepoURIError):
        get_raw_file_uri(funtoo_stash_netlocs[0], file_subpath)
        get_raw_file_uri(
            f"{funtoo_stash_netlocs[0]}{invalid_funtoo_stash_paths}", file_subpath
        )
    base_uri = hub.OPT.metarepo2json.funtoo_stash_raw_netloc
    results = [
        get_raw_file_uri(uris[0], file_subpath),
        get_raw_file_uri(uris[1], file_subpath, branch=custom_branch),
        get_raw_file_uri(uris[2], file_subpath, branch=default_branch),
        get_raw_file_uri(uris[3], file_subpath, branch=default_branch),
        get_raw_file_uri(uris[4], file_subpath),
    ]
    expected_results = [
        f"{default_protocol}://{base_uri}{bitbucket_repos[0]}/raw/{file_subpath}?at=refs%2Fheads%2F{default_branch}",
        f"{default_protocol}://{base_uri}{bitbucket_repos[0]}/raw/{file_subpath}?at=refs%2Fheads%2F{custom_branch}",
        f"{default_protocol}://{base_uri}{bitbucket_repos[0]}/raw/{file_subpath}?at=refs%2Fheads%2F{default_branch}",
        f"{default_protocol}://{base_uri}{bitbucket_repos[2]}/raw/{file_subpath}?at=refs%2Fheads%2F{default_branch}",
        f"{default_protocol}://{base_uri}{bitbucket_repos[0]}/raw/{file_subpath}?at=refs%2Fheads%2F{default_branch}",
    ]
    assert len(results) == len(expected_results)
    for i, result in enumerate(results):
        assert result == expected_results[i]


def test_get_raw_file_uri(
    get_raw_file_uri,
    funtoo_stash_uris,
    github_uris,
    github_repos,
    bitbucket_repos,
    invalid_git_service_uri,
):
    file_subpath = "metadata/kit-info.json"
    with pytest.raises(hub.metarepo2json.errors.GitServiceError):
        get_raw_file_uri(invalid_git_service_uri, file_subpath)
    base_uris = [
        hub.OPT.metarepo2json.github_raw_netloc,
        hub.OPT.metarepo2json.funtoo_stash_raw_netloc,
    ]
    uris = [github_uris[0], funtoo_stash_uris[0]]
    default_protocol = hub.OPT.metarepo2json.net_protocol
    default_branch = hub.OPT.metarepo2json.branch
    commit = "86909d655f985270d9e38ca0e3022c7136dda945"
    expected_results = [
        f"{default_protocol}://{base_uris[0]}{github_repos[0]}/{default_branch}/{file_subpath}",
        f"{default_protocol}://{base_uris[1]}{bitbucket_repos[0]}/raw/{file_subpath}?at=refs%2Fheads%2F{default_branch}",
        f"{default_protocol}://{base_uris[0]}{github_repos[0]}/{commit}/{file_subpath}",
        f"{default_protocol}://{base_uris[1]}{bitbucket_repos[0]}/raw/{file_subpath}?at={commit}",
    ]
    results = [
        get_raw_file_uri(uris[0], file_subpath),
        get_raw_file_uri(uris[1], file_subpath),
        get_raw_file_uri(uris[0], file_subpath, commit=commit),
        get_raw_file_uri(uris[1], file_subpath, commit=commit),
    ]
    assert len(results) == len(expected_results)
    for i, result in enumerate(results):
        assert result == expected_results[i]


def test_is_metarepo_corrupted(is_metarepo_corrupted):
    invalid_kitinfo = {"a": 1}
    invalid_kitsha1 = {}
    valid_kitinfo = KIT_INFO
    valid_kitsha1 = KIT_SHA1
    assert is_metarepo_corrupted(invalid_kitinfo, invalid_kitsha1) is True
    assert is_metarepo_corrupted(valid_kitinfo, invalid_kitsha1) is True
    assert is_metarepo_corrupted(invalid_kitinfo, valid_kitsha1) is True
    assert is_metarepo_corrupted(valid_kitinfo, valid_kitsha1) is False


def test_sort_kits(sort_kits):
    key = "name"
    name_order = ["a", "b", "c"]
    unsorted_list = [{key: "b"}, {key: "a"}, {key: "c"}]
    sorted_list = sort_kits(unsorted_list, key, name_order)
    assert sorted_list[0]["name"] == name_order[0]
    assert sorted_list[1]["name"] == name_order[1]
    assert sorted_list[2]["name"] == name_order[2]
    name_order = ["c", "b", "a"]
    sorted_list = sort_kits(unsorted_list, key, name_order)
    assert sorted_list[0]["name"] == name_order[0]
    assert sorted_list[1]["name"] == name_order[1]
    assert sorted_list[2]["name"] == name_order[2]
