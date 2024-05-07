#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
   echo "Enter your telerun credentials"
   echo -n "Username: "
   read username
   echo -n "Token: "
   read token

   echo $'\nSaving credentials'
   mkdir -p /usr/local/.telerun
   echo $'{\n\t"username": "'$username$'",\n\t"token": "'$token$'"\n}' > /usr/local/.telerun/auth.json
fi
