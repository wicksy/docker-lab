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

ADD docker/supervisor.d /etc/supervisor.d
RUN chmod -R +x /etc/supervisor.d/

ADD docker/confd /etc/confd
