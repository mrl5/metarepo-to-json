CONFIG = {
    "metarepo_dir": {
        "default": "/var/git/meta-repo",
        "help": "Funtoo meta-repo default location"
    },
    "kitinfo_subpath": {
        "default": "metadata/kit-info.json",
        "help": "kit-info.json default relative location in meta-repo"
    },
    "kitsha1_subpath": {
        "default": "metadata/kit-sha1.json",
        "help": "kit-sha1.json default relative location in meta-repo"
    },
    "version_subpath": {
        "default": "metadata/version.json",
        "help": "version.json default relative location in meta-repo"
    },
    "releases_key": {
        "default": "release_defs",
        "help": "key where kit releases are stored in kit-info.json"
    }
}

DYNE = {'metarepo2json': ['metarepo2json']}
