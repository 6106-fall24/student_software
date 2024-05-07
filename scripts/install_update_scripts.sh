#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
   mkdir -p /opt/6106

   echo "Creating symlink update-clang-6106"
   cp scripts/install_opencilk.sh /opt/6106/update-clang-6106.sh
   ln -sf /opt/6106/update-clang-6106.sh /usr/bin/update-clang-6106

   echo "Creating symlink update-telerun"
   cp scripts/install_telerun.sh /opt/6106/update-telerun.sh
   ln -sf /opt/6106/update-telerun.sh /usr/bin/update-telerun

   echo "Creating symlink authorize-telerun"
   cp scripts/authorize_telerun.sh /opt/6106/authorize-telerun.sh
   ln -sf /opt/6106/authorize-telerun.sh /usr/bin/authorize-telerun
fi
