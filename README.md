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

- **Base Jupyter Notebook**: based on the [`jupyter/datascience-notebook`](https://github.com/jupyter/docker-stacks/tree/master/datascience-notebook) plus:

  - Java kernel using JRE based on Open JDK 11
  - Julia, Python, and R packages installed with files (install.jl, requirements.txt, environment.yml, respectively).
  - Jupyter Notebook configuration to support iFrames

- **Learner Jupyter Notebook**: adds `nbgrader` extensions for the `learner` role.
- **Instructor Jupyter Notebook**: adds `nbgrader` extensions for the `instructor` role.
- **Grader Jupyter Notebook**: adds `nbgrader` extensions for the shared `grader` notebook.

The IllumiDesk docker layers for grader images are illustrated below:

![Jupyter notebook grader images](/img/docker_stacks_v2.png)

### Additional Workspace Types

- **THEIA IDE**: basic version of the THEIA IDE. `THEIA` is highly configurable, refer to [their documention](https://github.com/eclipse-theia/theia#documentation) for customization options (mostly done via package.json modifications).
- **VS Code**: this image contains the `code-server` VS Code distribution optimized for `docker`.
- **RStudio**: uses [`illumidesk/r-conda`](https://github.com/illumidesk/r-conda) as a base image.

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
FROM jupyter/minimal-notebook:latest AS base

FROM illumidesk/base-notebook:latest

ENV NB_USER=jovyan
ENV NB_UID=1000
ENV NB_GID="${NB_GID}"
ENV HOME="/home/${NB_USER}"

COPY --from=base /usr/local/bin/start* /usr/local/bin/
COPY --from=base /usr/local/bin/fix-permissions /usr/local/bin/
COPY --from=base /etc/jupyter/jupyter_notebook_config.py /etc/jupyter/

RUN ...
```

2. Push images to DockerHub

```bash
docker push organization/custom-image
```

## Testing

Tests start the docker container(s), runs commands by emulating the  `docker exec ...` command, and asserts the outputs. You can run tests on one image or all images. Use the `TAG` key to specify a docker image tag to test (TAG defaults to `latest`):

```bash
pytest -v
```

## References

These images are based on the `jupyter/docker-stacks` images. [Refer to their documentation](https://jupyter-docker-stacks.readthedocs.io/en/latest/) for the full set of configuration options.
