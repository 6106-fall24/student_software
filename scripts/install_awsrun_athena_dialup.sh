
#!/bin/bash
set -e

python3 -m pip install boto3

awsrun_source_link="https://dl.cloudsmith.io/public/mit-6-172/6-172/deb/ubuntu/pool/bionic/main/p/py/python3-awsrun_1.0.18-1_all.deb"
deb_file="/tmp/awsrun.deb"

echo "Downloading awsrun"

curl $awsrun_source_link --output $deb_file

echo "Installing awsrun"

install_dir=/tmp/awsrun
rm -rf $install_dir
mkdir $install_dir

dpkg -x $deb_file $install_dir
cp -r $install_dir/usr/bin/* $HOME/.local/bin/
cp -r $install_dir/usr/lib/python3/dist-packages/* $HOME/.local/lib/python3.10/site-packages

echo "export PATH=\$PATH:$HOME/.local/bin" >> $HOME/.bashrc

rm $deb_file
rm -r $install_dir
