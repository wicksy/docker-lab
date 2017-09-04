FROM wicksy/jre-8:latest

USER root

RUN addgroup elasticsearch && \
    adduser -D -h /home/elasticsearch -G elasticsearch elasticsearch && \
    mkdir -p /var/log/elasticsearch && \
    chown elasticsearch:elasticsearch /var/log/elasticsearch && \
    mkdir /opt

RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys 46095ACC8548582C1A2699A9D27D666CD88E42B4

RUN curl -o /opt/es.tar.gz "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.5.2.tar.gz" && \
    cd /opt && \
    tar -xzvf es.tar.gz && \
    ln -sf /opt/elasticsearch-5.5.2/ /opt/elasticsearch && \
    chown -R elasticsearch:elasticsearch /opt/elasticsearch-5.5.2/ && \
    rm -rf /opt/es.tar.gz

RUN pip install elasticsearch-curator

ADD docker/confd /etc/confd

ADD docker/supervisor.d /etc/supervisor.d
RUN chmod -R +x /etc/supervisor.d/

EXPOSE 9200
EXPOSE 9300
