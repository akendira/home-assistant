"""Support for AVM FRITZ! devices."""
from fritzconnection.core.fritzconnection import FritzConnection
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType, HomeAssistantType

from .const import DOMAIN

DEFAULT_HOST = "169.254.1.1"
DEFAULT_USERNAME = "admin"
PLATFORMS = ["device_tracker"]


def ensure_unique_hosts(value):
    """Validate that all configs have a unique host."""
    vol.Schema(vol.Unique("duplicate host entries found"))(
        [entry[CONF_HOST] for entry in value]
    )
    return value


CONFIG_SCHEMA = vol.Schema(
    vol.All(
        cv.deprecated(DOMAIN),
        {
            DOMAIN: vol.All(
                cv.ensure_list,
                [
                    vol.Schema(
                        {
                            vol.Required(CONF_HOST, default=DEFAULT_HOST): cv.string,
                            vol.Required(CONF_PASSWORD): cv.string,
                            vol.Required(
                                CONF_USERNAME, default=DEFAULT_USERNAME
                            ): cv.string,
                        }
                    )
                ],
                ensure_unique_hosts,
            )
        },
    ),
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistantType, config: ConfigType) -> bool:
    """Set up the AVM FRITZ! component."""

    if DOMAIN in config:
        hass.data[DOMAIN] = []

        for entry_config in config[DOMAIN]:
            hass.async_create_task(
                hass.config_entries.flow.async_init(
                    DOMAIN, context={"source": "import"}, data=entry_config
                )
            )

    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
    """Set up the AVM FRITZ! platform."""
    host = entry.data[CONF_HOST]
    user = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    fritz = FritzConnection(address=host, user=user, password=password)
    hass.data[DOMAIN].append(fritz)
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, DOMAIN))

    return True
