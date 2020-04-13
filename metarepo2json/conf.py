CONFIG = {
    "metarepo_source": {"default": "fs", "help": "Meta-repo storage medium",},
    "metarepo_fs_location": {
        "default": "/var/git/meta-repo",
        "help": "Funtoo meta-repo default location in filesystem",
    },
    "metarepo_web_location": {
        "default": "https://github.com/funtoo/meta-repo",
        "help": "Funtoo meta-repo default location in web",
    },
    "metarepo_branch": {"default": "1.4-release", "help": "Funtoo meta-repo branch",},
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
    "metarepo_source": {
        "options": ["-s", "--metarepo-source"],
        "os": "METAREPO_SOURCE",
        "type": str,
    },
    "metarepo_fs_location": {
        "options": ["-fs", "--file-system"],
        "os": "METAREPO_FS",
        "type": str,
    },
    "metarepo_web_location": {
        "options": ["-w", "--web"],
        "os": "METAREPO_WEB",
        "type": str,
    },
    "metarepo_branch": {
        "options": ["-b", "--branch"],
        "os": "METAREPO_BRANCH",
        "type": str,
    },
}

DYNE = {"metarepo2json": ["metarepo2json"]}
