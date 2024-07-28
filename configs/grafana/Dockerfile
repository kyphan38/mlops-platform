FROM grafana/grafana:11.0.0-ubuntu

USER root

# Update and install some necessary packges
RUN apt-get update -y && \
  apt-get install -y --no-install-recommends curl && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set working directory then copy and install configuration files
WORKDIR /var/lib/grafana
