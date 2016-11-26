FROM wicksy/base:latest

USER root

RUN apk update && \
    apk add nginx

RUN chown -R nginx:www-data /var/lib/nginx && \
    mkdir -p /run/nginx /app/public /var/log/app && \
    chown nginx:nginx /run/nginx /app/public /var/log/app

ADD docker/supervisor.d /etc/supervisor.d
RUN chmod -R +x /etc/supervisor.d/

ADD docker/confd /etc/confd
ADD docker/nginx /etc/nginx
ADD docker/html  /app/public

EXPOSE 80
EXPOSE 443
