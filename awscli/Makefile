.PHONY: build
newtag ?= latest
image = wicksy/awscli

build:
	docker build --no-cache=true -t "${image}:latest" .
	docker tag -f "${image}:latest" "${image}:${newtag}"
