
#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
    awsrun_source_link="https://dl.cloudsmith.io/public/mit-6-172/6-172/deb/ubuntu/pool/bionic/main/p/py/python3-awsrun_1.0.18-1_all.deb"
    deb_file="/tmp/awsrun.deb"

    echo "Downloading awsrun"

    curl $awsrun_source_link --output $deb_file

    echo "Installing awsrun"

    dpkg -i $deb_file

    rm $deb_file
fi
