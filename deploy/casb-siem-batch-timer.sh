#!/usr/bin/env bash

main() {
    while true; do
        sleep 60
        systemctl is-active casb-siem-batch.service | grep -qw "^active$" || systemctl restart casb-siem-batch.service
    done
}

main "$@"
