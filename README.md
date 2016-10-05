[![Build Status](https://travis-ci.org/wicksy/docker-lab.svg?branch=master)](https://travis-ci.org/wicksy/docker-lab) [![license](https://img.shields.io/badge/License-MIT-blue.svg?maxAge=2592000)](https://github.com/wicksy/docker-lab/blob/master/LICENSE.md)</br>

## Docker Lab

### Overview

![Docker logo](logos/docker.png "Docker")
![Alpine Linux logo](logos/alpine.png "Alpine")

Set of docker images based on Alpine Linux to keep container footprint nice and small (compared to say those base on Ubuntu
or Phusion).

```
➜  docker-lab git:(develop) ✗ docker images | grep 'wicksy.*latest'
wicksy/tiny-nginx                   latest              8053e9f01c7f        39 hours ago        6.883 MB
wicksy/synology                     latest              e8f7fd730b36        39 hours ago        157.2 MB
wicksy/awscli                       latest              7042b9febfa2        39 hours ago        93.82 MB
wicksy/salt-master                  latest              8434b0593fa7        39 hours ago        386.5 MB
wicksy/nginx                        latest              8c200d0d8169        39 hours ago        116.9 MB
wicksy/elasticsearch                latest              049b9d863a3e        39 hours ago        266.6 MB
wicksy/jre-7                        latest              f391546816cd        39 hours ago        231.2 MB
wicksy/base                         latest              e852ff80927a        40 hours ago        115.2 MB
➜  docker-lab git:(develop) ✗
```

### Requirements

* Docker (tested on version 1.6+)
* [semvertag](https://github.com/wicksy/semvertag)

### Images

#### base

The base image is designed to be an image others can be built on (using the `FROM` directive). Contains some useful
tooling (python+pip, wget, curl, gpg, awscli). Also includes [confd](https://github.com/kelseyhightower/confd) for configuration
file templating, [gosu](https://github.com/tianon/gosu/) for lightweight sudo-like capabilities and [supervisord](http://supervisord.org/)
for lightweight init-like process management.

#### nginx

Simple out-of-the-box nginx HTTPD service. Map a volume into `/var/lib/nginx/html` to serve content.

```
➜  ~ echo "Hello World" > ~/tmp/index.html
➜  ~ docker run -d -p 80:80 -v /Users/wicksy/tmp/:/var/lib/nginx/html wicksy/nginx:latest
e63ccbf47b199e64e2e39483801128075efb8180b5d9b676f43811298adbd811
➜  ~ curl "http://$(docker-machine ip docker-vm)"
Hello World
➜  ~
```

#### jre-7

Image with OpenJDK 7 (no GUI support) to be used to build containers requiring Java (e.g. Elasticsearch).

```
➜  ~ docker run wicksy/jre-7:latest java -version
java version "1.7.0_91"
OpenJDK Runtime Environment (IcedTea 2.6.3) (Alpine 7.91.2.6.3-r2)
OpenJDK 64-Bit Server VM (build 24.91-b01, mixed mode)
➜  ~
```

#### elasticsearch

Elasticsearch plus plugins.

```
➜  ~ docker run -d -p 9200:9200 wicksy/elasticsearch:latest
e950e6ed6a6408670e3e0faabba8022b5989eb3fcf1ed66cfd1294fca42cd245
➜  ~ curl "http://$(docker-machine ip docker-vm):9200"
{
  "name" : "Xi'an Chi Xan",
  "cluster_name" : "elasticdocker",
  "version" : {
    "number" : "2.1.1",
    "build_hash" : "40e2c53a6b6c2972b3d13846e450e66f4375bd71",
    "build_timestamp" : "2015-12-15T13:05:55Z",
    "build_snapshot" : false,
    "lucene_version" : "5.3.1"
  },
  "tagline" : "You Know, for Search"
}
➜  ~
```

#### tiny-nginx

Very small footprint nginx (currently < 10MB).

```
➜  ~ docker run -d -p 80:80 -v /Users/wicksy/tmp/:/var/lib/nginx/html wicksy/tiny-nginx:latest
35b84901f65e287960e772d4c01efc34ac23a0c81bff0f5d98fec025362d5b70
➜  ~ curl "http://$(docker-machine ip docker-vm)"
Hello World
➜  ~
```

#### salt-master

SaltStack Master/Minion to allow testing/development of new SLS, pillar data, config changes, reactors, mining, etc.

```
➜  ~ docker run -d --name=saltmaster wicksy/salt-master:latest
ec910d9bfbc2f2337dbac87264770327087f86faba82c67f3dd1fe8bc0da3e59
➜  ~ docker exec -it $(docker ps -q -f name="saltmaster") sh -o vi
/ # salt-call --local state.highstate
[WARNING ] Error loading grains, unexpected linux_gpu_data output, check that you have a valid shell configured and permissions to run lspci command
[WARNING ] /usr/lib/python2.7/site-packages/salt/grains/core.py:1493: DeprecationWarning: The "osmajorrelease" will be a type of an integer.

[WARNING ] State for file: /tmp/tempfile - Neither 'source' nor 'contents' nor 'contents_pillar' nor 'contents_grains' was defined, yet 'replace' was set to 'True'. As there is no source to replace the file with, 'replace' has been set to 'False' to avoid reading the file unnecessarily.
local:
----------
          ID: base_files
    Function: file.managed
        Name: /tmp/tempfile
      Result: True
     Comment: Empty file
     Started: 17:44:22.626546
    Duration: 6.065 ms
     Changes:
              ----------
              new:
                  file /tmp/tempfile created

Summary for local
------------
Succeeded: 1 (changed=1)
Failed:    0
------------
Total states run:     1
Total run time:   6.065 ms
/ #
```

#### awscli

Small environment to run AWS cli tools.

```
➜  ~ docker run wicksy/awscli:latest aws --version
aws-cli/1.10.66 Python/2.7.12 Linux/4.4.17-boot2docker botocore/1.4.56
➜  ~
```

#### synology

Image that is used to run tasks on my Synology NAS (DS415plus) running Docker that contains additional tooling
(vim, groff, git, openssh-client, pips (including awscli, boto, boto3)) as well as a task wrapper designed
to run particular tasks on the NAS.

The task wrapper (`/scripts/synology-task-wrapper.py`) works against a number of shell variables that can be
injected into the running container:

```
DSM_PRIVATE_KEY         Private (SSH) key used to pull from repos (usually just secrets) - OPTIONAL
DSM_WORKSPACE           Directory designed as a workspace e.g. where git repos will be pulled into - OPTIONAL
DSM_GIT_SECRETREPO      URL of git repository containing secrets e.g. keys - OPTIONAL
DSM_GIT_CODEREPO        URL of git repository containing tasks that can be run - OPTIONAL
DSM_TASK_EXECUTE        Task to execute (pulled in via git) - MANDATORY
```

The task wrapper is designed to pull in code to execute from another repository (e.g. on Github) but could also
be used to execute local tasks built into the container image.

#### wicksycv

Image for my [CV project](https://github.com/wicksy/CV).

### Branches

As well as `master` there is currently a `develop` branch for ongoing feature development.

### Builds

Image builds are triggered automatically and run on [Travis CI](https://travis-ci.org/wicksy/docker-lab/builds).

To build locally:

```
$ make buld
```

By default `build` will not bump the version tag on the repository. To bump the tag as well:

```
$ make build tagrepo=yes
```

To clean up old dangling images, dangling volumes, exited containers and kill all running containers:

```
$ make clean
```

### Tests

Post build tests are also run on Travis CI using the `test/test.sh` bash script.

```
==> Starting daemon images...
62ad1042e4b0e5756f1f6f99fa726d049b24990298fc697c58dbfe1d24083d56
03cdc1f8f2374d4bb322d6b690cb265644535cfdfbc455102b2c2d51c9c15663
518d929769c92a5eee8a0ccc33907a55378eb405a5a70834cff8c7d80442db59
===> Waiting for init...
===> Testing nginx...
######################################################################## 100.0%
<title>Welcome to nginx!</title>
<h1>Welcome to nginx!</h1>
===> Image nginx passed...
===> Testing tiny-nginx...
######################################################################## 100.0%
<title>Welcome to nginx!</title>
<h1>Welcome to nginx!</h1>
===> Image tiny-nginx passed...
===> Testing elasticsearch...
===> Waiting extra for init...
######################################################################## 100.0%
  "cluster_name" : "elasticdocker",
===> Image elasticsearch passed...
===> Testing non-daemon images...
===> Testing awscli...
aws-cli/1.10.66 Python/2.7.12 Linux/4.4.17-boot2docker botocore/1.4.56
===> Image awscli passed...
.
.
.
.
.
===> Image base passed...
===> Image testing complete...
===> Cleaning up...
518d929769c9
03cdc1f8f237
62ad1042e4b0
➜  docker-lab git:(develop) ✗
```
