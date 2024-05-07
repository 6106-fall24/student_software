.PHONY: all
all: build

.PHONY: validate
validate:
	docker run --rm -v $(realpath $(shell pwd)/../../):/student_software -w /student_software/ec2/ami hashicorp/packer validate student.json

.PHONY: build
build:
	docker run --rm -v $(realpath $(shell pwd)/../../):/student_software -w /student_software/ec2/ami hashicorp/packer build -var-file vars.json student.json

AMI_ID?=""
.PHONY: vmdk-s3
vmdk-s3:
	aws ec2 export-image --image-id $(AMI_ID) --disk-image-format VMDK --s3-export-location S3Bucket=6172-public,S3Prefix=/

EXPORT_ID?=""
.PHONY: vmdk-s3-status
vmdk-s3-status:
	aws ec2 describe-export-image-tasks --export-image-task-ids $(EXPORT_ID)
