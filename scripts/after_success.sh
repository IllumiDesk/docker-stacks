#!/bin/bash

set -e

dockerhub_login () {
    echo "${DOCKERHUB_TOKEN}" | docker login -u "${DOCKERHUB_USERNAME}" --password-stdin
}

# no need to build and tag images for pull requests.
tag_and_push () {
  if [ "${TRAVIS_PULL_REQUEST}" == "false" ]; then
    if [ "${TRAVIS_BRANCH}" == "main" ]; then
      export TAG="${TRAVIS_BUILD_NUMBER}"
      make build-all
    fi
  fi
}

main () {
  echo "DockerHub login..."
  dockerhub_login
  echo "Build and push images..."
  tag_and_push
}

main