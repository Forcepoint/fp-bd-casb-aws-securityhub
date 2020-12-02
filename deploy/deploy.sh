#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

readonly _dir="$(cd "$(dirname "${0}")" && pwd)"
readonly _deploy_siem="${1:-true}"

main() {
    cd "${_dir}"
    sudo cp ./casb-siem-aws-securityhub-batch.service /etc/systemd/system
    sudo cp ./casb-siem-aws-securityhub-batch.timer /etc/systemd/system
    sudo cp ./casb-siem-aws-securityhub.service /etc/systemd/system
    sudo systemctl daemon-reload
    sudo systemctl start casb-siem-aws-securityhub-batch.service casb-siem-aws-securityhub-batch.timer casb-siem-aws-securityhub.service
    sudo systemctl enable casb-siem-aws-securityhub-batch.service casb-siem-aws-securityhub-batch.timer casb-siem-aws-securityhub.service
    echo "casb-siem-aws processes deployed"
    if test "${_deploy_siem}" = true; then
        sudo cp ./casb-siem-batch.service /etc/systemd/system
        sudo cp ./casb-siem-batch-timer.service /etc/systemd/system
        sudo systemctl daemon-reload
        sudo systemctl start casb-siem-batch.service casb-siem-batch-timer.service
        sudo systemctl enable casb-siem-batch.service casb-siem-batch-timer.service
        echo "SIEM tool deployed"
    fi
    ./status.sh
}

main "$@"
