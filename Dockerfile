# Debian 8.5 with miniconda and python3.5
FROM continuumio/miniconda3

MAINTAINER Martin Tomik <mtomik@live.com>
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y --fix-missing libgtk2.0-dev libpq-dev

COPY *.txt /
RUN conda update -y --all && \
    conda create -y --name work python=3.5

ENV PATH $CONDA_DIR/bin:$PATH

RUN source activate work && \
    conda install -y --file conda-requirements.txt && \
    conda install -y -c menpo opencv3=3.2.0 && \
    pip install  -r requirements.txt

ENV PATH /opt/conda/envs/work/bin:$PATH

# copy Django project
RUN mkdir /code
WORKDIR /code
COPY . .
RUN chmod +x run_web.sh

RUN addgroup web
RUN adduser --disabled-password  --no-create-home --system -q --ingroup web web
USER web