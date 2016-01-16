.PHONY: build

currenttag = $(shell semvertag latest)
newtag = $(shell semvertag bump patch)

containers = awscli base elasticsearch jre-7 nginx salt-master synology tiny-nginx

build:
	semvertag tag ${newtag}
	$(MAKE) -C awscli newtag=${newtag}
	$(MAKE) -C base newtag=${newtag}
	$(MAKE) -C elasticsearch newtag=${newtag}
	$(MAKE) -C jre-7 newtag=${newtag}
	$(MAKE) -C nginx newtag=${newtag}
	$(MAKE) -C salt-master newtag=${newtag}
	$(MAKE) -C synology newtag=${newtag}
	$(MAKE) -C tiny-nginx newtag=${newtag}

push:
	docker push wicksy/synology:${currenttag}
	docker push wicksy/synology:latest

