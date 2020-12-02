#!/usr/bin/env bash

readonly _conf_file_name=cfg.json
readonly _dir="$(cd "$(dirname "${0}")" && pwd)"
readonly _home_dir="$(cd "${_dir}/.." && pwd)"/"${_HOME_DIR_NAME}"

main() {
    if [ ! -z ${CONFIG_FILE_URL_LOCATION} ]; then
        wget -O "${_home_dir}"/"${_conf_file_name}" "${CONFIG_FILE_URL_LOCATION}"
    fi
    echo -e "*/30\t*\t*\t*\t*\t"${_home_dir}"/src/modules/main_siem_watcher_batch.py" >>/etc/crontabs/root
    crond -b -l 0
    "${_home_dir}"/src/modules/main_siem_watcher_stream.py
}

main "$@"
