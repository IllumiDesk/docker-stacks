# IllumiDesk docker-stacks

Dockerfiles and related assets for IllumiDesk's workspace images.

## Pre Requisits

- [Docker](https://docs.docker.com/get-docker/)

## Quickstart

```bash
docker run -p 8888:8888 illumidesk/datascience-notebook
```

## Image catalogue

- **Base Jupyter Notebook**: based on the `jupyter/datascience-notebook` image + `Java kernel`.
- **Learner Jupyter Notebook**: adds nbgrader extensions for the `learner` role.
- **Instructor Jupyter Notebook**: adds nbgrader extensions for the `instructor` role.
- **Grader Jupyter Notebook**: adds nbgrader extensions for the shared `grader` notebook.
- **THEIA IDE**: basic version of the THEIA IDE. `THEIA` is highly configurable, refer to [their documention](https://github.com/eclipse-theia/theia#documentation) for customization options (mostly done via package.json modifications).
- **VS Code**: this image contains the `code-server` VS Code distribution optimized for `docker`.
- **RStudio**: uses [`binder-examples/r-conda`](https://github.com/binder-examples/r-conda) as a base image.

## Build Mechanisme

1. Build and tage the base image
2. Use the base image from step 1 above as:

  a) A base image and add additional layers to said image to create your own custom image
  b) A source image for files necessary to use image with the [IllumiDesk](https://github.com/IllumiDesk/illumidesk) stack.

3. Push images to DockerHub

## References

These images are based on the `jupyter/docker-stacks` images. [Refer to their documentation](https://jupyter-docker-stacks.readthedocs.io/en/latest/) for the full set of configuration options.
