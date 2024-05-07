#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
  opencilk_url="https://www.dropbox.com/scl/fi/fcxg1y6yf3ca3ic0ihfuo/opencilk-2.1.0-x86_64-linux-no-avx-v2.tar.gz?rlkey=9o348wgv8459np8vmbz7bppyo&st=q2385gge&dl=1"
  echo "Installing OpenCilk"
  mkdir -p /opt/6106/opencilk
  rm -rf /opt/6106/opencilk/*
  curl -L $opencilk_url | tar -zxv --strip-components=1 -C /opt/6106/opencilk

  ln -sf /opt/6106/opencilk/bin/clang /usr/bin/clang-6106
fi
