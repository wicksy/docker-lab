FROM wicksy/base:latest

RUN echo "http://nl.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories && \
    echo "http://nl.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && \
    echo "http://nl.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

RUN apk update && \
    apk upgrade musl && \
    apk add libzmq  && \
    apk add gcc && \
    apk add build-base && \
    apk add python3-dev && \
    apk add openssl && \
    apk add salt && \
    apk add salt-minion && \
    apk add salt-master && \
    pip3 install --upgrade pip && \
    pip3 install pyyaml && \
    pip3 install tornado && \
    pip3 install jinja2 && \
    pip3 install pyzmq && \
    pip3 install pycrypto && \
    pip3 install msgpack-pure

RUN mkdir -p /etc/salt /srv/salt/salt-formulas /srv/pillar

RUN /bin/echo -e "tcp_keepalive_idle: 300\ntcp_keepalive: True\n" >> /etc/salt/minion

ADD docker/salt/base /srv/salt/base
ADD docker/salt/top.sls /srv/salt/top.sls

ADD docker/supervisor.d /etc/supervisor.d
RUN chmod -R +x /etc/supervisor.d/

ADD docker/confd /etc/confd
