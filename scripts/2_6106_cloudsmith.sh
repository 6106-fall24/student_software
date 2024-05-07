#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
   apt-get install -y debian-keyring  # debian only
   apt-get install -y debian-archive-keyring  # debian only
   apt-get install -y apt-transport-https
   keyring_location=/usr/share/keyrings/mit-6-172-6-172-archive-keyring.gpg
   curl -1sLf 'https://dl.cloudsmith.io/public/mit-6-172/6-172/cfg/gpg/gpg.133FB930C31B3E08.key' |  gpg --dearmor > ${keyring_location}
   curl -1sLf 'https://dl.cloudsmith.io/public/mit-6-172/6-172/cfg/setup/config.deb.txt?distro=ubuntu&codename=bionic' > /etc/apt/sources.list.d/mit-6-172-6-172.list

   echo "Updating the package list"
   apt update

   echo "Installing 6.106 Packages"
   apt install -y 6172-metapackage
fi
