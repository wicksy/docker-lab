FROM alpine:latest

RUN apk update && \
    apk add bash && \
    apk add git && \
    apk add python && \
    apk add py2-pip && \
    pip install --upgrade pip && \
    pip install boto && \
    pip install boto3 && \
    pip install mkdocs && \
    pip install mkdocs-material && \
    addgroup wicksy && \
    adduser -h /home/wicksy -s /bin/bash -D -G wicksy wicksy && \
    mkdir -p /data/cv/ && \
    chown wicksy:wicksy /data/cv && \
    chmod -R 755 /data

EXPOSE 8080
VOLUME /data/cv

USER wicksy
WORKDIR /data/cv

CMD ["/usr/bin/mkdocs", "serve", "--dev-addr", "0.0.0.0:8080", "--theme", "material"]
