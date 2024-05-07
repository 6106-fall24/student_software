#!/bin/bash

# This script also lives at https://6172-fall20-public.s3.amazonaws.com/setup-nix.sh
# Thus, students can access it without first having to configure GitHub keys on their VM.
# Please make sure to also upload the latest version there by running `make upload-setup-nix`

set -e

if [[ ! -x $(command -v aws) ]]; then
    "aws not found. Please download and install the AWS CLI from https://aws.amazon.com/cli/ and then re-run this script."
    exit 1
fi

AMI_ID="ami-090b3f63bd13e1100"
PRIVATE_KEY_PATH="$HOME/.ssh/id_rsa"
PUBLIC_KEY_PATH="${PRIVATE_KEY_PATH}.pub"
TIMESTAMP="$(date '+%s')"
KEY_PAIR_NAME="6172-key-${TIMESTAMP}"
SECURITY_GROUP_NAME="6172-security-group"

mkdir -p "$HOME/.ssh"

if [[ ! -f "${PUBLIC_KEY_PATH}" ]]; then
    echo "Creating an SSH key"
    ssh-keygen -t rsa -q -f ${PRIVATE_KEY_PATH} -N ""
fi

echo "Importing your default SSH key into AWS EC2"
aws ec2 import-key-pair --key-name ${KEY_PAIR_NAME} --public-key-material "fileb://${PUBLIC_KEY_PATH}"

echo "Allowing SSH traffic on the default security group"
aws ec2 authorize-security-group-ingress --group-name default --protocol tcp --port 22 --cidr 0.0.0.0/0 || true
aws ec2 authorize-security-group-ingress --group-name default --ip-permissions IpProtocol=tcp,FromPort=22,ToPort=22,Ipv6Ranges=[{CidrIpv6=::/0}] || true


echo "Creating the AWS EC2 instance"
INSTANCE_ID=$(aws ec2 run-instances --image-id ${AMI_ID} --instance-type t2.small --key-name ${KEY_PAIR_NAME}  --output text --query 'Instances[].InstanceId')
echo "Created instance ${INSTANCE_ID}"

echo "Allocating an elastic ip address"
ALLOCATION_ID_AND_IP=$(aws ec2 allocate-address --output text --query '[AllocationId,PublicIp]')
ALLOCATION_ID=$(echo $ALLOCATION_ID_AND_IP | awk '{print $1;}')
ELASTIC_IP=$(echo $ALLOCATION_ID_AND_IP | awk '{print $2;}')
echo "Allocation ${ALLOCATION_ID} has IP ${ELASTIC_IP}"

echo "Waiting for instance to transition to running state"
while true; do
    STATE=$(aws ec2 describe-instance-status --instance-ids $INSTANCE_ID --output text --query 'InstanceStatuses[].InstanceState.Name')
    if [[ "$STATE" == "running" ]]; then
        echo "Instance is in running state; continuing"
        break
    fi
done


echo "Assocating IP address ${ELASTIC_IP} with instance ${INSTANCE_ID}"
aws ec2 associate-address --allocation-id ${ALLOCATION_ID} --instance-id ${INSTANCE_ID}

echo "Configuring SSH Config"
echo "Host 6172
    HostName ${ELASTIC_IP}
    User ubuntu
" >> "$HOME/.ssh/config"

echo 'Wait a few minutes for your 6172 Virtual Machine to provision. You can then connect to it via `ssh 6172`.'
