FROM python:3.9-slim

WORKDIR /project

RUN apt update && \
    apt install -y gcc

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install uwsgi --no-cache-dir && \
    pip install --no-cache-dir -r requirements.txt

COPY / .

# RUN groupadd -g 998 i2c && \
#     usermod -a -G i2c www-data

RUN export PYTHONPATH=/project
