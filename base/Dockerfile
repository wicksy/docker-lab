FROM alpine:latest

RUN apk update && \
    apk add python && \
    apk add py-pip && \
    apk add wget && \
    apk add curl && \
    apk add supervisor && \
    apk add gnupg && \
    pip install --upgrade pip && \
    pip install awscli

RUN wget --no-check-certificate -O /usr/bin/confd https://github.com/kelseyhightower/confd/releases/download/v0.11.0/confd-0.11.0-linux-amd64 && \
    chmod a+x /usr/bin/confd && \
    mkdir -p /etc/confd/conf.d && \
    mkdir -p /etc/confd/templates && \
    mkdir -p /etc/supervisor.d && \
    mv /etc/supervisord.conf /etc/supervisord.conf.sample

RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4


RUN curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.7/gosu-amd64" && \
    curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.7/gosu-amd64.asc" && \
    gpg --verify /usr/local/bin/gosu.asc && \
    rm /usr/local/bin/gosu.asc && \
    chmod +x /usr/local/bin/gosu

ADD docker/conf/supervisord.conf /etc/supervisord.conf
ADD docker/supervisor.d /etc/supervisor.d

RUN chmod -R +x /etc/supervisor.d/

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
