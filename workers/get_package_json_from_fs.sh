#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "$0" )" >/dev/null && pwd -P)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"
STYLESHEET="${PROJECT_DIR}/stylesheets/package.xslt"
EIX="/usr/bin/eix"
XSLTPROC="/usr/bin/xsltproc"
JQ="/usr/bin/jq"

print_help() {
    echo "$(tput bold)Usage:$(tput sgr0) $(basename "$0") package_name"
    echo ""
    echo "$(tput bold)Description:$(tput sgr0) this script will generate a JSON describing a package based on eix output"
    echo ""
}

check_input() {
    if [[ "$#" -eq 0 ]]; then
        print_help && exit 2
    elif [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
        print_help && exit
    fi
}

get_package_xml() {
    "${EIX}" -nv -x -e "$1" --xml
}

convert_xml_to_json() {
    "${XSLTPROC}" ${STYLESHEET} - | "${JQ}" -c '.'
}

# main()
check_input "$@" &&
    get_package_xml "$1" | convert_xml_to_json
