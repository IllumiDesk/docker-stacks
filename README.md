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

Running the image standalone is helpful for testing:

```bash
docker run -p 8888:8888 illumidesk/illumidesk-notebook:latest
```

> Refer to [docker's documentation](https://docs.docker.com/engine/reference/run/) for additional `docker run ...` options.

## Image catalogue

| Image | DockerHub Link |
| --- | --- |
| illumidesk/base-notebook | [![Docker Image](https://img.shields.io/docker/automated/illumidesk/base-notebook)](https://img.shields.io/docker/automated/illumidesk/base-notebook?label=base-notebook) |
| illumidesk/grader-notebook | [![Docker Image](https://img.shields.io/docker/automated/illumidesk/grader-notebook)](https://hub.docker.com/repository/docker/illumidesk/base-notebook?label=grader-notebook) |
| illumidesk/illumidesk-notebook | [![Docker Image](https://img.shields.io/docker/automated/illumidesk/instructor-notebook)](https://hub.docker.com/repository/docker/illumidesk/illumidesk-notebook?label=illumidesk-notebook) |

### Images prepared for Learning Tools Interoperability (LTI) Roles

- **Base Jupyter Notebook**: based on the [`jupyter/base-notebook`](https://github.com/jupyter/docker-stacks/tree/master/datascience-notebook) plus:

  - Java kernel using JRE based on Open JDK 11
  - Julia, Python, and R packages installed with [repo2docker-based conventions](https://repo2docker.readthedocs.io/en/latest/)
  - C++ kernels (11, 14, and 17) with Xeus installed with `conda`.
  - Jupyter Notebook configuration to support iFrames.
  - `nbgrader` extensions enabled by LTI role (`learner` and `instructor`)
  - Jupyter Classic and JupyterLab launchers for `jupyter-server-proxy` compatible services.
  - VS Code compatible IDE with `code-server` available with the `/vscode` path.
  - RStudio and Shiny servers available with the `/rstudio` and `/shiny` paths, respectively.

### Image Layers

The IllumiDesk docker layers for workspace types are illustrated below:

![Jupyter notebook workspace images](/img/docker_stacks_v2.png)

## Build Mechanism

1. Build and tag the base image or all images at once. Use the `TAG` argument to add your custom tag. The `TAG` argument defaults to `latest` if not specified:

```bash
    make build/base-notebook TAG=mytag
```

The base image uses the standard `repo2docker` convention to set dependencies. [Refer to this project's documentaiton](https://repo2docker.readthedocs.io/en/latest/) for additional configuration options.


2. (Optional) Use the base image from step 1 above as a base image for an image compatible with the illumidesk stack.

```
FROM jupyter/base-notebook:latest AS base

FROM illumidesk/base-notebook:latest

USER root

COPY --from=base /usr/local/bin/start* /usr/local/bin/
COPY --from=base /usr/local/bin/fix-permissions /usr/local/bin/
COPY --from=base /etc/jupyter/jupyter_notebook_config.py /etc/jupyter/

RUN ... do stuff

RUN fix-permissions "${HOME} \
 && fix-permissions "${CONDA_DIR}  # make sure you run fix-permissions after doing stuff

USER "${NB_USER}"

```

2. Push images to DockerHub

```bash
    docker push organization/custom-image
```

## Development and Testing

1. Create your virtual environment and install dev-requirements:

```bash
    make venv
```

2. Check Dockerfiles with linter:

```bash
    make lint-all
```

Type `make help` for additional commands.

Tests start the docker container(s), runs commands by emulating the  `docker exec ...` command, and asserts the outputs. You can run tests on one image or all images. Use the `TAG` key to specify a docker image tag to test (TAG defaults to `latest`):

```bash
    make test
```

## References

These images are based on the `jupyter/docker-stacks` images. [Refer to their documentation](https://jupyter-docker-stacks.readthedocs.io/en/latest/) for the full set of configuration options.

## Attributions

- [JupyterHub repo2docker](https://repo2docker.readthedocs.io/en/latest/)
- [jupyter/docker-stacks images](https://github.com/jupyter/docker-stacks)
- [code-server](https://github.com/cdr/code-server)

RStudio and Shiny are trademarks of RStudio, PBC. Refer to RStudio's trademark guidelines for more information.
