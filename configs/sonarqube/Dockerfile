FROM sonarqube:9.9.5-community

USER root

# Update and install some necessary packages
RUN apt-get update -y && \
  apt-get install -y --no-install-recommends curl unzip sudo && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Sonar Scanner
RUN curl -o /tmp/sonar_scanner.zip -L "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip" && \
  unzip /tmp/sonar_scanner.zip -d /opt/sonarqube/ && \
  mv /opt/sonarqube/sonar-scanner-5.0.1.3006-linux /opt/sonarqube/sonar_scanner && \
  rm /tmp/sonar_scanner.zip 

# Update PATH
ENV PATH="/opt/sonarqube/sonar_scanner/bin:${PATH}"

# Chagne permissions of logs folder
RUN chown -R sonarqube:sonarqube /opt/sonarqube/data \
                                 /opt/sonarqube/logs \
                                 /opt/sonarqube/temp \
                                 /opt/sonarqube/extensions \
                                 /opt/sonarqube/sonar_scanner && \
    mkdir -p /home/sonarqube && \
    chown -R sonarqube:sonarqube /home/sonarqube/ && \
    mkdir -p /opt/sonarqube/.scannerwork && \
    chown -R sonarqube:sonarqube /opt/sonarqube/.scannerwork

USER sonarqube

# Set working directory then copy and install configuration files
WORKDIR /opt/sonarqube