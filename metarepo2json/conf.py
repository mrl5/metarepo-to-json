CONFIG = {
    "data_source": {"default": "fs", "help": "Storage medium",},
    "repo_fs": {
        "default": "/var/git/meta-repo",
        "help": "Location in filesystem",
    },
    "repo_web": {
        "default": "https://github.com/funtoo/meta-repo",
        "help": "Location in web",
    },
    "branch": {"default": "1.4-release", "help": "Git branch",},
    "commit": {"default": None, "help": "Git commit SHA1",},
    "kitinfo_subpath": {
        "default": "metadata/kit-info.json",
        "help": "kit-info.json default relative location in meta-repo",
    },
    "kitsha1_subpath": {
        "default": "metadata/kit-sha1.json",
        "help": "kit-sha1.json default relative location in meta-repo",
    },
    "version_subpath": {
        "default": "metadata/version.json",
        "help": "version.json default relative location in meta-repo",
    },
    "kits_subpath": {"default": "kits", "help": "default kits filesystem subpath",},
    "categories_subpath": {
        "default": "profiles/categories",
        "help": "default categories file with kit categories list",
    },
    "net_protocol": {"default": "https", "help": "network protocol"},
    "github_raw_netloc": {
        "default": "raw.githubusercontent.com",
        "help": "urllib netloc for github repo raw files",
    },
    "funtoo_stash_raw_netloc": {
        "default": "code.funtoo.org",
        "help": "urllib netloc for Funtoo Stash a.k.a Bitbucket repo raw files",
    },
}

CLI_CONFIG = {
    "data_source": {
        "options": ["-s", "--source"],
        "os": "DATA_SOURCE",
        "type": str,
    },
    "repo_fs": {
        "options": ["-fs", "--file-system"],
        "os": "FS_LOCATION",
        "type": str,
        "nargs": "?",
        "positional": True,
    },
    "repo_web": {
        "options": ["-w", "--web"],
        "os": "WEB_LOCATION",
        "type": str,
    },
    "branch": {
        "options": ["-b"],
        "os": "BRANCH",
        "type": str,
    },
    "commit": {
        "options": ["-c"],
        "os": "COMMIT",
        "type": str,
    },
}

DYNE = {"metarepo2json": ["metarepo2json"]}
