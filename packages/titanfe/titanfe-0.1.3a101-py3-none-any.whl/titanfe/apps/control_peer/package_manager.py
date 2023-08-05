#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#
"""Install a Brick"""
from http import HTTPStatus

from aiohttp.client_exceptions import ClientError
from aiohttp_requests import requests

from titanfe import log as logging
from titanfe.config import configuration

log = logging.getLogger(__name__)


class PackageManagerError(ClientError):
    pass


class PackageManager:
    """ handle all requests to the package manager """
    @property
    def address(self):
        return f"{configuration.packagemanager_address}/bricks/"

    async def get(self, endpoint, context):
        response = await requests.get(self.address + endpoint)
        if response.status != HTTPStatus.OK:
            raise PackageManagerError(f"{context} failed: {response!r}")

        return await response.read()

    async def get_source_files(self, brick_id):
        """get the source files archive from the package manager"""
        return await self.get(brick_id, "Downloading source files")

    async def get_last_modified(self, brick_id):
        """get the source files archive from the package manager"""
        response = await self.get(
            f"{brick_id}/lastmodified",
            f"Getting timestamp of last modification for remote package: {brick_id}",
        )

        return float(response)


package_manager = PackageManager()  # pylint: disable=invalid-name
