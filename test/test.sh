#!/bin/bash

arg="${1}"

set -e
set -u
set -o pipefail

error() {
  echo "===> Error on line ${1}"
  echo "===> Cleaning up..."
  docker kill $(docker ps -q)
  docker rm -fv $(docker ps -q)
}

cleanup() {
  if [[ "$(docker ps -q | wc -l)" -gt 0 ]] ; then
    echo "===> Cleaning up..."
    docker kill $(docker ps -q)
    docker rm -fv $(docker ps -q)
  fi
}

if [[ "${arg}" == "boot2docker" ]] ; then
  testhost="$(docker-machine ip docker-vm)"
  echo "===> Running tests against ports mapped to docker-machine..."
elif [[ "$(uname | tr '[:upper:]' '[:lower:]')" == "darwin" ]] ; then
  testhost="$(docker-machine ip docker-vm)"
  echo "===> Running on OSX (using docker-machine address)..."
else
  testhost="localhost"
  echo "===> Running tests against ports mapped to localhost..."
fi

trap 'error $LINENO' ERR
cleanup

echo "===> Starting daemon images..."
docker run -d -p 80:80 -p 443:443 wicksy/nginx:latest
docker run -d -p 8080:80 wicksy/tiny-nginx:latest
docker run -d -p 9200:9200 wicksy/elasticsearch:latest
echo "===> Waiting for init..."
sleep 10

echo "===> Testing nginx..."
echo "===> HTTP..."
curl --progress-bar "http://${testhost}" \
  | grep 'Welcome to a Docker Nginx Demo'
echo "===> HTTPS..."
curl --insecure --progress-bar "https://${testhost}" \
  | grep 'Welcome to a Docker Nginx Demo'
echo "===> Image nginx passed..."

echo "===> Testing tiny-nginx..."
curl --progress-bar "http://${testhost}:8080" \
  | grep 'Welcome to nginx!'
echo "===> Image tiny-nginx passed..."

echo "===> Testing elasticsearch..."
echo "===> Waiting extra for init..."
sleep 10
curl --progress-bar "http://${testhost}:9200" \
  | grep 'cluster_name.*elasticdocker'
echo "===> Image elasticsearch passed..."

echo "===> Testing non-daemon images..."

echo "===> Testing awscli..."
docker run wicksy/awscli:latest aws --version
echo "===> Image awscli passed..."

#echo "===> Testing salt-master..."
#docker run wicksy/salt-master:latest salt --version
#docker run wicksy/salt-master:latest salt-master --version
#docker run wicksy/salt-master:latest salt-minion --version
#docker run wicksy/salt-master:latest salt-call --version
#echo "===> Image salt-master passed..."

echo "===> Testing jre-7..."
docker run wicksy/jre-7:latest java -version 2>&1 \
  | grep '^java version.*1\.7\.'
echo "===> Image jre-7 passed..."
echo "===> Testing jre-8..."
docker run wicksy/jre-8:latest java -version 2>&1 \
  | grep '^openjdk version.*1\.8\.'
echo "===> Image jre-8 passed..."

echo "===> Testing synology..."
docker run wicksy/synology:latest file -b /scripts/synology-task-wrapper.py \
  | grep 'Python'
echo "===> Image synology passed..."

echo "===> Testing wicksycv..."
docker run wicksy/wicksycv:latest mkdocs --version 2>&1 \
  | grep '^mkdocs.*version'
echo "===> Image wicksycv passed..."

echo "===> Testing base..."
for tools in python pip wget curl gpg
do
  docker run wicksy/base:latest ${tools} --version
done
docker run wicksy/base:latest openssl version
echo "===> Image base passed..."

echo "===> Image testing complete..."
cleanup
exit 0
