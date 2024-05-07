#!/bin/athena/bash
# set -e

echo "Running for Athena VDI."
echo "Copying repo into /tmp to be able to run setup as root"
rm -rf /tmp/student_software
cp -r $(dirname $0)/.. /tmp/student_software

echo "Starting 6.172 setup"

su root -c "/tmp/student_software/scripts/1_prerequs.sh"
# su root -c "/tmp/student_software/scripts//2_6172_cloudsmith.sh"
su root -c "/tmp/student_software/scripts/3_6172.sh"
$(dirname $0)/../scripts/4_aws.sh
su root -c "/tmp/student_software/scripts/6_install_vscode.sh"
su root -c "/tmp/student_software/scripts/7_install_awsrun.sh"

echo "Adding 6.172 locker to PATH"
echo "add 6.172" >> ~/.bashrc

rm -rf /tmp/student_software