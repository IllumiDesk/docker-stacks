[![Test Docker Image Status](https://github.com/illumidesk/docker-stacks/workflows/Test%20and%20Build/badge.svg)](https://github.com/illumidesk/docker-stacks/actions?query=branch%3Amain+workflow%3A%22Test+and+Build%22)

# IllumiDesk Docker Stacks

Dockerfiles and related assets for IllumiDesk's workspace images. The purpose of this repo is to provide a template repo for IllumiDesk customer-centric images. To create a new customer-centric repo, click on the Use this Template button and confirm the repo name.

## Pre Requisits

- [Docker](https://docs.docker.com/get-docker/)
- [Python 3.7+](https://www.python.org/downloads/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html#installation)

## Quickstart

1. Install dependencies:

```bash
make venv
```

2. Build images

```bash
make build-all
```

You can also override default owner, tags, and use other docker arguments with the make
command included in this repo. Type `make` from the root of this repo to confirm a complete
list of options.

For example running:

```bash
make OWNER=foo TAG=mytag build/illumidesk-notebook
```

Would create the image `foo/illumides-notebook:mytag`. More advanced options are available with the `DARGS`
option which is an alias for the `--build-args` flag.

> NOTE: You can use the native `docker` commands to build, push, and tag images (among others). The `make` command
is provided as a convenience and is used with GitHub Actions for automation.

3. Run:

Running the image standalone is helpful for testing:

```bash
make dev
```

Or:

```bash
docker run -p 8888:8888 illumidesk/illumidesk-notebook:latest
```

Then, navigate to `http://127.0.0.1:8888` to access your Jupyter Notebook server.

> Refer to [docker's documentation](https://docs.docker.com/engine/reference/run/) for additional `docker run ...` options.

4. Test:

```bash
make test
```
## Development and Testing

1. Create your virtual environment and install dev-requirements:

```bash
make venv
```

2. Run tests:

The standard `make test` command ensures the image is linted and built before running tests:

```bash
make test
```

You can skip the build step and run the tests directly from the root of this repo:

```bash
pytest -v
```

## References

These images are based on the `jupyter/docker-stacks` images. [Refer to their documentation](https://jupyter-docker-stacks.readthedocs.io/en/latest/) for the full set of configuration options.

## License

MIT
