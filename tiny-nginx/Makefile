.PHONY: build
newtag ?= latest
image = wicksy/tiny-nginx

build:
	docker build --no-cache=true -t "${image}:latest" .
	docker tag "${image}:latest" "${image}:${newtag}"
