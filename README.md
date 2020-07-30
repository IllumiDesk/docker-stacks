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
docker run -p 8888:8888 illumidesk/base-notebook:latest
```

> Refer to [docker's documentation](https://docs.docker.com/engine/reference/run/) for additional `docker run ...` options.

## Image catalogue

| Image | DockerHub Link |
| --- | --- |
| illumidesk/base-notebook | [![Docker Image](https://img.shields.io/docker/automated/illumidesk/base-notebook)](https://img.shields.io/docker/automated/illumidesk/base-notebook?label=base-notebook) |
| illumidesk/grader-notebook | [![Docker Image](https://img.shields.io/docker/automated/illumidesk/grader-notebook)](https://hub.docker.com/repository/docker/illumidesk/base-notebook?label=grader-notebook) |
| illumidesk/instructor-notebook | [![Docker Image](https://img.shields.io/docker/automated/illumidesk/instructor-notebook)](https://hub.docker.com/repository/docker/illumidesk/instructor-notebook?label=instructor-notebook) |
| illumidesk/learner-notebook | [![Docker Image](https://img.shields.io/docker/automated/illumidesk/learner-notebook)](https://hub.docker.com/repository/docker/illumidesk/learner-notebook?label=learner-notebook) |
| illumidesk/rstudio | [![Docker Image](https://img.shields.io/docker/automated/illumidesk/rstudio)](https://hub.docker.com/repository/docker/illumidesk/rstudio?label=rstudio) |
| illumidesk/theia | [![Docker Image](https://img.shields.io/docker/automated/illumidesk/theia)](https://hub.docker.com/repository/docker/illumidesk/theia?label=theia) |
| illumidesk/vscode | [![Docker Image](https://img.shields.io/docker/automated/illumidesk/vscode)](https://hub.docker.com/repository/docker/illumidesk/vscode?label=vscode) |

### Images prepared for Learning Tools Interoperability (LTI) Roles

- **Base Jupyter Notebook**: based on the [`jupyter/datascience-notebook`](https://github.com/jupyter/docker-stacks/tree/master/datascience-notebook) plus:

  - Java kernel using JRE based on Open JDK 11
  - Julia, Python, and R packages installed with files (install.jl, requirements.txt, environment.yml, respectively).
  - Jupyter Notebook configuration to support iFrames

- **Learner Jupyter Notebook**: adds `nbgrader` extensions for the `learner` role.
- **Instructor Jupyter Notebook**: adds `nbgrader` extensions for the `instructor` role.
- **Grader Jupyter Notebook**: adds `nbgrader` extensions for the shared `grader` notebook.

The IllumiDesk docker layers for grader images are illustrated below:

![Jupyter notebook grader images](/img/grader_images.png)

### Additional Workspace Types

- **THEIA IDE**: basic version of the THEIA IDE. `THEIA` is highly configurable, refer to [their documention](https://github.com/eclipse-theia/theia#documentation) for customization options (mostly done via package.json modifications).
- **VS Code**: this image contains the `code-server` VS Code distribution optimized for `docker`.
- **RStudio**: uses [`illumidesk/r-conda`](https://github.com/illumidesk/r-conda) as a base image.

The IllumiDesk docker layers for workspace types are illustrated below:

![Jupyter notebook workspace images](/img/workspace_images.png)

## Build Mechanism

1. Build and tag the base image or all images at once:

```bash
    make build/base-image TAG=mytag
```

or

```bash
    make build-all TAG=mytag
```


2. Use the base image from step 1 above as:

  a) A base image and add additional layers to said image to create your own custom image

```
FROM illumidesk/base-notebook:latest

RUN ...
```

or

  b) A source image for files necessary to use image with the [IllumiDesk](https://github.com/IllumiDesk/illumidesk) stack.

```
FROM illumidesk/base-notebook:latest AS base

FROM acme/image:tag

COPY --from=base /usr/local/bin/start* /usr/local/bin/
COPY --from=base /usr/local/bin/fix-permissions /usr/local/bin/
COPY --from=base /etc/jupyter/jupyter_notebook_config.py /etc/jupyter/

RUN ...
```

3. Push images to DockerHub

```bash
docker push organization/custom-image
```

## Testing

Tests start the docker container(s), runs commands by emulating the  `docker exec ...` command, and asserts the outputs. You can run tests on one image or all images. Use the `TAG` key to specify a docker image tag to test (TAG defaults to `latest`):

```bash
make test/base-notebook TAG=mytag
```

or

```bash
make test-all
```

## References

These images are based on the `jupyter/docker-stacks` images. [Refer to their documentation](https://jupyter-docker-stacks.readthedocs.io/en/latest/) for the full set of configuration options.
