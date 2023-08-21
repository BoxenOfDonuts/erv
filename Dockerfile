FROM python:3

WORKDIR /project

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
        libatlas-base-dev gfortran nginx supervisor

RUN pip install uwsgi

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --no-create-home nginx

RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

COPY server/nginx.conf /etc/nginx/
COPY server/site-nginx.conf /etc/nginx/conf.d/
COPY server/wsgi.ini /etc/uwsgi/
COPY server/supervisord.conf /etc/

COPY /app .

#ENV PYTHONPATH /project
RUN export PYTHONPATH=/project

CMD ["/usr/bin/supervisord"]
