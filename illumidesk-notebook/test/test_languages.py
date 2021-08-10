import docker
from docker.errors import ContainerError

import logging

import pytest


LOGGER = logging.getLogger(__name__)

PYTHON_VERSION = '3.9.5'
NOTEBOOK_IMAGE_TAG = f'python-{PYTHON_VERSION}'
NOTEBOOK_IMAGE_NAME = 'illumidesk/illumidesk-notebook'
NOTEBOOK_IMAGE = f'{NOTEBOOK_IMAGE_NAME}:{NOTEBOOK_IMAGE_TAG}'


@pytest.mark.parametrize(
    'language,version_output', [('python', ['Python', '3.9.5\n']),],
)
def test_languages(language, version_output):
    """Ensure that the language is available in the container's PATH and that
    it has the correct version
    """
    LOGGER.info(f'Test that language {language} {PYTHON_VERSION} is correctly installed ...')
    client = docker.from_env()
    output = client.containers.run(NOTEBOOK_IMAGE, f'{language} --version')
    output_decoded = output.decode('utf-8').split(' ')
    assert output_decoded[0:3] == version_output
    LOGGER.info(f'Output from command: {output_decoded[0:3]}')


def test_invalid_cmd():
    """Ensure that an invalid command returns a docker.errors.ContainerError"""
    with pytest.raises(ContainerError):
        LOGGER.info('Test an invalid command ...')
        client = docker.from_env()
        client.containers.run(NOTEBOOK_IMAGE, 'foo --version')
