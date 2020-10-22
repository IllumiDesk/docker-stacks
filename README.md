[![Build Status](https://travis-ci.com/IllumiDesk/docker-stacks.svg?branch=main)](https://travis-ci.com/IllumiDesk/docker-stacks)

# IllumiDesk docker-stacks

Dockerfiles and related assets for IllumiDesk's workspace images.

## Pre Requisits

- [Docker](https://docs.docker.com/get-docker/)

## Quickstart

1. Build images

Build images:

```
make build-all
```

2. Run:

Running the image standalone is helpful for testing. Replace `illumidesk/illumidesk-notebook:latest` below with your desired docker image and tag:

```bash
docker run -p 8888:8888 illumidesk/illumidesk-notebook:latest
```

> Refer to [docker's documentation](https://docs.docker.com/engine/reference/run/) for additional `docker run ...` options.

### Image Layers

The IllumiDesk docker layers for workspace types are built with the following sequence:

1. The `base-notebook` is built with all required dependencies using the `repo2docker` convention.
2. The `illumidesk-notebook` image builds from the `base-notebook` image to add scripts and environment variables that allows the base image to maintain compatibility with the upstream `jupyter/docker-stacks` images.
3. The `illumidesk-grader` adds the grader extensions to the `illumidesk-notebook` base image.

## Build Mechanism

1. Build and tag the base image or all images at once. Use the `TAG` argument to add your custom tag. The `TAG` argument defaults to `latest` if not specified:

```bash
    make build/base-notebook TAG=mytag
```

The base image uses the standard `repo2docker` convention to set dependencies. [Refer to this project's documentaiton](https://repo2docker.readthedocs.io/en/latest/) for additional configuration options.


2. (Optional) Use the base image from step 1 above as a base image for an image compatible with the IllumiDesk stack.

```
# The jupyter/base-notebook is the source for scripts and files to
# achieve jupyter/docker-stacks compatibility
FROM jupyter/base-notebook:latest AS base

# The image is built from the base-notebook image located in this repo
FROM illumidesk/base-notebook:latest

# The base notebook sets $NB_USER as the default users. We need to set the user to
# root to copy files to folders that require root permissions.
USER root

COPY --from=base /usr/local/bin/start* /usr/local/bin/
COPY --from=base /usr/local/bin/fix-permissions /usr/local/bin/
COPY --from=base /etc/jupyter/jupyter_notebook_config.py /etc/jupyter/

# Add additional depdencies if needed
RUN ... do stuff

# Make sure you run fix-permissions after running optional commands above
RUN fix-permissions "${HOME} \
 && fix-permissions "${CONDA_DIR}

# Always run the container as NB_USER
USER "${NB_USER}"

```

2. (Optional) Push images to DockerHub

```bash
    docker push illumidesk/illumidesk-notebook:latest
```

> This repo contains scripts to build, test, and push the images with GitHub actions. Avoid manual pushes if possible to avoid unnecessary drifts with the git-based commits.

## Development and Testing

> Type `make help` for a list of possible commands.

1. Create your virtual environment and install dev-requirements:

```bash
    make venv
```

2. Check Dockerfiles with linter:

```bash
    make lint-all
```

Tests start the docker container(s), runs commands by emulating the  `docker exec ...` command, and asserts the outputs with the `pytest` package. You can run tests on one image or all images. Use the `TAG` key to specify a docker image tag to test (TAG defaults to `latest`):

```bash
    make test
```

## References

These images are based on the `jupyter/docker-stacks` images. [Refer to their documentation](https://jupyter-docker-stacks.readthedocs.io/en/latest/) for the full set of configuration options.

## Attributions

- [JupyterHub repo2docker](https://repo2docker.readthedocs.io/en/latest/)
- [jupyter/docker-stacks images](https://github.com/jupyter/docker-stacks)
- [code-server](https://github.com/cdr/code-server)
