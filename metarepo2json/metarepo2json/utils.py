#!/usr/bin/env python3


from io import BytesIO
from pathlib import Path
from re import match
from urllib.parse import parse_qs, urlencode, urlparse

from git import Repo


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


def get_category(hub, category_name: str) -> dict:
    return {"name": category_name, "packages": []}


def get_package(hub, name: str, versions: list, **kwargs) -> dict:
    v = list(map(lambda x: {"version": x, "cpes": []}, versions))
    return {"name": name, "versions": v, **kwargs}


def get_raw_file_uri(hub, repo_uri, file_subpath, **kwargs) -> str:
    branch = kwargs["branch"] if "branch" in kwargs else hub.OPT.metarepo2json.branch
    commit = kwargs["commit"] if "commit" in kwargs else hub.OPT.metarepo2json.commit
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
        return fn(hub, repo_uri, file_subpath, branch=branch, commit=commit)
    except IndexError:
        errmsg = f"Invalid Git service: {o.netloc}"
        raise hub.metarepo2json.errors.GitServiceError(errmsg)


def get_fs_file_from_commit(hub, git_repo_path: str, commit: str, subpath: str) -> str:
    repo = Repo(git_repo_path)
    targetfile = repo.commit(commit).tree / subpath
    with BytesIO(targetfile.data_stream.read()) as f:
        return f.read().decode("utf-8")


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


def throw_on_corrupted_metarepo(hub, kitinfo: dict, kitsha1: dict):
    errmsg = "Corrupted meta-repo content"
    if is_metarepo_corrupted(hub, kitinfo, kitsha1):
        raise hub.metarepo2json.errors.CorruptedMetarepoError(errmsg)


def is_github(hub, netloc: str) -> bool:
    valid_netlocs = ["github.com", "www.github.com"]
    return netloc.split(":")[0] in valid_netlocs


def is_github_api_blob(hub, uri) -> bool:
    o = parse_uri(hub, uri)
    return o.netloc.split(":")[0] == "api.github.com" and "/git/blobs/" in o.path


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


def get_github_raw_file_uri(hub, repo_uri: str, file_subpath: str, **kwargs) -> str:
    base_uri = hub.OPT.metarepo2json.github_raw_netloc
    default_protocol = hub.OPT.metarepo2json.net_protocol
    branch = kwargs["branch"] if "branch" in kwargs else hub.OPT.metarepo2json.branch
    commit = kwargs["commit"] if "commit" in kwargs else hub.OPT.metarepo2json.commit
    o = parse_uri(hub, repo_uri, default_protocol)
    throw_on_invalid_git_service(hub, is_github, o.netloc)
    throw_on_invalid_github_path(hub, is_github_repo_given, o.path)
    throw_on_github_tree(hub, is_github_tree_given, o.path)
    path = normalize_net_path(hub, o.path)
    ref = branch if commit is None else commit
    return f"{default_protocol}://{base_uri}{path}/{ref}/{file_subpath}"


def get_funtoo_stash_raw_file_uri(hub, repo_uri, file_subpath, **kwargs) -> str:
    base_uri = hub.OPT.metarepo2json.funtoo_stash_raw_netloc
    default_protocol = hub.OPT.metarepo2json.net_protocol
    branch = kwargs["branch"] if "branch" in kwargs else hub.OPT.metarepo2json.branch
    commit = kwargs["commit"] if "commit" in kwargs else hub.OPT.metarepo2json.commit
    o = parse_uri(hub, repo_uri, default_protocol)
    throw_on_invalid_git_service(hub, is_funtoo_stash, o.netloc)
    throw_on_invalid_funtoo_stash_path(hub, is_bitbucket_repo_given, o.path)
    throw_on_bitbucket_refs(hub, is_bitbucket_refs_given, o.path)
    ref = {"at": [f"refs/heads/{branch}" if commit is None else commit]}
    qs = urlencode(ref, doseq=True)
    path = normalize_net_path(hub, o.path)
    if path.endswith("browse") is True:
        path = str(Path(path).parent)
    return f"{default_protocol}://{base_uri}{path}/raw/{file_subpath}?{qs}"


def get_github_tree_uri(hub, repo_uri: str, **kwargs) -> str:
    base_uri = hub.OPT.metarepo2json.github_api_netloc
    default_protocol = hub.OPT.metarepo2json.net_protocol
    branch = kwargs["branch"] if "branch" in kwargs else hub.OPT.metarepo2json.branch
    commit = kwargs["commit"] if "commit" in kwargs else hub.OPT.metarepo2json.commit
    o = parse_uri(hub, repo_uri, default_protocol)
    throw_on_invalid_git_service(hub, is_github, o.netloc)
    throw_on_invalid_github_path(hub, is_github_repo_given, o.path)
    throw_on_github_tree(hub, is_github_tree_given, o.path)
    path = normalize_net_path(hub, o.path)
    ref = branch if commit is None else commit
    return f"{default_protocol}://{base_uri}/repos{path}/git/trees/{ref}"


def get_funtoo_stash_tree_uri(hub, repo_uri: str, **kwargs) -> str:
    base_uri = hub.OPT.metarepo2json.funtoo_stash_api_netloc
    default_protocol = hub.OPT.metarepo2json.net_protocol
    branch = kwargs["branch"] if "branch" in kwargs else hub.OPT.metarepo2json.branch
    commit = kwargs["commit"] if "commit" in kwargs else hub.OPT.metarepo2json.commit
    o = parse_uri(hub, repo_uri, default_protocol)
    throw_on_invalid_git_service(hub, is_funtoo_stash, o.netloc)
    throw_on_invalid_funtoo_stash_path(hub, is_bitbucket_repo_given, o.path)
    throw_on_bitbucket_refs(hub, is_bitbucket_refs_given, o.path)
    path = normalize_net_path(hub, o.path)
    ref = {"at": [f"refs/heads/{branch}" if commit is None else commit]}
    qs = urlencode(ref, doseq=True)
    path = normalize_net_path(hub, o.path)
    if path.endswith("browse") is True:
        path = str(Path(path).parent)
    path = str(Path(path).relative_to("/bitbucket"))
    return f"{default_protocol}://{base_uri}/bitbucket/rest/api/1.0/{path}/browse?{qs}"


def get_ebuild_version(hub, ebuild: str) -> str:
    return match(r"([A-Za-z0-9_+]+-)+([0-9a-z-._]+)(\.ebuild)", ebuild).group(2)


def get_ebuild_properties(hub, ebuild: list) -> dict:
    var_to_dict = hub.metarepo2json.utils.var_to_dict
    dict_list = list(
        map(
            lambda x: var_to_dict(x),
            filter(
                lambda x: match("DESCRIPTION=", x)
                or match("HOMEPAGE=", x)
                or match("LICENSE=", x),
                ebuild.splitlines(),
            ),
        )
    )
    properties = {k: v for d in dict_list for k, v in d.items()}
    description = (
        properties["DESCRIPTION"] if "DESCRIPTION" in properties else None
    )
    homepages = (
        properties["HOMEPAGE"].split(" ") if "HOMEPAGE" in properties else None
    )
    licenses = (
        list(
            filter(
                lambda x: not match(r"(\|\||\(|\)|^$)", x),
                properties["LICENSE"].split(" "),
            )
        )
        if "LICENSE" in properties
        else None
    )
    return {"description": description, "homepages": homepages, "licenses": licenses}


def sort_list_of_dicts_by_key_values(hub, dicts: list, key: str, order: list) -> list:
    return list(map(lambda x: list(filter(lambda d: d[key] == x, dicts)).pop(), order))


def var_to_dict(hub, var: str) -> dict:
    a_list = var.split('#')[0].strip().replace('"', "").split("=")
    i = iter(a_list)
    return dict(zip(i, i))


def get_coroutine_results(hub, tasks: set) -> list:
    results = []
    for task in tasks:
        results.append(task.result())
    return results
