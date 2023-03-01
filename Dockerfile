FROM --platform=linux/amd64 python:3.10-slim

COPY / /project/

WORKDIR /project/app

#poetry
RUN set -x \
    && pip install \
        poetry==1.4.0 \
    && poetry config virtualenvs.create false \
    && poetry install 
