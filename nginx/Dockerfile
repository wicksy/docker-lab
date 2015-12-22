FROM wicksy/base:latest

USER root

RUN addgroup nginx && \
    adduser -D -h /home/nginx -G nginx nginx && \
    mkdir -p /var/log/nginx && \
    chown nginx:nginx /var/log/nginx

RUN apk update && \
    apk add nginx

ADD docker/supervisor.d /etc/supervisor.d
RUN chmod -R +x /etc/supervisor.d/

EXPOSE 80
EXPOSE 443
