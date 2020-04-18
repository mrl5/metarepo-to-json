#!/usr/bin/env python3


from pathlib import Path, PurePath
from re import match
from urllib.parse import parse_qs, urlencode, urlparse


def get_kit(
    hub, kit_name: str, kit_settings: dict, branches: list, kitsha1: dict
) -> dict:
    b = list(
        map(
            lambda x: {
                "name": x,
                "catpkgs": [],
                "sha1": kitsha1[x],
                "stability": kit_settings["stability"][x],
            },
            branches,
        )
    )
    return {"name": kit_name, "branches": b, "type": kit_settings["type"]}


def get_raw_file_uri(hub, repo_uri, file_subpath, branch=None) -> str:
    default_protocol = hub.OPT.metarepo2json.net_protocol
    o = parse_uri(hub, repo_uri, default_protocol)
    supported_git_webservices = [
        {
            "is_valid": is_github(hub, o.netloc),
            "return_function": get_github_raw_file_uri,
        },
        {
            "is_valid": is_funtoo_stash(hub, o.netloc),
            "return_function": get_funtoo_stash_raw_file_uri,
        },
    ]
    try:
        fn = list(
            map(
                lambda x: x["return_function"],
                filter(lambda x: x["is_valid"] is True, supported_git_webservices),
            )
        ).pop()
        return fn(hub, repo_uri, file_subpath, branch)
    except IndexError:
        errmsg = f"Invalid Git service: {o.netloc}"
        raise hub.metarepo2json.errors.GitServiceError(errmsg)


def is_metarepo_corrupted(hub, kitinfo: dict, kitsha1: dict) -> bool:
    kitinfo_required_keys = [
        "kit_order",
        "kit_settings",
        "release_defs",
        "release_info",
    ]
    return (
        not all(list(map(lambda x: x in kitinfo.keys(), kitinfo_required_keys)))
        or not kitsha1
    )


def parse_uri(hub, uri, protocol=None):
    if protocol is None:
        protocol = hub.OPT.metarepo2json.net_protocol
    if not (match(r"^http[s]?://", uri)):
        uri = "//" + uri
    return urlparse(uri, protocol)


def normalize_net_path(hub, path):
    if not path.startswith("/"):
        path = Path("/").joinpath(path)
    return path


def throw_on_invalid_git_service(hub, validator, netloc: str):
    errmsg = "Invalid network location of Git service"
    if not validator(hub, netloc):
        raise hub.metarepo2json.errors.GitServiceError(errmsg)


def throw_on_invalid_github_path(hub, validator, path: str):
    errmsg = "Invalid path to the GitHub repository"
    if not validator(hub, path):
        raise hub.metarepo2json.errors.GitHubRepoURIError(errmsg)


def throw_on_invalid_funtoo_stash_path(hub, validator, path: str):
    errmsg = "Invalid path to the Funtoo Stash repository"
    if not validator(hub, path):
        raise hub.metarepo2json.errors.FuntooStashRepoURIError(errmsg)


def throw_on_github_tree(hub, validator, path: str):
    errmsg = "Tree (branch reference) in URI"
    if validator(hub, path):
        raise hub.metarepo2json.errors.GitHubRepoURIError(errmsg)


def throw_on_bitbucket_refs(hub, validator, query: str):
    errmsg = "Branch reference in URI"
    if validator(hub, query):
        raise hub.metarepo2json.errors.FuntooStashRepoURIError(errmsg)


def throw_on_corrupted_metarepo(hub, kitinfo, kitsha1):
    errmsg = "Corrupted meta-repo content"
    if is_metarepo_corrupted(hub, kitinfo, kitsha1):
        raise hub.metarepo2json.errors.CorruptedMetarepoError(errmsg)


def is_github(hub, netloc: str) -> bool:
    valid_netlocs = ["github.com", "www.github.com"]
    return netloc.split(":")[0] in valid_netlocs


def is_funtoo_stash(hub, netloc) -> bool:
    valid_netlocs = ["code.funtoo.org"]
    return netloc.split(":")[0] in valid_netlocs


def is_github_repo_given(hub, path: str) -> bool:
    parents_len = len(Path(path).parents)
    return parents_len == 2


def is_bitbucket_repo_given(hub, path) -> bool:
    parents_len = len(Path(path).parents)
    predictate = 6 if path.endswith("browse") else 5
    return parents_len == predictate


def is_github_tree_given(hub, path: str) -> bool:
    if len(path) == 0:
        return False
    return str(Path(path).parents[0]).endswith("tree")


def is_bitbucket_refs_given(hub, query) -> bool:
    if len(query) == 0:
        return False
    return "at" in parse_qs(query)


def get_github_raw_file_uri(hub, repo_uri: str, file_subpath: str, branch=None) -> str:
    base_uri = hub.OPT.metarepo2json.github_raw_netloc
    default_protocol = hub.OPT.metarepo2json.net_protocol
    branch = branch if branch is not None else hub.OPT.metarepo2json.metarepo_branch
    o = parse_uri(hub, repo_uri, default_protocol)
    throw_on_invalid_git_service(hub, is_github, o.netloc)
    throw_on_invalid_github_path(hub, is_github_repo_given, o.path)
    throw_on_github_tree(hub, is_github_tree_given, o.path)
    path = normalize_net_path(hub, o.path)
    return f"{default_protocol}://{base_uri}{path}/{branch}/{file_subpath}"


def get_funtoo_stash_raw_file_uri(hub, repo_uri, file_subpath, branch=None) -> str:
    base_uri = hub.OPT.metarepo2json.funtoo_stash_raw_netloc
    default_protocol = hub.OPT.metarepo2json.net_protocol
    branch = branch if branch is not None else hub.OPT.metarepo2json.metarepo_branch
    o = parse_uri(hub, repo_uri, default_protocol)
    throw_on_invalid_git_service(hub, is_funtoo_stash, o.netloc)
    throw_on_invalid_funtoo_stash_path(hub, is_bitbucket_repo_given, o.path)
    throw_on_bitbucket_refs(hub, is_bitbucket_refs_given, o.path)
    branch_anchor = {"at": [f"refs/heads/{branch}"]}
    qs = urlencode(branch_anchor, doseq=True)
    path = normalize_net_path(hub, o.path)
    if path.endswith("browse") is True:
        path = str(PurePath(path).parent)
    return f"{default_protocol}://{base_uri}{path}/raw/{file_subpath}?{qs}"


def sort_kits(hub, kits, kits_order):
    return list(
        map(
            lambda x: list(filter(lambda kit: kit["name"] == x, kits)).pop(), kits_order
        )
    )
