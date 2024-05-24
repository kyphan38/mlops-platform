#!/bin/bash

# Input
command=$1

# Constants
DOCKER_USER="$DOCKER_USER"
PROJECT="mlops_platform_thesis"
IMAGE_NAME="feature_store"
IMAGE_TAG=$(git describe --always)

if [[ -z $DOCKER_USER ]]; then
  echo "Missing \$DOCKER_USER var in env"
  exit 1
fi

if [[ -z $command ]]; then
  echo "Missing command"
  exit 1
fi

usage() {
  echo "feature_repo      deploy feature repo and related scripts"
}

deploy_feature_repo() {
  rsync -avr feature_repo ../training_pipeline --exclude registry
}

case $command in
  feature_repo)
    deploy_feature_repo "$@"
    ;;

  *)
    echo -n "Unknown command: $command"
    usage
    exit 1
    ;;
esac
