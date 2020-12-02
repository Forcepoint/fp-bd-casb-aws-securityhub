#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

readonly _dir="$(cd "$(dirname "${0}")" && pwd)"
source "${_dir}"/casb-siem-setup.sh

main() {
    cd "$(dirname "$(find "${_SIEM_HOME_DIR}" -path \*SIEMClient.sh)")"
    ./SIEMClient.sh \
        --credentials.file "${_CREDENTIALS_FILE}" \
        --host "${_HOST}" \
        --port "${_PORT}" \
        --output.dir "${_OUTPUT_DIR}" \
        truststorePath="${_TRUST_STORE_PATH}" \
        cefCompliance=true
}

main "$@"
