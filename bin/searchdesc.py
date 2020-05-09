#!/usr/bin/env python3

import json
import sys
from re import IGNORECASE, match

import pop.hub

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="metarepo2json", omit_class=False)

get_fs_packages = hub.metarepo2json.catpkgs.simple_packages.get_fs_packages


if __name__ == "__main__":
    if hub.OPT.metarepo2json.searchdesc is None:
        sys.exit("Provide search phrase")
    keyword = hub.OPT.metarepo2json.searchdesc
    metarepo = hub.OPT.metarepo2json.repo_fs
    packages = get_fs_packages(metarepo)
    print(
        json.dumps(
            list(
                filter(
                    lambda x: match(rf"{keyword}", x["name"], IGNORECASE)
                    or (
                        x["description"] is not None
                        and match(rf"{keyword}", x["description"], IGNORECASE)
                    ),
                    packages,
                )
            )
        )
    )
