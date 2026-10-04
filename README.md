# Device Entity XLSX Export

Home-Assistant-Custom-Integration für den komfortablen Excel-Export aller Entitäten eines Geräts.

Version **0.3.0** verbessert den Download in der Home-Assistant-Companion-App. Statt die XLSX-Datei nur als Browser-Blob zu erzeugen, erstellt die Integration jetzt einen kurzlebigen echten HTTP(S)-Download-Link. Das ist insbesondere für Android/iOS-WebViews zuverlässiger.

## Funktionen

- eigener Sidebar-Eintrag **Excel Export**
- übersichtliche Geräteauswahl mit Anzahl der zugeordneten Entitäten
- Vorschau aller Entity-Registry-Einträge des Geräts
- deaktivierte Entitäten werden standardmäßig angezeigt und exportiert
- direkter XLSX-Download im Browser
- verbesserter Download in der Home-Assistant-Companion-App ab v0.3.0
- sichtbarer Download-Link als Fallback, falls ein automatischer Download blockiert wird
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

Danach erscheint links **Excel Export**. Dort Gerät auswählen und **Excel erstellen** anklicken. Der Download wird automatisch gestartet. Falls die Companion-App den automatischen Start blockiert, bleibt darunter der Button **Datei herunterladen** sichtbar.

## Update auf Version 0.3.0

1. In HACS **Device Entity XLSX Export** neu herunterladen/aktualisieren.
2. Home Assistant vollständig neu starten.
3. Falls noch die alte Oberfläche geladen wird, App bzw. Browser einmal vollständig schließen und erneut öffnen.
4. In der Companion-App anschließend unter **Excel Export** einen neuen Export erzeugen.

Der erzeugte Download-Link ist bewusst nur **10 Minuten** gültig und enthält ein zufälliges Token. Die XLSX-Datei wird dafür temporär ausschließlich im Arbeitsspeicher von Home Assistant gehalten und nicht öffentlich abgelegt.

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

Der Service schreibt die Datei weiterhin nach `/config/entity_exports/`. Die Sidebar-Oberfläche nutzt dagegen den direkten Download.

## Architektur und Sicherheit

- Config Entry mit Einzelinstanz
- `panel_custom`-Sidebar-Panel als gebündeltes JavaScript-Modul
- authentifizierte Home-Assistant-HTTP-Endpunkte für Geräte, Entitäten und das Erzeugen eines Downloads
- Geräte-/Entity-/Export-Endpunkte sind zusätzlich serverseitig auf Administratoren beschränkt
- zufälliger, kurzlebiger Download-Token für den eigentlichen Dateiabruf
- Download-Cache nur im RAM, maximal 20 vorbereitete Dateien gleichzeitig
- keine Übertragung von Home-Assistant-Daten an externe Dienste
- Formelschutz für Textwerte, die mit `=`, `+`, `-` oder `@` beginnen
- Dateinamen werden bereinigt; Pfadbestandteile werden nicht übernommen

## v0.3.0 – Mobile-Download-Fix

Die vorherige v0.2.0 lud die erzeugte XLSX-Datei per `fetch()` als Blob und startete danach programmgesteuert einen `<a download>`-Klick. Dieser Ablauf kann in eingebetteten WebViews, insbesondere in Companion-Apps, blockiert oder anders behandelt werden.

v0.3.0 erzeugt stattdessen nach erfolgreicher Authentifizierung einen temporären Download-Link auf dem Home-Assistant-Server. Dadurch sieht die Companion-App einen normalen HTTP(S)-Dateidownload mit `Content-Disposition: attachment`. Falls ein automatischer Start nicht funktioniert, kann derselbe Link über den sichtbaren Download-Button erneut aufgerufen werden.


## Validierung

Das Repository enthält GitHub Actions für **HACS validation** und **Home Assistant hassfest**. Vor einem Release sollten beide Workflows erfolgreich durchlaufen.
