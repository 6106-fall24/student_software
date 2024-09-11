#!/bin/bash
set -e

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
mkdir -p "$HOME/.telerun"
echo $'{\n\t"username": "'$USERNAME$'",\n\t"token": "'$TOKEN$'"\n}' > "$HOME/.telerun/auth.json"
