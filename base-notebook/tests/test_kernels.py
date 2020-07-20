# Souced from:
# https://github.com/jupyter/docker-stacks/blob/d3ef6d89b2f8b9062a57f9c7856b2b91fc9298f0/datascience-notebook/test/test_julia.py
import logging

from typing import Container


LOGGER = logging.getLogger(__name__)


KERNELS = ['java', 'julia', 'python', 'R']


def test_kernels(container: Container) -> bool:
    """Basic kernels test, loops through KERNELS list and test --version
    flag for each kernel"""
    for kernel in KERNELS:
        LOGGER.info(f'Test that kernel {kernel} is correctly installed ...')
        running_container = container.run(
            tty=True, command=['start.sh', 'bash', '-c', 'sleep infinity']
        )
        command = f'{kernel} --version'
        cmd = running_container.exec_run(command)
        output = cmd.output.decode('utf-8')
        assert cmd.exit_code == 0, f'Command {command} failed {output}'
        LOGGER.debug(output)
