FROM python:3.10-slim AS build

RUN apt-get update
COPY deployment/requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.10-slim

RUN apt-get update && \
  apt-get install -y --no-install-recommends curl && \
  apt-get autoremove -yqq --purge && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# ENV

COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . /pipeline
WORKDIR /pipeline
