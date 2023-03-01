FROM python:3.10

ENV PYTHONIOENCODING utf-8
ENV TZ="Asia/Tokyo"
ENV LANG=C.UTF-8
ENV LANGUAGE=en_US:en_US
ENV PYTHONDONTWRITEBYTECODE=1

COPY / /app/

WORKDIR /app/src

#poetry
RUN set -x \
    && pip install \
        poetry==1.4.0 \
    && poetry config virtualenvs.create false \
    && poetry install 
