#!/bin/bash

# Input
command=$1

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
