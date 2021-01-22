[![Build Status](https://travis-ci.com/IllumiDesk/docker-stacks.svg?branch=main)](https://travis-ci.com/IllumiDesk/docker-stacks)

# IllumiDesk Docker Stacks

Dockerfiles and related assets for IllumiDesk's workspace images. The purpose of this repo is to provide a template repo for IllumiDesk customer-centric images. To create a new customer-centric repo, click on the Use this Template button and confirm the repo name.

## Pre Requisits

- [Docker](https://docs.docker.com/get-docker/)

## Quickstart

1. Install dependencies

```bash
make venv
```

2. Build images

```bash
make build-all
```

3. Run:

Running the image standalone is helpful for testing:

```bash
docker run -p 8888:8888 illumidesk/illumidesk-notebook:latest
```

Then, navigate to `http://localhost:8888` to access your Jupyter Notebook server.

> Refer to [docker's documentation](https://docs.docker.com/engine/reference/run/) for additional `docker run ...` options.

4. Test:

```bash
make test
```

## Build Mechanism

1. Build and tag the base image or all images at once. Use the `TAG` argument to add your custom tag. The `TAG` argument defaults to `latest` if not specified.

Build all images:

```bash
make build-all
```

Build one image with custom tag:

```bash
make build/illumidesk-notebook TAG=mytag
```


1. (Optional) Change the base image based on one of the [`jupyter/docker-stacks`](https://github.com/jupyter/docker-stacks) images.

```

FROM jupyter/scipy-notebook:latest

RUN ... do stuff

USER root

RUN fix-permissions "${HOME} \
 && fix-permissions "${CONDA_DIR}  # make sure you run fix-permissions after doing stuff

USER "${NB_USER}"

```

## Development and Testing

1. Create your virtual environment and install dev-requirements:

```bash
make venv
```

2. Check Dockerfiles and code formatting with linters:

```base
make lint-all
```

3. Run tests:

```base
make test
```

## References

These images are based on the `jupyter/docker-stacks` images. [Refer to their documentation](https://jupyter-docker-stacks.readthedocs.io/en/latest/) for the full set of configuration options.
## License

MIT
