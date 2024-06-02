FROM jenkins/jenkins:2.460-jdk17

USER root

# Update and install some necessary packges
RUN apt-get update -y && \
  apt-get install -y --no-install-recommends curl && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install plugins
RUN jenkins-plugin-cli --plugins pipeline-stage-view:2.34 \
                                 pipeline-graph-view:287.v3ef017b_780d5 \
                                 credentials-binding:677.vdc9d38cb_254d \
                                 sonar:2.17.2

# Set working directory then copy and install configuration files
WORKDIR /var/jenkins_home
