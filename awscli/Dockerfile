FROM alpine:latest

RUN apk update && \
    apk add python && \
    apk add py-pip && \
    pip install --upgrade pip && \
    pip install awscli

CMD ["/bin/sh"]
