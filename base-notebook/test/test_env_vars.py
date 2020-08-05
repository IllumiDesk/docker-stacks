import docker
from docker.errors import ContainerError

import logging

import pytest


LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    'env_var',
    [
        ('NB_UID=1000'),
        ('NB_GID=100'),
        ('PATH=/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'),
        ('DEBIAN_FRONTEND=noninteractive'),
        ('CONDA_DIR=/opt/conda'),
        ('SHELL=/bin/bash'),
        ('NB_USER=jovyan'),
        ('LC_ALL=en_US.UTF-8'),
        ('LANG=en_US.UTF-8'),
        ('LANGUAGE=en_US.UTF-8'),
        ('HOME=/home/jovyan'),
        ('MINICONDA_MD5=d63adf39f2c220950a063e0529d4ff74'),
        ('XDG_CACHE_HOME=/home/jovyan/.cache/'),
        ('JULIA_DEPOT_PATH=/opt/julia'),
        ('JULIA_PKGDIR=/opt/julia'),
        ('JULIA_VERSION=1.4.1'),
        ('JHUB_HASH_COMMIT=f3c3225124f1c5d9acb2503ec4d9c35a140f6a78'),
        ('JUPYTER_ENABLE_LAB=yes'),
        ('RESTARTABLE=yes')
    ],
)
def test_env_vars(env_var):
    """Ensure that the environment variables are correctly set
    """
    LOGGER.info(f'Test that the {env_var} is correctly set ...')
    client = docker.from_env()
    output = client.containers.run(
        'illumidesk/base-notebook',
        command='env',
        stdout=True)
    output_decoded = output.decode('utf-8').split('\n')
    if env_var in output_decoded:
        LOGGER.info(f'env var {env_var} is in {output_decoded}')
    else:
        LOGGER.info(f'env var {env_var} not in {output_decoded}')
    assert env_var in output_decoded
    LOGGER.info(f'Output from command: {output_decoded[0]}')
