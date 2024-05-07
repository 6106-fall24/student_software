#!/bin/bash
set -e

$(dirname $0)/../scripts/1_prerequs.sh
$(dirname $0)/../scripts/2_6172_cloudsmith.sh
$(dirname $0)/../scripts/3_6172.sh
$(dirname $0)/../scripts/4_aws.sh
$(dirname $0)/../scripts/5_ssh.sh