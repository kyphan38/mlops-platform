FROM grafana/loki:latest

USER root

# Set working directory then copy and install configuration files
WORKDIR /etc/loki

# Create necessary directories for Loki
RUN mkdir -p /loki/index /loki/chunks /loki/boltdb-cache

CMD ["-config.file=/etc/loki/local-config.yaml"]
