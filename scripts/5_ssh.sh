#!/bin/bash
set -e

EXTERNAL_IP=$(hostname -I)
printf "\033[01;33mCopy the following text. Press enter when you have copied it.\033[00m\n\n"
echo "Host 6172
    HostName ${EXTERNAL_IP}
    User ubuntu
"
read $COPIED
echo "Setup script completed"
