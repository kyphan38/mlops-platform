FROM python:3.12-slim

# Set DAGSTER_HOME and setup for Dagster instance
ENV DAGSTER_HOME=/opt/dagster/dagster_home
RUN mkdir -p ${DAGSTER_HOME} && \
  mkdir -p ${DAGSTER_HOME}/storage && \
  mkdir -p ${DAGSTER_HOME}/compute_logs && \
  mkdir -p ${DAGSTER_HOME}/local_artifact_storage

RUN apt-get update && apt-get install -y curl iputils-ping

# Set working directory then copy and install configuration files
WORKDIR ${DAGSTER_HOME}
COPY ./requirements.txt ${DAGSTER_HOME}
RUN pip install --upgrade pip && pip install -r requirements.txt
