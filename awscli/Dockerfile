FROM alpine:latest

RUN apk update && \
    apk add python3 && \
    apk add groff && \
    apk add less && \
    pip3 install --upgrade pip && \
    pip3 install awscli

CMD ["/bin/sh"]
