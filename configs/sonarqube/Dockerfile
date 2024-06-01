FROM sonarqube:9.9.5-community

USER root

# Update and install some necessary packges
RUN apt-get update -y && \
  apt-get install -y --no-install-recommends curl && \
  apt-get clean && \
  rm -rf /var/lib/apt/list/* /tmp/* /var/tmp/*

# Set working directory then copy and install configuration files
WORKDIR /opt/sonarqube

# Chagne permissions of logs folder
RUN chown -R sonarqube:sonarqube /opt/sonarqube/data /opt/sonarqube/logs /opt/sonarqube/temp /opt/sonarqube/extensions

USER sonarqube