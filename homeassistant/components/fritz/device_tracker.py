"""Support for FRITZ!Box routers."""
from fritzconnection.lib.fritzhosts import FritzHosts

from homeassistant.components.device_tracker.config_entry import ScannerEntity
from homeassistant.components.device_tracker.const import SOURCE_TYPE_ROUTER
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.entity import Entity

from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up device tracker for AVM FRITZ! component."""
    connection = hass.data[DOMAIN]["connection"]
    fritz = await self.hass.async_add_executor_job(FritzHosts, connection)
    async_add_entities([FritzScanner(fritz)])


class FritzScanner(Entity):
    self._fritz = None

    def __init__(self, connection):
        self._fritz = FritzHosts(fritz)

    async def async_update(self):
        self.hass.data[DOMAIN]["hosts"] = await self.hass.async_add_executor_job(
            self._fritz.get_hosts_info
        )


class FritzScannerEntity(ScannerEntity):
    self._mac = None
    self._info = None

    def __init__(self, mac):
        self._mac = mac

    async def async_update(self):
        self._info = self.hass.data[DOMAIN]["hosts"].get(self._mac, {})

    @property
    def is_connected(self):
        """Return true if the device is connected to the network."""
        return self._info.get("status") is not None

    @property
    def source_type(self):
        """Return the source type of the device."""
        return SOURCE_TYPE_ROUTER

    @property
    def name(self) -> str:
        """Return the name of the device."""
        return self._info.get("name")

    @property
    def unique_id(self) -> str:
        """Return a unique identifier for this device."""
        return self._mac

    @property
    def device_info(self):
        """Return a device description for device registry."""
        return {
            "connections": {(CONNECTION_NETWORK_MAC, self._mac)},
            "name": self.name,
        }
