# Changelog

All notable changes to **Device Entity XLSX Export** are documented here.

## [0.3.1] - 2026-10-04

### Fixed
- Prevented XLSX downloads from navigating the custom panel back to the Home Assistant start dashboard.
- Kept the normal HTTP download flow for desktop browsers and mobile Companion App WebViews, including the visible fallback link.

## [0.3.0] - 2026-10-03

### Fixed
- Replaced the Blob-based XLSX download used by the sidebar with a normal HTTP(S) file download to improve compatibility with the Home Assistant Companion App and mobile WebViews.
- Added a visible **Datei herunterladen** fallback when an automatic download is blocked.

### Added
- Short-lived, cryptographically random download tokens.
- 10-minute expiry for prepared downloads.
- In-memory download cache capped at 20 prepared files.
- Server-side administrator checks for device, entity and export preparation endpoints.
- HACS validation and Home Assistant hassfest GitHub Actions.

### Compatibility
- The existing `device_entity_xlsx_export.export_device` action remains available and continues to write files to `/config/entity_exports/`.
- Desktop browser behavior remains supported.

## [0.2.0]

### Added
- Home Assistant sidebar panel.
- Device selection and entity preview.
- Direct XLSX export from the panel.
- Disabled Entity Registry entries can be included in exports.
