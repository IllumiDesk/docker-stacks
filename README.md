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

Running the image standalone is helpful for testing. Refer to the sections below to ensure the images have the required assets to run with the IllumiDesk stack.

```bash
docker run -p 8888:8888 illumidesk/datascience-notebook
```

> Refer to [docker's documentation](https://docs.docker.com/engine/reference/run/) for additional `docker run ...` options.

## Image catalogue

### Images prepared for Learning Tools Interoperability (LTI) Roles

- **Base Jupyter Notebook**: based on the [`jupyter/datascience-notebook`](https://github.com/jupyter/docker-stacks/tree/master/datascience-notebook) image + `Java kernel`.
- **Learner Jupyter Notebook**: adds `nbgrader` extensions for the `learner` role.
- **Instructor Jupyter Notebook**: adds `nbgrader` extensions for the `instructor` role.
- **Grader Jupyter Notebook**: adds `nbgrader` extensions for the shared `grader` notebook.

The IllumiDesk docker layers for grader images are illustrated below:

![Jupyter notebook grader images](/img/grader_images.png)

### Additional Workspace Types

- **THEIA IDE**: basic version of the THEIA IDE. `THEIA` is highly configurable, refer to [their documention](https://github.com/eclipse-theia/theia#documentation) for customization options (mostly done via package.json modifications).
- **VS Code**: this image contains the `code-server` VS Code distribution optimized for `docker`.
- **RStudio**: uses [`binder-examples/r-conda`](https://github.com/binder-examples/r-conda) as a base image.

The IllumiDesk docker layers for workspace types are illustrated below:

![Jupyter notebook workspace images](/img/workspace_images.png)

## Build Mechanism

1. Build and tag the base image

```bash
    docker build -t illumidesk/datascience-notebook:latest \
      -f notebooks/Dockerfile.base \
      notebooks/.
```

2. Use the base image from step 1 above as:

  a) A base image and add additional layers to said image to create your own custom image

```
FROM illumidesk/datascience-notebook:latest

RUN ...
```

  b) A source image for files necessary to use image with the [IllumiDesk](https://github.com/IllumiDesk/illumidesk) stack.

```
FROM illumidesk/datascience-notebook:latest AS base

FROM acme/image:tag

COPY --from=base /usr/local/bin/start* /usr/local/bin/
COPY --from=base /usr/local/bin/fix-permissions /usr/local/bin/
COPY --from=base /etc/jupyter/jupyter_notebook_config.py /etc/jupyter/

RUN ...
```

3. Push images to DockerHub

## References

These images are based on the `jupyter/docker-stacks` images. [Refer to their documentation](https://jupyter-docker-stacks.readthedocs.io/en/latest/) for the full set of configuration options.
