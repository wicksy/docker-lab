.PHONY: build
newtag ?= latest
image = wicksy/synology

build:
	docker build --no-cache=true -t "${image}:latest" .
	docker tag -f "${image}:latest" "${image}:${newtag}"
