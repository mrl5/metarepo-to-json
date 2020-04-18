#!/usr/bin/env python3


def __init__(hub):
    global HUB
    HUB = hub


class InvalidStructureError(OSError):
    def __init__(self, msg):
        self.hub = HUB
        self.msg = msg


class CorruptedMetarepoError(KeyError):
    def __init__(self, msg):
        self.hub = HUB
        self.msg = msg


class CorruptedKitError(ValueError):
    def __init__(self, msg):
        self.hub = HUB
        self.msg = msg


class GitServiceError(ValueError):
    def __init__(self, msg):
        self.hub = HUB
        self.msg = msg


class GitHubRepoURIError(GitServiceError):
    def __init__(self, msg):
        self.hub = HUB
        self.msg = msg


class FuntooStashRepoURIError(GitServiceError):
    def __init__(self, msg):
        self.hub = HUB
        self.msg = msg
