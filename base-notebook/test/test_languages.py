import docker
from docker.errors import ContainerError

import logging

import pytest


LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    'language,version_output',
    [
        ('java', ['openjdk', '11.0.7', '2020-04-14\nOpenJDK',],),
        ('julia', ['julia', 'version', '1.4.1\n']),
        ('python', ['Python', '3.7.6\n']),
        ('R', ['R', 'version', '3.6.3',],),
    ],
)
def test_languages(language, version_output):
    """Ensure that the language is available in the container's PATH and that
    it has the correct version
    """
    LOGGER.info(f'Test that language {language} is correctly installed ...')
    client = docker.from_env()
    output = client.containers.run('illumidesk/base-notebook', f'{language} --version')
    output_decoded = output.decode('utf-8').split(' ')
    assert output_decoded[0:3] == version_output
    LOGGER.info(f'Output from command: {output_decoded[0:3]}')


def test_invalid_cmd():
    """Ensure that an invalid command returns a docker.errors.ContainerError
    """
    with pytest.raises(ContainerError):
        LOGGER.info(f'Test an invalid command ...')
        client = docker.from_env()
        client.containers.run('illumidesk/base-notebook', 'foo --version')
