FROM wicksy/base:latest

RUN apk update && \
    apk add bash && \
    apk add git && \
    pip install --upgrade pip && \
    pip install boto && \
    pip install boto3 && \
    pip install mkdocs

CMD ["/bin/bash", "-o", "vi"]
