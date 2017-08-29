.PHONY: build

tagrepo = no
currenttag = $(shell semvertag latest)
newtag = $(shell semvertag bump patch)

containers = awscli base elasticsearch jre-7 nginx salt-master synology tiny-nginx

build:
ifeq ($(tagrepo),yes)
	@echo Tagging repo
	semvertag tag ${newtag}
else
	echo Not tagging repo
endif
	$(MAKE) -C base newtag=${newtag}
	$(MAKE) -C jre-7 newtag=${newtag}
	$(MAKE) -C jre-8 newtag=${newtag}
	$(MAKE) -C elasticsearch newtag=${newtag}
	$(MAKE) -C nginx newtag=${newtag}
	$(MAKE) -C salt-master newtag=${newtag}
	$(MAKE) -C awscli newtag=${newtag}
	$(MAKE) -C synology newtag=${newtag}
	$(MAKE) -C tiny-nginx newtag=${newtag}
	$(MAKE) -C wicksycv newtag=${newtag}

push:
	docker push wicksy/synology:${currenttag}
	docker push wicksy/synology:latest

clean:
	-docker kill `docker ps -aq`
	-docker rm -vf `docker ps -aq`
	-docker volume rm `docker volume ls -qf "dangling=true"`
	-docker rmi  -f `docker images -q -f "dangling=true"`

debug:
ifeq ($(tagrepo),yes)
	@echo Tagging repo
	@echo Current tag: ${currenttag}
	@echo New tag: ${newtag}
else
	@echo Not tagging repo
endif
