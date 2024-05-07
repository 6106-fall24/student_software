#!/bin/sh

# This script is used to run VSCode on Athena VDI
# You cannot run VSCode normally there because the home directory is on AFS
# VSCode tries to create a UNIX socket in the home directoy
# UNIX Sockets are not supported on AFS
# https://github.com/microsoft/vscode/issues/102952

# This should either be added to the class locker
# Another option is to add it somewhere on the student locker
# and add that location to the PATH

vscode_runtime_dir="/var/tmp/vscode-runtime-dir-6106"
mkdir -p $vscode_runtime_dir

export XDG_RUNTIME_DIR=$vscode_runtime_dir
exec /usr/bin/code --extensions-dir $vscode_runtime_dir "$@"