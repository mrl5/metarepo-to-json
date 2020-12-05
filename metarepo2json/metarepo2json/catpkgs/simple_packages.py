#!/usr/bin/env python3


from os import walk
from pathlib import Path


def get_fs_packages(hub, path):
    get_ebuild_version = hub.metarepo2json.utils.get_ebuild_version
    get_ebuild_properties = hub.metarepo2json.utils.get_ebuild_properties
    get_package = hub.metarepo2json.utils.get_package
    tree = [d for d in walk(path)]
    packages = []
    for leafs in tree:
        if len(leafs) > 2:
            files = leafs[2]
            ebuilds = list(filter(lambda x: x.endswith(".ebuild"), files))
            if len(ebuilds) > 0:
                path = leafs[0]
                with open(Path(path).joinpath(ebuilds[0])) as f:
                    ebuild = f.read()
                catpkg_name = Path(path).name
                properties = get_ebuild_properties(ebuild)
                versions = list(
                    map(lambda x: get_ebuild_version(catpkg_name, x), ebuilds)
                )
                packages.append(
                    get_package(
                        catpkg_name,
                        versions,
                        description=properties["description"],
                        homepages=properties["homepages"],
                        licenses=properties["licenses"],
                    )
                )
    return packages
