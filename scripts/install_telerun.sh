#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
   echo "Installing telerun"
   mkdir -p /opt/6106
   cp telerun/submit.py /opt/6106/submit.py
   ln -sf /opt/6106/submit.py /usr/bin/telerun
fi
