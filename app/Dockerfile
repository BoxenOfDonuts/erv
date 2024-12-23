FROM python:3.11-alpine3.21

WORKDIR /project

RUN apk add --no-cache build-base libffi-dev

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install uwsgi --no-cache-dir && \
    pip install --no-cache-dir -r requirements.txt

COPY / .

RUN export PYTHONPATH=/project
