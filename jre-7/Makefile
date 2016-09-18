.PHONY: build
newtag ?= latest
image = wicksy/jre-7

build:
	docker build --no-cache=true -t "${image}:latest" .
	docker tag "${image}:latest" "${image}:${newtag}"
