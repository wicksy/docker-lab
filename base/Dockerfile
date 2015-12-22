FROM alpine:latest

RUN apk update && \
    apk add python && \
    apk add py-pip && \
    apk add wget && \
    apk add curl && \
    apk add supervisor && \
    pip install --upgrade pip && \
    pip install awscli

RUN wget -O /usr/bin/confd https://github.com/kelseyhightower/confd/releases/download/v0.11.0/confd-0.11.0-linux-amd64 && \
    chmod a+x /usr/bin/confd && \
    mkdir -p /etc/confd/conf.d && \
    mkdir -p /etc/confd/templates && \
    mkdir -p /etc/supervisor.d && \
    mv /etc/supervisord.conf /etc/supervisord.conf.sample

ADD docker/conf/supervisord.conf /etc/supervisord.conf
ADD docker/supervisor.d /etc/supervisor.d

RUN chmod -R +x /etc/supervisor.d/

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
