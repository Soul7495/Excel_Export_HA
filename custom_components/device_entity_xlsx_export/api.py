"""HTTP API for the Device Entity XLSX Export sidebar panel."""
from __future__ import annotations

import secrets
import time
from typing import Any
from urllib.parse import quote

from aiohttp import web

from homeassistant.components.http import KEY_HASS, HomeAssistantView, require_admin
from homeassistant.exceptions import ServiceValidationError

from .const import API_BASE, DOMAIN, DOWNLOAD_TTL_SECONDS, MAX_PENDING_DOWNLOADS
from .exporter import async_build_export, collect_device, list_devices

XLSX_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def _device_ids(data: dict[str, Any]) -> list[str]:
    """Return device IDs from new multi-device or legacy single-device input."""
    value = data.get("device_ids")
    if isinstance(value, list):
        return [str(item) for item in value if item]
    legacy = data.get("device_id")
    return [str(legacy)] if legacy else []


def _download_store(hass) -> dict[str, dict[str, Any]]:
    """Return the temporary in-memory download store."""
    return hass.data.setdefault(DOMAIN, {}).setdefault("downloads", {})


def _cleanup_downloads(hass) -> None:
    """Discard expired downloads and cap memory usage."""
    store = _download_store(hass)
    now = time.monotonic()

    for token, item in list(store.items()):
        if item["expires_at"] <= now:
            store.pop(token, None)

    if len(store) <= MAX_PENDING_DOWNLOADS:
        return

    oldest = sorted(store.items(), key=lambda item: item[1]["created_at"])
    for token, _ in oldest[: len(store) - MAX_PENDING_DOWNLOADS]:
        store.pop(token, None)


def _attachment_headers(filename: str) -> dict[str, str]:
    """Build download headers with ASCII fallback and UTF-8 filename."""
    ascii_name = filename.encode("ascii", "ignore").decode("ascii") or "entity_export.xlsx"
    encoded_name = quote(filename, safe="")
    return {
        "Content-Disposition": (
            f'attachment; filename="{ascii_name}"; filename*=UTF-8\'\'{encoded_name}'
        ),
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Referrer-Policy": "no-referrer",
        "X-Content-Type-Options": "nosniff",
    }


class DevicesView(HomeAssistantView):
    """Return devices that have entity-registry entries."""

    url = f"{API_BASE}/devices"
    name = "api:device_entity_xlsx_export:devices"
    requires_auth = True

    @require_admin
    async def get(self, request: web.Request) -> web.Response:
        """Return available devices for the export UI."""
        return self.json({"devices": list_devices(request.app[KEY_HASS])})


class EntitiesView(HomeAssistantView):
    """Return entity-registry entries for a selected device."""

    url = f"{API_BASE}/entities"
    name = "api:device_entity_xlsx_export:entities"
    requires_auth = True

    @require_admin
    async def get(self, request: web.Request) -> web.Response:
        """Return the selected device and its entities."""
        try:
            device_ids = request.query.getall("device_id", [])
            devices = []
            rows = []
            for device_id in dict.fromkeys(device_ids):
                device, device_rows = collect_device(
                    request.app[KEY_HASS],
                    device_id,
                    request.query.get("include_disabled", "true").lower() != "false",
                )
                devices.append(device)
                rows.extend(device_rows)
            if not devices:
                collect_device(request.app[KEY_HASS], "")
            return self.json({"devices": devices, "entities": rows})
        except ServiceValidationError as err:
            return self.json({"error": str(err)}, status_code=400)


class ExportView(HomeAssistantView):
    """Return a workbook directly for backwards compatibility."""

    url = f"{API_BASE}/export"
    name = "api:device_entity_xlsx_export:export"
    requires_auth = True

    @require_admin
    async def post(self, request: web.Request) -> web.Response:
        """Build and return an XLSX response in one request."""
        try:
            data = await request.json()
            filename, content, _, _ = await async_build_export(
                request.app[KEY_HASS],
                device_ids=_device_ids(data),
                filename=data.get("filename"),
                include_disabled=bool(data.get("include_disabled", True)),
                include_attributes=bool(data.get("include_attributes", True)),
            )
        except (ServiceValidationError, ValueError, TypeError) as err:
            return self.json({"error": str(err)}, status_code=400)

        return web.Response(
            body=content,
            content_type=XLSX_CONTENT_TYPE,
            headers=_attachment_headers(filename),
        )


class ExportPrepareView(HomeAssistantView):
    """Create a short-lived HTTP download URL for browsers and Companion apps."""

    url = f"{API_BASE}/prepare"
    name = "api:device_entity_xlsx_export:prepare"
    requires_auth = True

    @require_admin
    async def post(self, request: web.Request) -> web.Response:
        """Prepare an XLSX file and return a temporary download URL."""
        hass = request.app[KEY_HASS]
        try:
            data = await request.json()
            filename, content, count, device_name = await async_build_export(
                hass,
                device_ids=_device_ids(data),
                filename=data.get("filename"),
                include_disabled=bool(data.get("include_disabled", True)),
                include_attributes=bool(data.get("include_attributes", True)),
            )
        except (ServiceValidationError, ValueError, TypeError) as err:
            return self.json({"error": str(err)}, status_code=400)

        _cleanup_downloads(hass)
        token = secrets.token_urlsafe(32)
        now = time.monotonic()
        _download_store(hass)[token] = {
            "filename": filename,
            "content": content,
            "created_at": now,
            "expires_at": now + DOWNLOAD_TTL_SECONDS,
        }
        _cleanup_downloads(hass)

        return self.json(
            {
                "filename": filename,
                "download_url": f"{API_BASE}/download/{token}",
                "expires_in": DOWNLOAD_TTL_SECONDS,
                "entity_count": count,
                "device": device_name,
            }
        )


class DownloadView(HomeAssistantView):
    """Serve a short-lived workbook over a normal HTTP(S) download."""

    url = f"{API_BASE}/download/{{token}}"
    name = "api:device_entity_xlsx_export:download"
    # The unguessable, short-lived token is the credential for this endpoint.
    # A normal authenticated API request is deliberately not required here so
    # mobile WebViews can hand the URL to their native download handler.
    requires_auth = False

    async def get(self, request: web.Request, token: str) -> web.Response:
        """Return the prepared workbook while its token is still valid."""
        hass = request.app[KEY_HASS]
        _cleanup_downloads(hass)
        item = _download_store(hass).get(token)

        if item is None or item["expires_at"] <= time.monotonic():
            return web.Response(
                status=404,
                text="Download link expired. Create a new Excel export in Home Assistant.",
                headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"},
            )

        return web.Response(
            body=item["content"],
            content_type=XLSX_CONTENT_TYPE,
            headers=_attachment_headers(item["filename"]),
        )
