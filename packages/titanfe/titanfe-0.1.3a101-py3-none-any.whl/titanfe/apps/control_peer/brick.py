#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

"""A Brick"""

import re
import shutil
from collections import namedtuple
from datetime import datetime
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from aiohttp import ClientError
from ruamel import yaml
from ruamel.yaml import YAMLError

from titanfe import log as logging
from .package_manager import package_manager
from ...config import configuration

Flow = namedtuple("Flow", ("uid", "name"))
Connections = namedtuple("Connections", ("input", "output"))

RuntimeParameters = namedtuple(
    "RuntimeParameters",
    ("autoscale_max_instances", "autoscale_queue_level", "exit_after_idle_seconds"),
)


class BrickBaseDefinition:
    """
    The general definition of a brick contains it's name and id, as well as the module itself
    and possibly a set of default parameters for that module read from the annexed config.yaml
    """

    def __init__(self, uid, name, family, logger):
        self.uid = uid
        self.name = name
        self.family = family

        self.log = logger

        self.module_path = None
        self.guess_module_path()

        self.default_parameters = {}
        self.load_default_parameters()

    def guess_module_path(self):
        """
        The module is expected to be found in the configured brick_folder extended with the brick-ID
        and should be either a folder or python file having the same name as the brick.
        """

        module_parent = Path(configuration.brick_folder) / self.uid

        try:
            self.module_path = next(
                path
                for path in module_parent.iterdir()
                if re.match(f"^{self.name}(?:\\.py)?$", path.name, re.IGNORECASE)
            )
        except (FileNotFoundError, StopIteration):
            self.log.info("Missing module `%s/` or `%s.py`", self.name, self.name)

    def load_default_parameters(self):
        """ load default parameters from config.yaml (if any) """
        if not self.module_path:
            return

        default_parameters = {}
        config_path = self.module_path.parent / "config.yml"
        try:
            with open(config_path) as config_file:
                default_parameters = yaml.safe_load(config_file)
        except OSError as error:
            self.log.debug("Failed to open config file: %s -> %s", config_path, error)
        except YAMLError as error:
            self.log.error("Failed to parse config file: %s -> %s", config_path, error)

        self.default_parameters = default_parameters

    def __repr__(self):
        return (
            f"Base({self.uid}, {self.name}, "
            f"module_path={self.module_path}, "
            f"default_parameters={self.default_parameters})"
        )

    async def install_or_update(self, update=True, force_update=False):
        """ Get a brick from the package manager and install it"""
        module_parent = Path(configuration.brick_folder)
        destination = module_parent / self.uid

        if destination.exists():
            self.log.debug("Brick %s is already present", self.uid)

            if not update:
                return

            if not force_update:
                try:
                    last_modified_remote = await package_manager.get_last_modified(self.uid)
                except ClientError:
                    self.log.warning(
                        "Failed to read remote timestamp, continue without brick update",
                        exc_info=True,
                    )
                    return

                last_modified_local = destination.stat().st_mtime
                if datetime.utcfromtimestamp(last_modified_local) >= \
                        datetime.utcfromtimestamp(last_modified_remote):
                    return

            shutil.rmtree(destination)

        destination.mkdir(parents=True, exist_ok=True)

        source = await package_manager.get_source_files(self.uid)

        if not source:
            return

        with ZipFile(BytesIO(source), "r") as compressed:
            self.log.debug("compressed brick content: %s", compressed.printdir())
            compressed.extractall(path=destination)

        self.log.info(
            "installed/updated source files for brick %s into %s",
            self.uid,
            list(destination.iterdir()),
        )
        self.guess_module_path()
        self.load_default_parameters()


class BrickInstanceDefinition:
    """
    The Brick Instance Definition is a fully configured brick in a flow context.
    It should have it's own name and uid within the flow, precise parameters
    and possibly connections to other bricks.
    """

    def __init__(
        self,
        uid,
        name,
        flow: Flow,
        base: BrickBaseDefinition,
        processing_parameters: dict,
        runtime_parameters: RuntimeParameters,
        connections: Connections,
    ):
        self.flow = flow
        self.uid = uid
        self.name = name
        self.base = base

        self.processing_parameters = {**self.base.default_parameters, **processing_parameters}
        self.runtime_parameters = runtime_parameters
        self.connections = connections

    def __repr__(self):
        return (
            f"Brick({self.uid}, {self.name}, flow={self.flow}, "
            f"base={self.base}, "
            f"processing_parameters={self.processing_parameters}, "
            f"runtime_parameters={self.runtime_parameters}, "
            f")"
        )

    def __hash__(self):
        return hash(self.uid)

    def __eq__(self, other):
        if isinstance(other, BrickInstanceDefinition):
            return other.uid == self.uid
        return False

    @ classmethod
    def from_gridmanager(cls, brick_description):
        """Add brick configuration using default and flow-specific parameters if available"""
        config = brick_description["Configuration"]
        instance_uid = config["instanceId"]
        instance_name = config["name"]

        flow = Flow(brick_description["FlowID"], brick_description["FlowName"])

        logger = logging.getLogger(
            __name__, context=logging.FlowContext(*flow, instance_uid, instance_name)
        )

        base = BrickBaseDefinition(config["id"], config["brick"], config["family"], logger)
        runtime_params = RuntimeParameters(*[config[f] for f in RuntimeParameters._fields])
        processing_params = config["parameters"]
        connections = Connections(brick_description["Inbound"], brick_description["Outbound"])

        instance = cls(
            instance_uid, instance_name, flow, base, processing_params, runtime_params, connections
        )
        return instance
