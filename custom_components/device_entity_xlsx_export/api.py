"""Authenticated REST endpoints for the sidebar panel."""
from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.exceptions import ServiceValidationError
from .const import API_BASE
from .exporter import async_build_export, collect_device, list_devices

class DevicesView(HomeAssistantView):
    url = f"{API_BASE}/devices"; name = "api:device_entity_xlsx_export:devices"; requires_auth = True
    async def get(self, request):
        return self.json({"devices": list_devices(request.app["hass"])})

class EntitiesView(HomeAssistantView):
    url = f"{API_BASE}/entities"; name = "api:device_entity_xlsx_export:entities"; requires_auth = True
    async def get(self, request):
        try:
            device, rows = collect_device(request.app["hass"], request.query.get("device_id", ""), request.query.get("include_disabled", "true").lower() != "false")
            return self.json({"device": device, "entities": rows})
        except ServiceValidationError as err:
            return self.json({"error": str(err)}, status_code=400)

class ExportView(HomeAssistantView):
    url = f"{API_BASE}/export"; name = "api:device_entity_xlsx_export:export"; requires_auth = True
    async def post(self, request):
        try:
            data = await request.json()
            filename, content, _, _ = await async_build_export(request.app["hass"], device_id=str(data.get("device_id", "")), filename=data.get("filename"), include_disabled=bool(data.get("include_disabled", True)), include_attributes=bool(data.get("include_attributes", True)))
        except (ServiceValidationError, ValueError, TypeError) as err:
            return self.json({"error": str(err)}, status_code=400)
        return web.Response(body=content, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f'attachment; filename="{filename}"'})
