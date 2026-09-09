"""Device Entity XLSX Export integration."""
from pathlib import Path
import voluptuous as vol
from homeassistant.components import frontend, panel_custom
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType
from .api import DevicesView, EntitiesView, ExportView
from .const import *
from .exporter import async_export_to_disk

SERVICE_SCHEMA = vol.Schema({vol.Required(ATTR_DEVICE_ID): cv.string, vol.Optional(ATTR_FILENAME): cv.string, vol.Optional(ATTR_INCLUDE_DISABLED, default=True): cv.boolean, vol.Optional(ATTR_INCLUDE_ATTRIBUTES, default=True): cv.boolean})

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    data = hass.data.setdefault(DOMAIN, {})
    if not data.get("http_registered"):
        await hass.http.async_register_static_paths([StaticPathConfig(f"/{DOMAIN}", str(Path(__file__).parent / "frontend"), True)])
        for view in (DevicesView, EntitiesView, ExportView):
            hass.http.register_view(view)
        data["http_registered"] = True
    if not hass.services.has_service(DOMAIN, SERVICE_EXPORT_DEVICE):
        async def handle(call: ServiceCall):
            result = await async_export_to_disk(hass, device_id=call.data[ATTR_DEVICE_ID], filename=call.data.get(ATTR_FILENAME), include_disabled=call.data[ATTR_INCLUDE_DISABLED], include_attributes=call.data[ATTR_INCLUDE_ATTRIBUTES])
            return result if call.return_response else None
        hass.services.async_register(DOMAIN, SERVICE_EXPORT_DEVICE, handle, schema=SERVICE_SCHEMA, supports_response=SupportsResponse.OPTIONAL)
    if PANEL_URL_PATH not in hass.data.get("frontend_panels", {}):
        await panel_custom.async_register_panel(hass, webcomponent_name="device-entity-xlsx-export-panel", frontend_url_path=PANEL_URL_PATH, module_url=f"/{DOMAIN}/panel.js?v=0.2.0", sidebar_title=PANEL_TITLE, sidebar_icon=PANEL_ICON, require_admin=True, config={}, config_panel_domain=DOMAIN)
    data["entry_id"] = entry.entry_id
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    frontend.async_remove_panel(hass, PANEL_URL_PATH)
    hass.services.async_remove(DOMAIN, SERVICE_EXPORT_DEVICE)
    hass.data.get(DOMAIN, {}).pop("entry_id", None)
    return True
