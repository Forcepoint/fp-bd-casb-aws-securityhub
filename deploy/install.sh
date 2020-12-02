#!/usr/bin/env bash

readonly _dir="$(cd "$(dirname "${0}")" && pwd)"
readonly _home_folder="$(cd "${_dir}/.." && pwd)"

install_prerequisite_centos() {
    echo "install_prerequisite_centos"
    sudo yum update -y
    sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm
    sudo yum install -y python36u epel-release python-pip java-1.8.0-openjdk unzip
}

install_prerequisite_debian() {
    echo "install_prerequisite_debian"
    sleep 5
    sudo apt update
    sudo apt install -y python3-pip python3-venv openjdk-8-jdk
}

# this only made to cater for centos7 and ubuntu18
main() {
    hostnamectl | grep -qi centos && install_prerequisite_centos || install_prerequisite_debian
    sudo -H pip3 install -U pipenv
    sudo chmod ugo+rw "${_home_folder}"/*.json
    sudo chmod +x "${_dir}"/*.sh
}

main "$@"
