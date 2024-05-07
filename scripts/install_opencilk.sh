#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
  opencilk_url="http://6.172.scripts.mit.edu/opencilk_6106.tar.gz"
  echo "Installing OpenCilk"
  mkdir -p /opt/6106/opencilk
  rm -rf /opt/6106/opencilk/*
  curl -L $opencilk_url | tar -zxv --strip-components=1 -C /opt/6106/opencilk

  ln -sf /opt/6106/opencilk/bin/clang /usr/bin/clang-6106
fi
