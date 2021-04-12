#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

readonly _dir="$(cd "$(dirname "${0}")" && pwd)"
readonly _home_folder="$(cd "${_dir}/.." && pwd)"
readonly _deploy_siem_tool="${1:-true}"

validate_prerequisites() {
    local __r=0
    local __prerequisites=("$@")
    local __clear_previous_display="\r\033[K"
    for prerequisite in "${__prerequisites[@]}"; do
        echo -en "${__clear_previous_display}Prerequisite - ${prerequisite} - check" && sleep 0.1
        command -v ${prerequisite} >/dev/null 2>&1 || {
            echo -e "${__clear_previous_display}We require >>> ${prerequisite} <<< but it's not installed. Please try again after installing ${prerequisite}." &&
                __r=1 &&
                break
        }
    done
    echo -en "${__clear_previous_display}"
    return "${__r}"
}

setup_systemd_home_dir() {
    local -r __systemd_file="${1}"
    local -r __home_dir="${2}"
    local -r __home_dir_variable_name="${3}"
    local -r __user="${4}"
    local __r=1
    local __content="$(awk '{gsub(/Environment=.*$/,"Environment='"${__home_dir_variable_name}"'='"${__home_dir}"'")}1' "${__systemd_file}")"
    echo "${__content}" >"${__systemd_file}" && __r=0
    __content="$(awk '{gsub(/WorkingDirectory=.*$/,"WorkingDirectory='"${__home_dir}"'")}1' "${__systemd_file}")"
    echo "${__content}" >"${__systemd_file}" && __r=0
    __content="$(awk '{gsub(/User=.*$/,"User='"${__user}"'")}1' "${__systemd_file}")"
    echo "${__content}" >"${__systemd_file}" && __r=0
    return "${__r}"
}

main() {
    cd "${_dir}"
    local __prerequisites=(python3.8 java pipenv systemctl)
    local __home_dir_variable_name="APP_HOME"
    local __config_file="${_home_folder}"/cfg.json
    local -r __user="$(whoami)"
    validate_prerequisites "${__prerequisites[@]}"
    sudo chown -R "${__user}" "${_home_folder}"
    sudo chmod +x "${_home_folder}"/src/modules/main_siem_watcher_batch.py "${_home_folder}"/src/modules/main_siem_watcher_stream.py
    sudo chmod ugo+rw "${_dir}"/*.service
    cd "${_home_folder}" && pipenv install
    for _sysd_file in "${_dir}"/*.service; do
        setup_systemd_home_dir "${_sysd_file}" "${_home_folder}" "${__home_dir_variable_name}" "${__user}"
    done
    cd "${_dir}" && ./deploy.sh ${_deploy_siem_tool}
}

main "$@"
