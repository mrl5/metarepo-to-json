CONFIG = {
    "output_dir": {
        "default": "metarepo_dump",
        "help": "Directory where output files will be written",
    },
    "data_source": {"default": "fs", "help": "Storage medium"},
    "repo_fs": {"default": "/var/git/meta-repo", "help": "Location in filesystem"},
    "kit": {"default": "core-kit", "help": "Kit name"},
    "repo_web": {
        "default": "https://github.com/funtoo/meta-repo",
        "help": "Location in web",
    },
    "branch": {"default": "1.4-release", "help": "Git branch"},
    "commit": {"default": None, "help": "Git commit SHA1"},
    "category": {"default": None, "help": "Kit category (e.g. www-client)"},
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
    "kits_subpath": {"default": "kits", "help": "default kits filesystem subpath"},
    "categories_subpath": {
        "default": "profiles/categories",
        "help": "default categories file with kit categories list",
    },
    "net_protocol": {"default": "https", "help": "network protocol"},
    "github_raw_netloc": {
        "default": "raw.githubusercontent.com",
        "help": "urllib netloc for GitHub repo raw files",
    },
    "github_api_netloc": {
        "default": "api.github.com",
        "help": "urllib netloc for GitHub API",
    },
    "funtoo_stash_raw_netloc": {
        "default": "code.funtoo.org",
        "help": "urllib netloc for Funtoo Stash a.k.a Bitbucket repo raw files",
    },
    "funtoo_stash_api_netloc": {
        "default": "code.funtoo.org",
        "help": "urllib netloc for Funtoo Stash a.k.a Bitbucket API",
    },
    "searchdesc": {
        "default": None,
        "help": "Keyword for searching by package name or package description",
    },
}

CLI_CONFIG = {
    "output_dir": {"options": ["-o", "--output-dir"], "os": "OUTPUT_DIR", "type": str,},
    "data_source": {"options": ["-s", "--source"], "os": "DATA_SOURCE", "type": str},
    "kit": {"options": ["-k", "--kit"], "os": "KIT", "type": str},
    "repo_fs": {
        "options": ["-fs", "--file-system"],
        "os": "FS_LOCATION",
        "type": str,
        "nargs": "?",
        "positional": True,
    },
    "repo_web": {"options": ["-w", "--web"], "os": "WEB_LOCATION", "type": str},
    "branch": {"options": ["-b"], "os": "BRANCH", "type": str},
    "commit": {"options": ["-c"], "os": "COMMIT", "type": str},
    "category": {"options": [], "os": "CATEGORY", "type": str},
    "searchdesc": {},
}

DYNE = {"metarepo2json": ["metarepo2json"]}
