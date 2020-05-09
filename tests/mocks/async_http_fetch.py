#!/usr/bin/env python3

import json
from pathlib import Path
from urllib.parse import urlparse

from tests.mocks.categories import CATEGORIES
from tests.mocks.kit_info import KIT_INFO
from tests.mocks.kit_sha1 import KIT_SHA1

file_path = Path(__file__).resolve()
api_mocks = file_path.parent.joinpath("apis")
ebuilds_mocks = file_path.parent.joinpath("ebuilds")


async def stub_get_page(uri, session, **kwargs):
    o = urlparse(uri)
    if o.path.endswith("kit-info.json"):
        return json.dumps(KIT_INFO)
    if o.path.endswith("kit-sha1.json"):
        return json.dumps(KIT_SHA1)
    if o.path.endswith("categories"):
        return "\n".join(CATEGORIES)
    if o.path.endswith("firefox-72.0.2.ebuild"):
        with open(ebuilds_mocks / "firefox-72.0.2.ebuild") as f:
            result = f.read()
        return result
    if o.netloc == "api.github.com":
        return github_api_stub(o, **kwargs)
    if o.netloc == "code.funtoo.org":
        return funtoo_stash_api_stub(o, **kwargs)


def github_api_stub(o, **kwargs):
    headers = kwargs["headers"] if "headers" in kwargs else None
    if o.path.endswith("/5932b921ba48f44e9c19d19301ae9448bb3fd912"):
        with open(
            api_mocks / "github_5932b921ba48f44e9c19d19301ae9448bb3fd912.json"
        ) as f:
            result = f.read()
        return result
    if o.path.endswith("/04eb725f50c46031116df312c634eb767ba1b718"):
        with open(
            api_mocks / "github_04eb725f50c46031116df312c634eb767ba1b718.json"
        ) as f:
            result = f.read()
        return result
    if o.path.endswith("/ba2ec9cdda1ab7d29185777d5d9f7b2488ae7390"):
        with open(
            api_mocks / "github_ba2ec9cdda1ab7d29185777d5d9f7b2488ae7390.json"
        ) as f:
            result = f.read()
        return result
    if o.path.endswith("/789bfa81a335ab23accbd0da7d0808b499227510"):
        if headers is not None and headers["accept"] == "application/vnd.github.v3.raw":
            with open(ebuilds_mocks / "firefox-72.0.2.ebuild") as f:
                result = f.read()
        else:
            with open(
                api_mocks / "github_789bfa81a335ab23accbd0da7d0808b499227510.json"
            ) as f:
                result = f.read()
        return result
    raise ValueError("unsupported path")


def funtoo_stash_api_stub(o, **kwargs):
    if o.query.endswith("=5932b921ba48f44e9c19d19301ae9448bb3fd912"):
        with open(
            api_mocks / "funtoo_stash_5932b921ba48f44e9c19d19301ae9448bb3fd912.json"
        ) as f:
            result = f.read()
        return result
    if o.query.endswith("=04eb725f50c46031116df312c634eb767ba1b718"):
        with open(
            api_mocks / "funtoo_stash_04eb725f50c46031116df312c634eb767ba1b718.json"
        ) as f:
            result = f.read()
        return result
    if o.query.endswith("=ba2ec9cdda1ab7d29185777d5d9f7b2488ae7390"):
        with open(
            api_mocks / "funtoo_stash_ba2ec9cdda1ab7d29185777d5d9f7b2488ae7390.json"
        ) as f:
            result = f.read()
        return result
    raise ValueError("unsupported path")
