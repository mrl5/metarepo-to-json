#!/usr/bin/env python3


def __init__(hub):
    hub.pop.config.load(['metarepo2json'], 'metarepo2json')
    hub.pop.sub.load_subdirs(hub.metarepo2json, recurse=True)
