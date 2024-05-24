FROM python:3.10-slim

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# Update packages and install curl
RUN apt-get update --yes && \
  apt-get install --yes --no-install-recommends curl awscli tree && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Add repository code
WORKDIR /opt/dagster/app
COPY requirements.txt /opt/dagster/app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /opt/dagster/app/pipeline

# CMD allows this to be overridden from run launchers or executors that want to run other commands against your repository
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4002", "-m", "training_pipeline"]
