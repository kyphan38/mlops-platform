FROM ghcr.io/mlflow/mlflow:v2.0.1

USER root

# Update packages and install curl
RUN apt-get update --yes && \
  apt-get install --yes --no-install-recommends curl && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /mlflow/mlruns
COPY ./requirements.txt /mlflow/mlruns
RUN pip install --upgrade pip && pip install -r requirements.txt
