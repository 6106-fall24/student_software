#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0 "$@"
else
   USERNAME=
   TOKEN=

   if [ $# -eq 2 ]; then
      USERNAME="$1"
      TOKEN="$2"
   else
      echo "Enter your telerun credentials"
      echo -n "Username: "
      read USERNAME
      echo -n "Token: "
      read TOKEN
   fi

   echo $'\nSaving credentials'
   mkdir -p ~/.telerun
   echo $'{\n\t"username": "'$USERNAME$'",\n\t"token": "'$TOKEN$'"\n}' > ~/.telerun/auth.json
fi
