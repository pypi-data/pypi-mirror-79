#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

"""the actual control peer"""

import asyncio
import signal
from collections import defaultdict

from titanfe import log as logging
from titanfe.log import TitanLogAdapter, FlowContext
from . import grid_manager
from .runner import BrickRunner
from .webapi import WebApi

log = logging.getLogger(__name__)


class ControlPeer:
    """The control peer application will start runners as required for the flows/bricks
       as described in the given config file. Once the runners have registered themselves,
       they will get according assignments.
    """

    def __init__(self):
        logging.initialize(service="ControlPeer")

        self.loop = asyncio.get_event_loop()

        self.runners = {}
        self.runners_by_flow = defaultdict(set)

        self.api = WebApi(self)

    @classmethod
    def create(cls):
        """"Create control peer"""
        control_peer = cls()
        control_peer.install_signal_handlers()

        return control_peer

    def install_signal_handlers(self):
        signals = signal.SIGINT, signal.SIGTERM

        for sig in signals:
            signal.signal(sig, self.schedule_shutdown)

    async def run(self):
        """run the application"""
        try:
            await grid_manager.register(self.api.address)
        except Exception:  # pylint: disable=broad-except
            log.error("Failed to register, shutting down.", exc_info=True)
        else:
            await self.api.serve()

        log.info("Exit")

    def schedule_shutdown(self, sig, _):
        log.info(
            "Received signal %s - scheduling shutdown",
            signal.Signals(sig).name  # pylint: disable=no-member
        )
        asyncio.create_task(self.shutdown())

    async def shutdown(self):
        """shut down the controlpeer"""
        log.debug("Initiating shutdown")

        await self.api.stop()
        await self.stop_runners()

        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        log.debug("Cancelling outstanding tasks (%s)", len(tasks))

        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks)

    async def start_new_runner(self, brick):
        """update the configuration and start the flow"""
        try:
            await brick.base.install_or_update()

            runner = BrickRunner(brick, on_termination_cb=self.remove_runner)
            runner.start()
        except Exception as error:  # pylint: disable=broad-except
            logger = TitanLogAdapter(log, extra=FlowContext.from_brick(brick).asdict())
            logger.error("Failed to start runner for: %s", brick, exc_info=True)
            raise error

        self.runners[runner.uid] = runner
        self.runners_by_flow[brick.flow.uid].add(runner)

    def remove_runner(self, runner):
        log.debug("Runner %s terminated - remove.", runner)
        self.runners.pop(runner.uid)
        flow_runners = self.runners_by_flow.get(runner.brick.flow.uid, set())
        flow_runners.discard(runner)

    async def stop_runners(self, flow_uid=None):
        """ stop all runners or all runners for the given flow.uid """
        if flow_uid:
            log.debug("Stopping brick runners for Flow: %s", flow_uid)
            runners = self.runners_by_flow.pop(flow_uid, set())
        else:
            log.debug("Stopping all runners")
            runners = self.runners.values()

        await asyncio.gather(*[runner.stop() for runner in runners])
