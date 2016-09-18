## Docker Lab

#### Overview
Set of docker images based on Alpine Linux to keep container footprint nice and small

#### Build Status
**Develop branch** (https://travis-ci.org/wicksy/docker-lab.svg?branch=develop)</br>
**Master branch** (https://travis-ci.org/wicksy/docker-lab.svg?branch=master)</br>

#### Images

- base - Image upon which other images can be based

- nginx - HTTPD nginx service

- jre-7 - OpenJDK 7 (no GUI support)

- elasticsearch - Elasticsearch plus plugins

- tiny-nginx - Small footprint nginx

- salt-master - SaltStack Master/Minion to allow testing/development of new SLS, pillar data, config changes, etc

- awscli - Small environment to run AWS cli

- synology - Container used to run tasks on my Synology NAS (DS415plus) running Docker

- wicksycv - Container for my CV project (https://github.com/wicksy/CV)
