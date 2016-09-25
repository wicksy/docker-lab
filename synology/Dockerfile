FROM alpine:latest

ADD docker/py/requirements.txt /tmp/requirements.txt

RUN apk update && \
    apk add bash && \
    apk add python && \
    apk add py-pip && \
    apk add wget && \
    apk add curl && \
    apk add file && \
    apk add vim && \
    apk add groff && \
    apk add git && \
    apk add git-bash-completion && \
    apk add openssh-client && \
    pip install --upgrade pip && \
    pip install --requirement /tmp/requirements.txt

# Tidy up apk cache
RUN rm -rf /var/cache/apk/*

ADD docker/root /root
RUN chmod 700 /root/.ssh

RUN mkdir /scripts
ADD docker/py/ /scripts
RUN chmod -R +x /scripts

CMD ["/bin/bash", "-o", "vi"]
