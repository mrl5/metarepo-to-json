#!/usr/bin/env python3

import json
from urllib.parse import urlparse
from tests.mocks.metadata.kit_info import KIT_INFO
from tests.mocks.metadata.kit_sha1 import KIT_SHA1


async def stub_get_page(uri, session):
    o = urlparse(uri)
    if o.path.endswith("kit-info.json"):
        return json.dumps(KIT_INFO)
    if o.path.endswith("kit-sha1.json"):
        return json.dumps(KIT_SHA1)
