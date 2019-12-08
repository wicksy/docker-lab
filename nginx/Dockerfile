FROM wicksy/base:latest

USER root

RUN apk update && \
    apk add nginx

RUN chown -R nginx:www-data /var/lib/nginx && \
    mkdir -p /run/nginx /app/public /var/log/app && \
    chown nginx:nginx /run/nginx /app/public /var/log/app && \
    rm -f /etc/nginx/conf.d/default.conf

RUN openssl req -x509 -nodes -days 365 -subj "/C=CA/ST=QC/O=Company, Inc./CN=mydomain.com" -addext "subjectAltName=DNS:mydomain.com" -newkey rsa:2048 -keyout /etc/ssl/key.pem -out /etc/ssl/cert.pem

ADD docker/supervisor.d /etc/supervisor.d
RUN chmod -R +x /etc/supervisor.d/

ADD docker/confd /etc/confd
ADD docker/nginx /etc/nginx
ADD docker/html  /app/public

EXPOSE 80
EXPOSE 443
