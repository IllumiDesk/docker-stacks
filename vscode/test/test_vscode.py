import docker
from docker.errors import ContainerError

import logging

import pytest


LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    'cmd,version_output', [('code-server', '3.4.1 48f7c2724827e526eeaa6c2c151c520f48a61259',),],
)
def test_cmd(cmd, version_output):
    """Ensures that coder bin is found in the PATH and that it returns the correct
    version. Other tests verify the correct versions for npm and node.
    """
    LOGGER.info(f'Test that vscode {cmd} is correctly installed ...')
    client = docker.from_env()
    output = client.containers.run('illumidesk/vscode', f'{cmd} --version')
    output_decoded = output.decode('utf-8').split(' ')
    output_decoded = output.decode('utf-8').split('\n')
    LOGGER.info(f'Output from command: {output_decoded[2]}')
    assert output_decoded[2] == version_output


def test_invalid_command():
    """Ensure that an invalid command returns a docker.errors.ContainerError
    """
    with pytest.raises(ContainerError):
        LOGGER.info('Test an invalid command ...')
        client = docker.from_env()
        client.containers.run('illumidesk/vscode', 'foo --version')
