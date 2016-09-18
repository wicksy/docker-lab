.PHONY: build
newtag ?= latest
image = wicksy/wicksycv

build:
	docker build --no-cache=true -t "${image}:latest" .
	docker tag "${image}:latest" "${image}:${newtag}"

testbuild:
	docker build -t "${image}:testing" .
