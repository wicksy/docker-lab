.PHONY: build
newtag ?= latest
image = wicksy/elasticsearch

build:
	docker build --no-cache=true -t "${image}:latest" .
	docker tag "${image}:latest" "${image}:${newtag}"
