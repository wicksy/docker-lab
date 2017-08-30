.PHONY: build
newtag ?= latest
image = wicksy/jre-8

build:
	docker build --no-cache=true -t "${image}:latest" .
	docker tag "${image}:latest" "${image}:${newtag}"
