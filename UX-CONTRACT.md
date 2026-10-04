# NIBE Control — UX Contract

## Canonical UI Map
| Capability | Canonical owner | Source of truth | Allowed variants | Verification |
|---|---|---|---|---|
| Navigation | interne Tab-Leiste | `src/nibe-control.js` | Übersicht / Verläufe / Datencheck / Diagnose | Tastatur + schmaler Viewport |
| Solltemperatur | `climate.set_temperature` | `src/profile.js` Allowlist | Range sowie Plus/Minus | Unit-Test + HA-Livetest |
| Select/Listbox | native Select-Auswahl | `water_heater.operation_list` | nur bei angebotenen Modi | Tastatur + HA-Livetest |
| Scrollbar | Komponenten-Root | `DESIGN.md` Runtime mapping | Browser-Standardgeometrie | statischer Audit |
| Historie | HA WebSocket History | `src/nibe-control.js` | 24 h / leere Historie / Fehler | Unit-Test + HA-Livetest |
| Entity Discovery | Entity Registry + Register-ID | `src/profile.js` | automatisch / manueller Override | Unit-Test |
| Feedback | Inline-Zustand | `UX-CONTRACT.md` | verfügbar / deaktiviert / fehlt / offline | Unit-Test + HA-Livetest |

## State behavior
- `unknown`, `unavailable` und fehlend werden als Gedankenstrich dargestellt.
- Deaktivierte empfohlene Entities erscheinen im Datencheck mit konkreter Anleitung.
- Statuscodes ohne belastbare Dokumentation werden als Rohcode bezeichnet.
- EVCC/PV sind optional und blockieren die NIBE-Ansicht nicht.
