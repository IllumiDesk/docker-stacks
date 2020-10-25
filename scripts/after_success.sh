#!/bin/bash

set -e

# no need to build and tag images for pull requests.
tag_and_push () {
  if [ "${TRAVIS_PULL_REQUEST}" == "false" ]; then
    if [ "${TRAVIS_BRANCH}" == "main" ]; then
      echo "${DOCKERHUB_TOKEN}" | docker login -u "${DOCKERHUB_USERNAME}" --password-stdin
      export TAG="${TRAVIS_BUILD_NUMBER}"
      make build-all
      make push-all
      export TAG="latest"
      make build-all
      make push-all
    fi
  fi
}

main () {
  echo "Build and push images..."
  tag_and_push
}

main