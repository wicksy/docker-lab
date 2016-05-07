.PHONY: build
newtag ?= latest
image = wicksy/wicksycv

build:
	docker build --no-cache=true -t "${image}:latest" .
	docker tag -f "${image}:latest" "${image}:${newtag}"
