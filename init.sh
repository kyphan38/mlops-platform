#!/bin/bash

mkdir -p ./logs/sonarqube/sonar_scanner && chmod -R 777 ./logs/sonarqube/sonar_scanner
mkdir -p ./logs/sonarqube/sonarqube_data && chmod -R 777 ./logs/sonarqube/sonarqube_data
mkdir -p ./logs/sonarqube/sonarqube_extensions && chmod -R 777 ./logs/sonarqube/sonarqube_extensions
mkdir -p ./logs/sonarqube/sonarqube_logs && chmod -R 777 ./logs/sonarqube/sonarqube_logs

# Swap space
# sudo fallocate -l 4G /swapfile
# sudo chmod 600 /swapfile
# sudo mkswap /swapfile
# sudo swapon /swapfile
# sudo sh -c 'echo "/swapfile swap swap defaults 0 0" >> /etc/fstab'
