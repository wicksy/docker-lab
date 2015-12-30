image = wicksy/tiny-nginx
newtag ?= latest

build:
	docker build -t "${image}:latest" .
	docker tag -f "${image}:latest" "${image}:${newtag}"
