"""A client for the 2020/21 edition of the Multi-Agent Programming Contest."""

from __future__ import annotations

import asyncio
import logging
import json

__version__ = "0.1.0"  # Remember to update setup.py

LOGGER = logging.getLogger(__name__)

class AgentException(RuntimeError):
    """Runtime error caused by misbehaving agent or simulation server."""

class AuthFailed(AgentException):
    """Server rejected agent credentials."""

class Bye(AgentException):
    """Server shut down."""

class AgentProtocol(asyncio.Protocol):
    def __init__(self, user: str, pw: str):
        self.user = user
        self.pw = pw

        self.transport = None
        self.buffer = bytearray()

        self.disconnected = asyncio.Event()
        self.fatal: AgentException = None

        self.sim_started = asyncio.Event()
        self.action_requested = asyncio.Event()
        self.static = None
        self.dynamic = None
        self.end = None

    def connection_made(self, transport):
        self.transport = transport
        self.fatal = None
        self.buffer.clear()
        self.disconnected.clear()
        self.sim_started.clear()
        self.action_requested.clear()
        LOGGER.info("%s: Connection made", self)

        self.send_message({
            "type": "auth-request",
            "content": {
                "user": self.user,
                "pw": self.pw,
            },
        })

    def send_message(self, message):
        LOGGER.debug("%s: << %s", self, message)
        self.transport.write(json.dumps(message).encode("utf-8") + b"\0")

    def connection_lost(self, exc):
        LOGGER.info("%s: Connection lost (error: %s)", self, exc)
        self.disconnected.set()

    def data_received(self, data):
        self.buffer.extend(data)
        while b"\0" in self.buffer:
            message_bytes, self.buffer = self.buffer.split(b"\0", 1)
            message = json.loads(message_bytes)
            LOGGER.debug("%s: >> %s", self, message)
            self.message_received(message)

    def message_received(self, message):
        if message["type"] == "auth-response":
            self.handle_auth_response(message["content"])
        elif message["type"] == "sim-start":
            self.handle_sim_start(message["content"])
        elif message["type"] == "sim-end":
            self.handle_sim_end(message["content"])
        elif message["type"] == "request-action":
            self.handle_request_action(message["content"])
        elif message["type"] == "bye":
            self.handle_bye(message["content"])
        else:
            LOGGER.warning("%s: Unknown message type: %s", self, message["type"])

    def handle_auth_response(self, content):
        if content["result"] != "ok":
            self.fatal = AuthFailed()

    def handle_sim_start(self, content):
        self.static = content
        self.sim_started.set()

    def handle_sim_end(self, content):
        self.end = content

    def handle_request_action(self, content):
        self.dynamic = content
        self.action_requested.set()

    def handle_bye(self, _content):
        self.fatal = Bye()
