[![Build Status](https://travis-ci.org/wicksy/docker-lab.svg?branch=master)](https://travis-ci.org/wicksy/docker-lab) [![license](https://img.shields.io/badge/License-MIT-blue.svg?maxAge=2592000)](https://github.com/wicksy/docker-lab/blob/master/LICENSE.md)</br>

## Docker Lab

### Overview

![Docker logo](logos/docker.png "Docker")
![Alpine Linux logo](logos/alpine.png "Alpine")

Set of docker images based on Alpine Linux to keep container footprint nice and small (compared to say those base on Ubuntu
or Phusion).

```
➜  docker-lab git:(develop) ✗ docker images | grep 'wicksy.*latest'
wicksy/elasticsearch   latest              e32ef61087c3        4 days ago          241MB
wicksy/jre-8           latest              0a0ea0f78810        4 days ago          200MB
wicksy/base            latest              db6c5a5487f2        4 days ago          130MB
wicksy/wicksycv        latest              daf799569e61        7 days ago          145MB
wicksy/tiny-nginx      latest              26e3feb7b398        7 days ago          6.44MB
wicksy/synology        latest              5af77d266511        7 days ago          173MB
wicksy/awscli          latest              e83974b207fc        7 days ago          103MB
wicksy/salt-master     latest              c55968b52f21        7 days ago          422MB
wicksy/nginx           latest              b957dba4f7d6        7 days ago          131MB
wicksy/jre-7           latest              8ec61574bf91        7 days ago          245MB
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

HTTPD service based on [nginx](https://nginx.org/en/). Templated configuration file to define an application root and index.

Environment variables for the container:

```
NGINX_INDEX - set a custom index document, defaults to 'index.html' if unset
NGINX_ROOT  - set a custom root path, defaults to '/app/public' if unset
NGINX_SSL_FORCE_REDIRECT - if set then container will redirect all http traffic to https
```

Using the built in /app/public/index.html:

```
➜  ~ docker run -d -p 80:80 wicksy/nginx:latest
5ab8af2b85de4c77b09d8b91e383bb1c176fdfd4ab5e506380bd3acfe4abf014
➜  ~ curl "http://$(docker-machine ip docker-vm)"
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Hello World</title>
    </head>
    <body>
        <div class="page-header" align=center>
          <h1>Welcome to a Docker Nginx Demo</h1>
        </div>
        <div class="container" align=center>
          <h3>Hello World</h3>
        </div>
    </body>
</html>
➜  ~
```

Example of mapping in a volume (with content) to a different document root and index document:

```
➜  ~ echo "Hello World" > ~/tmp/hello.html
➜  ~ docker run -d -p 80:80 --env NGINX_ROOT=/var/lib/nginx/html --env NGINX_INDEX=hello.html -v /Users/wicksy/tmp/:/var/lib/nginx/html wicksy/nginx:latest
e63ccbf47b199e64e2e39483801128075efb8180b5d9b676f43811298adbd811
➜  ~ curl "http://$(docker-machine ip docker-vm)"
Hello World
➜  ~
```

Sample docker-compose file:

```
➜  ~ cat docker-compose.yml
# Demo docker-compose file for nginx

nginx:
  image: wicksy/nginx:latest
  ports:
    - 80:80
    - 443:443
  environment:
    - NGINX_ROOT=/var/lib/nginx/html
    - NGINX_INDEX=index.html

➜  ~ docker-compose up -d
Creating nginx_nginx_1
➜  ~ curl "http://$(docker-machine ip docker-vm)"
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
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

#### jre-8

Image with OpenJDK 8 (no GUI support) to be used to build containers requiring Java (e.g. Elasticsearch).

```
➜  ~ docker run wicksy/jre-8:latest java -version
openjdk version "1.8.0_131"
OpenJDK Runtime Environment (IcedTea 3.4.0) (Alpine 8.131.11-r2)
OpenJDK 64-Bit Server VM (build 25.131-b11, mixed mode)
➜  ~
```

#### elasticsearch

Elasticsearch plus plugins.

```
➜  ~ docker run -d -p 9200:9200 wicksy/elasticsearch:latest
e950e6ed6a6408670e3e0faabba8022b5989eb3fcf1ed66cfd1294fca42cd245
➜  ~ curl "http://$(docker-machine ip docker-vm):9200"
{
  "name" : "C8KJrVa",
  "cluster_name" : "elasticdocker",
  "cluster_uuid" : "6CtmpzGLR22xzSkz2_Zlwg",
  "version" : {
    "number" : "5.5.2",
    "build_hash" : "b2f0c09",
    "build_date" : "2017-08-14T12:33:14.154Z",
    "build_snapshot" : false,
    "lucene_version" : "6.6.0"
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
$ make build
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
ubuntu@Dell-Inspiron:/srv/docker-lab$ test/test.sh
===> Running tests against ports mapped to localhost...
===> Cleaning up...
54b219cda212
===> Starting daemon images...
27c818eccd8df9292a75a3b4c46fa54cc54ec3b9f291e65348b88df83e669a5d
b83cc453a234d76d13b9f795ead164665c4f990e4a74456f782bacc2d0b4aa63
66543beb5a555f1a3b6a42473dd79f5218a6891a140e231eb895de6121f9446d
===> Waiting for init...
===> Testing nginx...
===> HTTP...
######################################################################## 100.0%
          <h1>Welcome to a Docker Nginx Demo</h1>
===> HTTPS...
######################################################################## 100.0%
          <h1>Welcome to a Docker Nginx Demo</h1>
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
aws-cli/1.11.141 Python/2.7.13 Linux/4.4.0-92-generic botocore/1.6.8
===> Image awscli passed...
.
.
.
.
.
===> Image testing complete...
===> Cleaning up...
66543beb5a55
b83cc453a234
27c818eccd8d
ubuntu@Dell-Inspiron:/srv/docker-lab$
```
