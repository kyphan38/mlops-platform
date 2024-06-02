FROM python:3.12-slim

ENV DAGSTER_HOME=/opt/dagster/dagster_home

# Setup for Dagster instance
RUN mkdir -p ${DAGSTER_HOME} && \
  mkdir -p ${DAGSTER_HOME}/storage && \
  mkdir -p ${DAGSTER_HOME}/compute_logs && \
  mkdir -p ${DAGSTER_HOME}/local_artifact_storage

# Update and install some necessary packges
RUN apt-get update -y && \
  apt-get install -y --no-install-recommends curl && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set working directory then copy and install configuration files
WORKDIR ${DAGSTER_HOME}
COPY ./requirements.txt ${DAGSTER_HOME}
RUN pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt && \
  rm -rf ~/.cache/pip
