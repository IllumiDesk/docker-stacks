#!/bin/bash

set -e

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
  echo "Build and push images..."
  tag_and_push
}

main