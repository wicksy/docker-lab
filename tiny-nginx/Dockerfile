FROM alpine:latest

USER root

RUN apk update && \
    apk add nginx

RUN echo -e "\ndaemon off;" >> /etc/nginx/nginx.conf && \
    chown -R nginx:www-data /var/lib/nginx

EXPOSE 80
EXPOSE 443

WORKDIR /etc/nginx

CMD ["/usr/sbin/nginx"]
