"""Support for Video Storm IrUsb."""

from __future__ import annotations

import logging
import telnetlib  # pylint: disable=deprecated-module

import voluptuous as vol

from homeassistant.components import remote
from homeassistant.components.remote import (
    ATTR_NUM_REPEATS,
    DEFAULT_NUM_REPEATS,
    PLATFORM_SCHEMA as REMOTE_PLATFORM_SCHEMA,
)
from homeassistant.const import (
    CONF_DEVICES,
    CONF_HOST,
    CONF_MAC,
    CONF_NAME,
    CONF_PORT,
    DEVICE_DEFAULT_NAME,
)
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

DEFAULT_PORT = 9093
CONNECT_TIMEOUT = 5000
CONF_COMMANDS = "commands"
CONF_DATA = "data"

PLATFORM_SCHEMA = REMOTE_PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
    }
)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the IrUsb connection and devices."""
    name = config.get[CONF_NAME]
    host = config.get[CONF_HOST]
    port = config.get[CONF_PORT]

    remote = IrUsbRemote(name, host, port)
    add_entities([remote])


class IrUsbRemote(remote.RemoteEntity):
    """Device that sends commands to an IrUsb device."""

    def __init__(self, name, host, port):
        """Initialize device."""
        self._host = host
        self._port = port
        self._power = False
        self._name = name or DEVICE_DEFAULT_NAME

    def telnet_command(self, command):
        """Establish a telnet connection and sends `command`."""
        telnet = telnetlib.Telnet(self._host, self._port)
        _LOGGER.debug("Sending: %s", command)
        telnet.write(command.encode("ASCII") + b"\r")
        telnet.read_very_eager()  # skip response
        telnet.close()

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._power

    def turn_on(self) -> None:
        """Turn the device on."""
        self._power = True
        self.telnet_command("QWAKE")

    def turn_off(self) -> None:
        """Turn the device off."""
        self._power = False
        self.telnet_command("OFF")

    def up_arrow(self) -> None:
        """Up Arrow."""
        self.telnet_command("QHIDCODE1000082")

    def down_arrow(self) -> None:
        """Down Arrow."""
        self.telnet_command("QHIDCODE1000081")

    def left_arrow(self) -> None:
        """Left Arrow."""
        self.telnet_command("QHIDCODE1000080")

    def right_arrow(self) -> None:
        """Right Arrow."""
        self.telnet_command("QHIDCODE1000079")

    def enter_arrow(self) -> None:
        """Enter Arrow."""
        self.telnet_command("QHIDCODE1000040")

    def prev(self) -> None:
        """Previous."""
        self.telnet_command("QHIDCODE1000241")

    def play_pause(self) -> None:
        """Play/Pause."""
        self.telnet_command("QHIDCODE2000205")

    def skip(self) -> None:
        """Skip."""
        self.telnet_command("QHIDCODE1000242")

    def back(self) -> None:
        """Back."""
        self.telnet_command("QHIDCODE1000241")

    def Home(self) -> None:
        """Home."""
        self.telnet_command("QHIDCODE2002035")