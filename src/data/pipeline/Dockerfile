FROM python:3.12-slim

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# Update and install some necessary packges
RUN apt-get update -y && \
  apt-get install -y --no-install-recommends curl awscli tree && \
  apt-get clean && \
  rm -rf /var/lib/apt/list/* /tmp/* /var/tmp/*

# Add repository code
WORKDIR /opt/dagster/app
COPY ./requirements.txt /opt/dagster/app/
RUN pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt && \
  rm -rf ~/.cache/pip

# CMD allows this to be overridden from run launchers or executors that want to run other commands against your repository
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-m", "pipeline"]
