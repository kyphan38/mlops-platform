FROM jupyter/base-notebook:python-3.11

USER root

# Update and install some necessary packges
RUN apt-get update -y && \
  apt-get install -y --no-install-recommends curl && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create folder for MLflow
RUN mkdir /mlflow && \
  chmod 777 -R /mlflow

# Set working directory then copy and install configuration files
WORKDIR /home/jovyan/
COPY ./requirements.txt /home/jovyan/
RUN pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt && \
  rm -rf ~/.cache/pip
