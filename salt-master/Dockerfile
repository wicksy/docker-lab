FROM wicksy/base:latest

RUN echo "http://nl.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

RUN apk update && \
    apk add libzmq  && \
    apk add gcc && \
    apk add build-base && \
    apk add python-dev && \
    apk add salt && \
    pip install --upgrade pip && \
    pip install pyyaml && \
    pip install tornado && \
    pip install jinja2 && \
    pip install pyzmq && \
    pip install pycrypto && \
    pip install msgpack-pure

RUN /bin/echo -e "tcp_keepalive_idle: 300\ntcp_keepalive: True\n" >> /etc/salt/minion

RUN mkdir -p /srv/salt/_libs/base /srv/salt/salt-formulas /srv/pillar

ADD docker/salt/_libs/base /srv/salt/_libs/base
ADD docker/salt/top.sls /srv/salt/top.sls

ADD docker/supervisor.d /etc/supervisor.d
RUN chmod -R +x /etc/supervisor.d/

ADD docker/confd /etc/confd
