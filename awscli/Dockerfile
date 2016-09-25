FROM alpine:latest

RUN apk update && \
    apk add python && \
    apk add py-pip && \
    apk add groff && \
    apk add less && \
    pip install --upgrade pip && \
    pip install awscli

CMD ["/bin/sh"]
