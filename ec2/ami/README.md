# AMI

The student AMI containing OpenCilk is built using packer.
For simplicity, the Makefile runs Packer inside Docker, so you will
need Docker to run the Makefile.

## How to Build
1. Copy `vars.template.json` to `vars.json` and populate your amazon IAM credentials
1. `make build`
