# source from:
# https://github.com/jupyter/docker-stacks/blob/8de52359adc001426731c0f5fb42406393e4d9b8/test/helpers.py
#
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
#
# CondaPackageHelper is partially based on the work https://oerpli.github.io/post/2019/06/conda-outdated/.
# MIT Licensed

from collections import defaultdict
from itertools import chain
import json
import logging
import re

from tabulate import tabulate

from typing import Container


LOGGER = logging.getLogger(__name__)


class CondaPackageHelper:
    """Conda package helper permitting to get information about packages
    """

    def __init__(self, container: Container) -> None:
        # if isinstance(container, TrackedContainer):
        self.running_container = CondaPackageHelper.start_container(container)
        self.specs = None
        self.installed = None
        self.available = None
        self.comparison = None

    @staticmethod
    def _conda_export_command(from_history=False) -> str:
        """Return the conda export command with or without history"""
        cmd = ["conda", "env", "export", "-n", "base", "--json", "--no-builds"]
        if from_history:
            cmd.append("--from-history")
        return cmd

    @staticmethod
    def _extract_available(lines):
        """Extract packages and versions from the lines returned by the list of packages"""
        ddict = defaultdict(set)
        for line in lines.splitlines()[2:]:
            pkg, version = re.match(r"^(\S+)\s+(\S+)", line, re.MULTILINE).groups()
            ddict[pkg].add(version)
        return ddict

    @staticmethod
    def _packages_from_json(env_export: dict) -> dict:
        """Extract packages and versions from the lines returned by the list of specifications"""
        # dependencies = filter(lambda x:  isinstance(x, str), json.loads(env_export).get("dependencies"))
        dependencies = json.loads(env_export).get("dependencies")
        # Filtering packages installed through pip in this case it's a dict {'pip': ['toree==0.3.0']}
        # Since we only manage packages installed through conda here
        dependencies = filter(lambda x: isinstance(x, str), dependencies)
        packages_dict = dict()
        for split in map(lambda x: x.split("=", 1), dependencies):
            # default values
            package = split[0]
            version = set()
            # cheking if it's a proper version by testing if the first char is a digit
            if len(split) > 1:
                if split[1][0].isdigit():
                    # package + version case
                    version = set(split[1:])
                else:
                    # The split was incorrect and the package shall not be splitted
                    package = f"{split[0]}={split[1]}"
            packages_dict[package] = version
        return packages_dict

    @staticmethod
    def semantic_cmp(version_string: str) -> tuple:
        """Manage semantic versioning for comparison"""

        def mysplit(string):
            version_substrs = lambda x: re.findall(r"([A-z]+|\d+)", x)
            return list(chain(map(version_substrs, string.split("."))))

        def str_ord(string):
            num = 0
            for char in string:
                num *= 255
                num += ord(char)
            return num

        def try_int(version_str):
            try:
                return int(version_str)
            except ValueError:
                return str_ord(version_str)

        mss = list(chain(*mysplit(version_string)))
        return tuple(map(try_int, mss))

    @staticmethod
    def start_container(container: Container) -> bytes:
        """Start the TrackedContainer and return an instance of a running container"""
        LOGGER.info(f"Starting container {container.image_name} ...")
        return container.run(
            tty=True, command=["start.sh", "bash", "-c", "sleep infinity"]
        )

    def _execute_command(self, command):
        """Execute a command on a running container"""
        rc = self.running_container.exec_run(command)
        return rc.output.decode("utf-8")

    def available_packages(self):
        """Return the available packages"""
        if self.available is None:
            LOGGER.info("Grabing the list of available packages (can take a while) ...")
            # Keeping command line output since `conda search --outdated --json` is way too long ...
            self.available = CondaPackageHelper._extract_available(
                self._execute_command(["conda", "search", "--outdated"])
            )
        return self.available

    def check_updatable_packages(self, specifications_only: bool = True):
        """Check the updatables packages including or not dependencies"""
        specs = self.specified_packages()
        installed = self.installed_packages()
        available = self.available_packages()
        self.comparison = list()
        for pkg, inst_vs in self.installed.items():
            if not specifications_only or pkg in specs:
                avail_vs = sorted(
                    list(available[pkg]), key=CondaPackageHelper.semantic_cmp
                )
                if not avail_vs:
                    continue
                current = min(inst_vs, key=CondaPackageHelper.semantic_cmp)
                newest = avail_vs[-1]
                if avail_vs and current != newest:
                    if CondaPackageHelper.semantic_cmp(
                        current
                    ) < CondaPackageHelper.semantic_cmp(newest):
                        self.comparison.append(
                            {"Package": pkg, "Current": current, "Newest": newest}
                        )
        return self.comparison

    def get_outdated_summary(self, specifications_only: bool = True):
        """Return a summary of outdated packages"""
        if specifications_only:
            nb_packages = len(self.specs)
        else:
            nb_packages = len(self.installed)
        nb_updatable = len(self.comparison)
        updatable_ratio = nb_updatable / nb_packages
        return f"{nb_updatable}/{nb_packages} ({updatable_ratio:.0%}) packages could be updated"

    def get_outdated_table(self):
        """Return a table of outdated packages"""
        return tabulate(self.comparison, headers="keys")

    def installed_packages(self) -> dict:
        """Return the installed packages"""
        if self.installed is None:
            LOGGER.info("Grabing the list of installed packages ...")
            self.installed = CondaPackageHelper._packages_from_json(
                self._execute_command(CondaPackageHelper._conda_export_command())
            )
        return self.installed

    def specified_packages(self):
        """Return the specifications (i.e. packages installation requested)"""
        if self.specs is None:
            LOGGER.info("Grabing the list of specifications ...")
            self.specs = CondaPackageHelper._packages_from_json(
                self._execute_command(CondaPackageHelper._conda_export_command(True))
            )
        return self.specs
