#!/usr/bin/env python3

import aiohttp
import logging
import sys

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("http_fetcher")
logging.getLogger("chardet.charsetprober").disabled = True


async def fetch_html(hub, url: str, session: aiohttp.ClientSession, **kwargs) -> str:
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    logger.debug(f"Got response [{resp.status}] for URL: {url}")
    return await resp.text()
