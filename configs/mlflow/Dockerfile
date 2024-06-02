FROM ghcr.io/mlflow/mlflow:v2.0.1

USER root

# Update and install some necessary packges
RUN apt-get update -y && \
  apt-get install -y --no-install-recommends curl && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set working directory then copy and install configuration files
WORKDIR /mlflow/mlruns
COPY ./requirements.txt /mlflow/mlruns/
RUN pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt && \
  rm -rf ~/.cache/pip
