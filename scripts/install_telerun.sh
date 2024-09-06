#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
   telerun_url="https://raw.githubusercontent.com/6106-fall24/student_software/main/telerun/submit.py"
   echo "Installing telerun"
   mkdir -p /opt/6106
   curl -O --output-dir /opt/6106 $telerun_url
   chmod +x /opt/6106/submit.py
   ln -sf /opt/6106/submit.py /usr/bin/telerun
fi
