#!/usr/bin/env python3

import json
from urllib.parse import urlparse
from tests.mocks.kit_info import KIT_INFO
from tests.mocks.kit_sha1 import KIT_SHA1
from tests.mocks.categories import CATEGORIES


async def stub_get_page(uri, session):
    o = urlparse(uri)
    if o.path.endswith("kit-info.json"):
        return json.dumps(KIT_INFO)
    if o.path.endswith("kit-sha1.json"):
        return json.dumps(KIT_SHA1)
    if o.path.endswith("categories"):
        return "\n".join(CATEGORIES)
