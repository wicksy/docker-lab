FROM wicksy/base:latest

USER root

RUN apk update && \
    apk add nginx

RUN echo -e "\ndaemon off;" >> /etc/nginx/nginx.conf && \
    chown -R nginx:www-data /var/lib/nginx && \
    mkdir /run/nginx && \
    chown nginx:nginx /run/nginx

ADD docker/supervisor.d /etc/supervisor.d
RUN chmod -R +x /etc/supervisor.d/

EXPOSE 80
EXPOSE 443
