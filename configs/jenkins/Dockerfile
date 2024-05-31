FROM jenkins/jenkins:2.460-jdk17

USER root

# Update and install some necessary packges
RUN apt-get update -y && \
  apt-get install -y --no-install-recommends curl && \
  apt-get clean && \
  rm -rf /var/lib/apt/list/* /tmp/* /var/tmp/*

# Set working directory then copy and install configuration files
WORKDIR /var/jenkins_home
