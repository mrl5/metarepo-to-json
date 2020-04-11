#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "$0" )" >/dev/null && pwd -P)"
DEFAULT_METAREPO_DIR="/var/git/meta-repo"
JQ="/usr/bin/jq"
CAT="/bin/cat"

metarepo_dir="${DEFAULT_METAREPO_DIR}"
kit=""
kitdir=""
categories=""

print_help() {
    echo "$(tput bold)Usage:$(tput sgr0) $(basename "$0") -k kit"
    echo ""
    echo "$(tput bold)Description:$(tput sgr0) this script will generate a JSON describing categories in given kit"
    echo "Flags:"
    echo -e "\t-k|--kit name of kit"
    echo -e "\t-r|--meta-repo location of meta-repo (defaults to ${DEFAULT_METAREPO_DIR})"
    echo ""
}

check_input() {
    if [[ "$#" -eq 0 ]]; then
        print_help && exit 2
    elif [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
        print_help && exit
    fi
}

set_kit() {
    local errmsg=""
    kit="$1"
    kitdir="${metarepo_dir}/kits/${kit}"
    categories="${kitdir}/profiles/categories"
    if [ ! -d "${kitdir}" ]; then
        echo "Kit ${kit} not found. Aborting" && exit 1
    elif [ ! -f "${categories}" ]; then
        echo "Structure of kit ${kit} has invalid format. Aborting" && exit 1
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

process_wrong_syntax() {
    echo "Wrong syntax. Aborting"
    print_help
    exit 2
}

process_opts() {
    check_input "$@"
    while (( "$#" )); do
        case "$1" in
            -k|--kit)
                set_kit "$2"
                shift 2
                ;;
            -r|--meta-repo)
                set_metarepo_dir "$2"
                shift 2
                ;;
            *)
                process_wrong_syntax
                ;;
        esac
    done
}

get_categories_json() {
    "${CAT}" "${categories}" | "${JQ}" -cR '{name: ., packages: []}'
}

# main()
process_opts "$@" &&
    get_categories_json
