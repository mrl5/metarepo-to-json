#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from os import path

from metarepo2json.config import CONFIG as conf

from .ikits import KitsInterface


class KitsFromFileSystem(KitsInterface):
    def __init__(self, metarepo_dir=conf["metarepo"]["DEFAULT_METAREPO_DIR"]):
        self.metarepo_dir = metarepo_dir
        self.kitinfo_path = path.join(
            self.metarepo_dir, conf["metarepo"]["KITINFO_SUBPATH"]
        )
        self.kitsha1_path = path.join(
            self.metarepo_dir, conf["metarepo"]["KITSHA1_SUBPATH"]
        )
        self.kitinfo = None
        self.kitsha1 = None
        self.kits = []

    def _load_data_source(self):
        with open(self.kitinfo_path) as f:
            self.kitinfo = json.load(f)
        with open(self.kitsha1_path) as f:
            self.kitsha1 = json.load(f)

    def _is_repo_structure_valid(self):
        is_valid = False
        try:
            is_valid = (
                path.isdir(path.join(self.metarepo_dir, ".git"))
                and path.isfile(self.kitinfo_path)
                and path.isfile(self.kitsha1_path)
                and path.isfile(
                    path.join(self.metarepo_dir, conf["metarepo"]["VERSION_SUBPATH"])
                )
            )
        except Exception:
            is_valid = False
        return is_valid

    def _is_repo_corrupted(self):
        is_corrupted = True
        try:
            self._load_data_source()
            is_corrupted = (
                conf["metarepo"]["RELEASES_KEY"] not in self.kitinfo or not self.kitsha1
            )
        except Exception:
            is_corrupted = True
        return is_corrupted

    def _get_kit_dict(self, kit, branches):
        b = list(
            map(
                lambda x: {"name": x, "catpkgs": [], "sha1": self.kitsha1[kit][x]},
                branches,
            )
        )
        return {"name": kit, "branches": b}

    def load_data_source(self):
        if not self._is_repo_structure_valid():
            raise self.InvalidMetarepoStructureError()
        if self._is_repo_corrupted():
            raise self.CorruptedMetarepoError()

    def get_kits_data(self):
        for kit, branches in self.kitinfo[conf["metarepo"]["RELEASES_KEY"]].items():
            self.kits.append(self._get_kit_dict(kit, branches))
        return self.kits

    class InvalidMetarepoStructureError(OSError):
        def __init__(self):
            self.strerror = "Invalid meta-repo structure"

    class CorruptedMetarepoError(KeyError):
        def __init__(self):
            self.strerror = "Corrupted meta-repo content"
