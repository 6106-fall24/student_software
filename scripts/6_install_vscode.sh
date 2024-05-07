#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
    redirect_source_link="https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64"
    deb_file="/tmp/vscode_installation.deb"

    echo "Downloading VSCode"

    curl $redirect_source_link --output $deb_file -L

    echo "Installing VSCode"

    dpkg -i $deb_file

    rm $deb_file
fi
