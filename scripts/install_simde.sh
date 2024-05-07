#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
  simde_url="https://github.com/simd-everywhere/simde/releases/download/v0.8.0/simde-amalgamated-0.8.0.tar.xz"
  simde_dirname="simde-amalgamated-0.8.0"

  echo "Downloading SIMDE"

  curl -L $simde_url | tar -Jxv --strip-components=1 -C /usr/include/ $simde_dirname/x86
fi
