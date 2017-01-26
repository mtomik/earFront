# Debian 8.5 with miniconda and python3.5
FROM continuumio/miniconda3

MAINTAINER Martin Tomik <mtomik@live.com>

RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y --fix-missing libgtk2.0-dev libpq-dev

COPY *.txt /
RUN conda update -y --all && \
    conda install -y --file conda-requirements.txt && \
    conda install -y -c menpo opencv3=3.2.0 && \
    pip install  -r requirements.txt

# copy Django project
RUN mkdir /code
WORKDIR /code
COPY . .
RUN chmod +x run_celery.sh run_web.sh

RUN adduser --disabled-password --gecos '' myuser
#EXPOSE 8000
#CMD ["python","manage.py","runserver","0.0.0.0:8000"]