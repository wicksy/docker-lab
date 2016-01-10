FROM alpine:latest

RUN apk update && \
    apk add bash && \
    apk add python && \
    apk add py-pip && \
    apk add wget && \
    apk add curl && \
    apk add vim && \
    apk add git && \
    apk add git-bash-completion && \
    pip install --upgrade pip && \
    pip install awscli

ADD docker/root /root

CMD ["/bin/bash", "-o", "vi"]
