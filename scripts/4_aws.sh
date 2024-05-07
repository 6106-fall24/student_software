#!/bin/bash
set -e

echo "Adding Configuration for AWS"

# For now, we are using a shared IAM credential that does not have any significant permissions
AWS_ACCESS_KEY=""
AWS_SECRET_ACCESS_KEY=""

mkdir -p ~/.aws

touch ~/.aws/config
chmod 600 ~/.aws/config

echo "[default]
region = us-east-1" > ~/.aws/config

touch ~/.aws/credentials
chmod 600 ~/.aws/credentials

echo "[default]
aws_access_key_id = ${AWS_ACCESS_KEY}
aws_secret_access_key = ${AWS_SECRET_ACCESS_KEY}" > ~/.aws/credentials
