# Device Entity XLSX Export

Eine einfache Home-Assistant-Custom-Integration für HACS, die **alle Entitäten eines ausgewählten Geräts** als Excel-Datei (`.xlsx`) exportiert.

Besonders nützlich für Geräte wie **NIBE Heat Pump**, weil der Export aus der **Entity Registry** erzeugt wird. Dadurch können auch **deaktivierte Entitäten** exportiert werden, selbst wenn sie aktuell keinen State in Home Assistant besitzen.

## Funktionen

- Geräteauswahl direkt im Home-Assistant-Aktionsdialog
- XLSX-Export aller dem Gerät zugeordneten Entitäten
- deaktivierte Entitäten standardmäßig enthalten
- Live-State, Einheit, Device Class, State Class, Plattform, Unique ID usw.
- optionale State-Attribute als JSON
- zusätzliches Arbeitsblatt mit Geräteinformationen
- Export nach `/config/entity_exports/`
- Dateiname automatisch oder frei wählbar

## Voraussetzungen

- Home Assistant 2026.8 oder neuer
- HACS

## Installation über HACS als benutzerdefiniertes Repository

1. Dieses Repository zu GitHub hochladen.
2. In `custom_components/device_entity_xlsx_export/manifest.json` die beiden `REPLACE_ME`-Stellen durch deinen GitHub-Benutzernamen ersetzen.
3. In HACS oben rechts auf die drei Punkte gehen.
4. **Benutzerdefinierte Repositories** öffnen.
5. GitHub-URL des Repositorys eintragen.
6. Kategorie **Integration** wählen.
7. Repository hinzufügen und installieren.
8. Home Assistant neu starten.
9. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** nach `Device Entity XLSX Export` suchen und einmal hinzufügen.

## Manuelle Installation zum Testen

Den Ordner

`custom_components/device_entity_xlsx_export`

nach

`/config/custom_components/device_entity_xlsx_export`

kopieren und Home Assistant neu starten.

## Export ausführen

1. **Entwicklerwerkzeuge → Aktionen** öffnen.
2. Aktion `device_entity_xlsx_export.export_device` auswählen.
3. Bei **Gerät** z. B. `NIBE Heat Pump` auswählen.
4. `Deaktivierte Entitäten einschließen` aktiviert lassen.
5. Aktion ausführen.

Die Datei wird unter

`/config/entity_exports/`

gespeichert.

Beispiel:

`/config/entity_exports/nibe_heat_pump_20260909_104500.xlsx`

## YAML-Beispiel

```yaml
action: device_entity_xlsx_export.export_device
data:
  device_id: DEINE_DEVICE_ID
  filename: nibe_heat_pump.xlsx
  include_disabled: true
  include_attributes: true
```

## Spalten im Excel-Export

- Entity ID
- Name
- Zustand
- Einheit
- Domain
- Integration / Plattform
- Device Class
- State Class
- Entity Category
- Deaktiviert durch
- Ausgeblendet durch
- Aktuell geladen
- Letzte Zustandsänderung
- Letzte Aktualisierung
- Unique ID
- Config Entry ID
- Area ID
- Attribute (JSON), optional

## Entwicklung / Validierung

Das Repository enthält GitHub Actions für:

- HACS Validation
- Home Assistant Hassfest

Für eine Veröffentlichung in der regulären HACS-Liste sind zusätzlich die jeweils aktuellen HACS-Anforderungen wie Repository-Metadaten, Brand-Assets und ggf. Release/Einreichung zu beachten.
