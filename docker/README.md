# Docker for 6.106

## High Level Instructions

1. `make build` to build 6.106 docker image.

2. `make run` to create a container from image.

Specify `IMAGE_NAME` to name the docker image (`6106` by default). For example:

```
make build IMAGE_NAME=6106
make run IMAGE_NAME=6106
```

To mount a local directory to a docker container, specify `MOUNT_DIR` as an absolute path.

```
make run MOUNT_DIR=/path/to/directory
```
