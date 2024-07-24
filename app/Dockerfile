FROM python:3.9

WORKDIR /project

RUN apt-get update -y && \
    apt-get install --no-install-recommends cmake -y

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install uwsgi --no-cache-dir && \
    pip install --no-cache-dir -r requirements.txt

COPY / .

RUN export PYTHONPATH=/project
