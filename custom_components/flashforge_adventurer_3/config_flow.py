# config_flow.py

from homeassistant import config_entries
from typing import Any, Dict, Optional
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import CONF_IP_ADDRESS, CONF_PORT, CONF_TYPE
from homeassistant.helpers import selector

from .const import CONF_PRINTERS, DEFAULT_PORT, DOMAIN, CONF_MODEL, AVAILABLE_MODELS

CONFIG_SCHEMA = vol.Schema({
    vol.Required(CONF_IP_ADDRESS): cv.string,
    vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.port,
    vol.Required(CONF_MODEL): selector.SelectSelector(
        selector.SelectSelectorConfig(options=AVAILABLE_MODELS)
    ),
})

class FlashForgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}
        if user_input is not None:
            if not errors:
                # Input is valid, set data.
                self.data = user_input
                self.data[CONF_PRINTERS] = []
                # Return the form of the next step.
                return self.async_create_entry(title=f'{user_input[CONF_MODEL]}', data=self.data)
        return self.async_show_form(
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )