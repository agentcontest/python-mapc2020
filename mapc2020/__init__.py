"""A client for the 2020/21 edition of the Multi-Agent Programming Contest."""

from __future__ import annotations

import asyncio
import logging

__version__ = "0.1.0"  # Remember to update setup.py

LOGGER = logging.getLogger(__name__)

class AgentProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self.disconnected = asyncio.Event()

    def connection_made(self, transport):
        self.transport = transport
        self.disconnected.clear()
        LOGGER.info("%s: Connection made", self)

    def connection_lost(self, exc):
        LOGGER.info("%s: Connection lost (error: %s)", self, exc)
        self.disconnected.set()

    def data_received(self, data):
        print(data)
