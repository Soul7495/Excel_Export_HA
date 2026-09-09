"""Config flow for Device Entity XLSX Export."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN


class DeviceEntityXlsxExportConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Device Entity XLSX Export."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(
                title="Device Entity XLSX Export",
                data={},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
        )
