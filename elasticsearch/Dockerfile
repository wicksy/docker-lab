FROM wicksy/jre-7:latest

USER root

RUN addgroup elasticsearch && \
    adduser -D -h /home/elasticsearch -G elasticsearch elasticsearch && \
    mkdir -p /var/log/elasticsearch && \
    chown elasticsearch:elasticsearch /var/log/elasticsearch && \
    mkdir /opt

RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys 46095ACC8548582C1A2699A9D27D666CD88E42B4

RUN curl -o /opt/es211.tar.gz "https://download.elasticsearch.org/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.1.1/elasticsearch-2.1.1.tar.gz" && \
    cd /opt && \
    tar -xzvf es211.tar.gz && \
    ln -sf /opt/elasticsearch-2.1.1/ /opt/elasticsearch && \
    chown -R elasticsearch:elasticsearch /opt/elasticsearch-2.1.1/ && \
    rm -rf /opt/es211.tar.gz

EXPOSE 9200
EXPOSE 9300
