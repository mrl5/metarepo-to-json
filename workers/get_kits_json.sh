#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "$0" )" >/dev/null && pwd -P)"
DEFAULT_METAREPO_DIR="/var/git/meta-repo"
JQ="/usr/bin/jq"

metarepo_dir="${DEFAULT_METAREPO_DIR}"
kitinfo="${metarepo_dir}/metadata/kit-info.json"

print_help() {
    echo "$(tput bold)Usage:$(tput sgr0) $(basename "$0") metarepo_dir"
    echo ""
    echo "$(tput bold)Description:$(tput sgr0) this script will generate a JSON describing metarepo kits"
    echo "\n if no args then ${DEFAULT_METAREPO_DIR} is used"
}

check_input() {
    if [[ "$#" -gt 1 ]]; then
        print_help && exit 2
    elif [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
        print_help && exit
    fi
}

exitOnMalformedRepo() {
    local repo="${metarepo_dir}"
    local gitdir="${repo}/.git"
    local version="${repo}/metadata/version.json"
    local predictate_key="release_defs"
    local errmsg="Looks like ${repo} is not a metarepo dir. Aborting"

    if [ ! -d "${gitdir}" ] || [ ! -f ${kitinfo} ] || [ ! -f ${version} ]; then
        echo ${errmsg} && exit 1
    fi

    "${JQ}" -cre ".${predictate_key}" "${kitinfo}" >/dev/null
    if [ $? -ne 0 ]; then
        echo ${errmsg} && exit 1
    fi
}

set_metarepo_dir() {
    if [[ "$#" -eq 1 ]]; then
        metarepo_dir="$1"
    fi
    if [ ! -d "${metarepo_dir}" ]; then
        echo "${metarepo_dir} not found. Aborting" && exit 1
    fi
}

get_kits_json() {
    "${JQ}" -c '.release_defs | to_entries[] |
        {name: .key, branches: [.value | to_entries[] |
            {name: .value, catpkgs: []}]}' \
        "${kitinfo}"
}

# main()
check_input "$@" &&
    set_metarepo_dir "$@" &&
    exitOnMalformedRepo &&
    get_kits_json
