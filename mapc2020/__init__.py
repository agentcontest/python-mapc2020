"""A client for the 2020/21 edition of the Multi-Agent Programming Contest."""

from __future__ import annotations

import asyncio
import logging
import json
import xml.etree.ElementTree as ET

from typing import Dict, Union

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
        self.status_updated = asyncio.Event()
        self.static = None
        self.dynamic = None
        self.status = None
        self.end = None

    def connection_made(self, transport):
        self.transport = transport
        self.fatal = None
        self.buffer.clear()
        self.disconnected.clear()
        self.sim_started.clear()
        self.action_requested.clear()
        self.status_updated.clear()
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
        elif message["type"] == "status-response":
            self.handle_status_response(message["content"])
        else:
            LOGGER.warning("%s: Unknown message type: %s", self, message["type"])

    def handle_auth_response(self, content):
        if content["result"] != "ok":
            self.fatal = AuthFailed()

    def handle_sim_start(self, content):
        self.static = content["percept"]
        self.sim_started.set()

    def handle_sim_end(self, content):
        self.end = content

    def handle_request_action(self, content):
        self.dynamic = content
        self.action_requested.set()

    def handle_bye(self, _content):
        self.fatal = Bye()

    def handle_status_response(self, content):
        self.status = content
        self.status_updated.set()

    async def send_action(self, tpe, params):
        await self.sim_started.wait()
        await self.action_requested.wait()
        self.action_requested.clear()
        self.send_message({
            "type": "action",
            "content": {
                "id": self.dynamic["id"],
                "type": tpe,
                "p": params,
            }
        })

    def _repr_svg_(self) -> str:
        vision = self.static["vision"]

        svg = ET.Element("svg", {
            "xmlns": "http://www.w3.org/2000/svg",
            "version": "1.2",
            "baseProfile": "tiny",
            "viewBox": f"{-vision} {-vision} {2 * vision + 1} {2 * vision + 1}",
        })

        # Fog of war.
        for x in range(-vision, vision + 1):
            for y in range(-vision, vision + 1):
                if abs(x) + abs(y) > vision:
                    ET.SubElement(svg, "rect", _attrs({
                        "x": x,
                        "y": y,
                        "width": 1,
                        "height": 1,
                        "fill": "black",
                        "opacity": "0.3",
                    }))

        # Agent.
        ET.SubElement(svg, "line", _attrs({
            "x1": 0.5,
            "y1": 0,
            "x2": 0.5,
            "y2": 1,
            "stroke": "black",
            "stroke-width": 0.2,
        }))
        ET.SubElement(svg, "line", _attrs({
            "x1": 0,
            "y1": 0.5,
            "x2": 1,
            "y2": 0.5,
            "stroke": "black",
            "stroke-width": 0.2,
        }))

        return ET.tostring(svg).decode("utf-8")

def _attrs(attrs: Dict[str, Union[str, int, float, None]]) -> Dict[str, str]:
    return {k: str(v) for k, v in attrs.items() if v is not None}
