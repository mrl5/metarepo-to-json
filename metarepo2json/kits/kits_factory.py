#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .kits_fs import KitsFromFileSystem


def get_kits_instance(kit="fskit"):
    """ factory design pattern """
    kits = {"fskit": KitsFromFileSystem()}
    return kits[kit]
