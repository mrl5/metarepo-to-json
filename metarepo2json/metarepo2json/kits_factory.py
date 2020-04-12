#!/usr/bin/env python3


def get_kits_instance(hub, kit="fskit"):
    """ factory design pattern """
    kits = {
        "fskit": hub.metarepo2json.kits_fs.KitsFromFileSystem()
    }
    return kits[kit]
