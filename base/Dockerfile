FROM alpine:latest

RUN apk update && \
    apk add python && \
    apk add py-pip && \
    apk add wget && \
    apk add curl && \
    pip install --upgrade pip && \
    pip install awscli

# confd
RUN wget -O /usr/bin/confd https://github.com/kelseyhightower/confd/releases/download/v0.11.0/confd-0.11.0-linux-amd64 && \
    chmod a+x /usr/bin/confd && \
    mkdir -p /etc/confd/conf.d && \
    mkdir -p /etc/confd/templates
