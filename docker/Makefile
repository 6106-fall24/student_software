IMAGE_NAME=6106
MOUNT_DIR=

.PHONY: all
all: build

.PHONY: build
build:
	docker build -t $(IMAGE_NAME) -f Dockerfile ..

.PHONY: run
run:
	docker run $(if $(MOUNT_DIR), -v $(MOUNT_DIR):/6106) -it $(IMAGE_NAME)
