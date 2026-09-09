# Device Entity XLSX Export

Home-Assistant-Custom-Integration für den komfortablen Excel-Export aller Entitäten eines Geräts. Version **0.2.0** bringt eine eigene Seite in der Home-Assistant-Seitenleiste und lädt die XLSX-Datei direkt im Browser herunter.

## Funktionen

- eigener Sidebar-Eintrag **Excel Export**
- übersichtliche Geräteauswahl mit Anzahl der zugeordneten Entitäten
- Vorschau aller Entity-Registry-Einträge des Geräts
- deaktivierte Entitäten werden standardmäßig angezeigt und exportiert
- direkter XLSX-Download im Browser, ohne File Editor oder Samba
- Live-Zustand, Einheit, Plattform, Device/State Class, Unique ID und Registry-Metadaten
- optionale State-Attribute als JSON
- zusätzliche Arbeitsblätter für Gerätedaten und Exportinformationen
- bisheriger Service `device_entity_xlsx_export.export_device` bleibt kompatibel und speichert weiterhin nach `/config/entity_exports/`

## Voraussetzungen

- Home Assistant 2026.8 oder neuer
- HACS
- ein Administrator-Konto für den Sidebar-Eintrag

## Installation über HACS

1. HACS öffnen.
2. Oben rechts **Benutzerdefinierte Repositories** wählen.
3. `https://github.com/Soul7495/Excel_Export_HA` als Repository und **Integration** als Kategorie eintragen.
4. **Device Entity XLSX Export** installieren.
5. Home Assistant neu starten.
6. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** nach **Device Entity XLSX Export** suchen und einmal hinzufügen.

Danach erscheint links **Excel Export**. Dort Gerät auswählen, optional die Entitäten prüfen und **Excel herunterladen** anklicken.

## Update von Version 0.1.x

1. In HACS bei **Device Entity XLSX Export** das Update auf `0.2.0` installieren (bei einem benutzerdefinierten Repository ggf. über das Drei-Punkte-Menü neu herunterladen).
2. Home Assistant vollständig neu starten.
3. Browser-Cache einmal hart aktualisieren (`Strg+F5`), falls der neue Sidebar-Eintrag noch die alte Oberfläche zeigt.
4. Falls die Integration noch nicht unter **Geräte & Dienste** eingerichtet ist, einmal hinzufügen.

Die alten Dateien in `/config/entity_exports/` bleiben unverändert. Für den neuen Browser-Download muss dieser Ordner nicht mehr geöffnet werden.

## Manueller Test

Den Ordner `custom_components/device_entity_xlsx_export` nach `/config/custom_components/device_entity_xlsx_export` kopieren und Home Assistant neu starten. Bei einem Update den vorhandenen Integrationsordner vollständig durch den neuen ersetzen, damit keine veralteten Dateien übrig bleiben.

## Service / Automationen

Der bisherige Service bleibt verfügbar:

```yaml
action: device_entity_xlsx_export.export_device
data:
  device_id: DEINE_DEVICE_ID
  filename: nibe_heat_pump.xlsx
  include_disabled: true
  include_attributes: true
```

Der Service schreibt die Datei nach `/config/entity_exports/`. Die Sidebar-Oberfläche erzeugt dieselben Arbeitsblätter, liefert die Datei aber direkt an den angemeldeten Browser aus.

## Architektur und Sicherheit

- Config Entry mit Einzelinstanz
- `panel_custom`-Sidebar-Panel als gebündeltes JavaScript-Modul
- authentifizierte Home-Assistant-HTTP-Endpunkte für Geräte, Entitäten und XLSX-Download
- kein externer Webdienst und keine Übertragung von Home-Assistant-Daten nach außen
- Formelschutz für Textwerte, die mit `=`, `+`, `-` oder `@` beginnen
- Dateinamen werden bereinigt; Pfadbestandteile werden nicht übernommen

## Entwicklung / Validierung

Vor einer Veröffentlichung sollten HACS Validation und Home Assistant Hassfest ausgeführt werden. Für die Aufnahme in das Standard-HACS-Verzeichnis gelten zusätzlich die jeweils aktuellen Anforderungen an Repository-Metadaten, Releases und Brand Assets.
