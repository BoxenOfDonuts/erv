FROM python:3.9

WORKDIR /project

COPY requirements.txt ./

#RUN useradd --no-create-home nginx

#RUN rm /etc/nginx/sites-enabled/default
#RUN rm -r /root/.cache

#COPY server/nginx.conf /etc/nginx/
#COPY server/site-nginx.conf /etc/nginx/conf.d/
#COPY server/wsgi.ini /etc/uwsgi/
#COPY server/supervisord.conf /etc/

COPY / .

RUN apt-get update
RUN apt-get install -y cmake

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN pip install uwsgi

#ENV PYTHONPATH /project
RUN export PYTHONPATH=/project

#CMD ["/usr/bin/supervisord"]
#CMD ["uwsgi", "--http", "0.0.0.0:5000", "--master", "-p", "4", "-w", "wsgi:app"]
