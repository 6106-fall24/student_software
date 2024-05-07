#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
   echo "Installing prerequisites"
   apt-get update
   apt-get install -y --no-install-recommends \
      sudo \
      curl \
      debian-keyring  \
      debian-archive-keyring   \
      apt-transport-https \
      gnupg \
      ca-certificates \
      libc-dev \
      build-essential \
      libx11-dev \
      libxext-dev \
      git \
      python-is-python3 \
      python3-boto3 \
      valgrind \
      linux-tools-common \
      linux-tools-generic \
      ubuntu-desktop \
      gnome-panel \
      gnome-settings-daemon \
      metacity \
      nautilus \
      network-manager \
      gnome-terminal \
      gdb \
      openssh-server \
      llvm
   
   add-apt-repository ppa:ubuntu-toolchain-r/test
   apt upgrade -y libstdc++6

   if ! perf --version; then
      # fix for perf on OrbStack
      echo "Creating symlink for perf"
      
      sudo rm /usr/bin/perf

      perf_path=$(find /usr/lib/linux-tools/ -name perf -executable -print -quit)
      if [ -z "$perf_path" ]; then
         echo "perf not found in linux-tools"
         exit 1
      fi

      sudo ln -s "$perf_path" /usr/bin/perf

   fi
fi

