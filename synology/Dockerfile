FROM alpine:latest

ADD docker/py/requirements.txt /tmp/requirements.txt

RUN apk update && \
    apk add bash && \
    apk add python && \
    apk add py-pip && \
    apk add wget && \
    apk add curl && \
    apk add vim && \
    apk add groff && \
    apk add git && \
    apk add git-bash-completion && \
    pip install --upgrade pip && \
    pip install --requirement /tmp/requirements.txt

ADD docker/root /root

CMD ["/bin/bash", "-o", "vi"]
