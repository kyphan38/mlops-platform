FROM jupyter/base-notebook:python-3.11

WORKDIR /home/jovyan/
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install -r ./requirements.txt
