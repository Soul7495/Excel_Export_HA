# NIBE Control 0.3.0

Dynamisches, lokales Home-Assistant-Dashboard für NIBE-Wärmepumpen der S-Serie. Das VVM-S320-Profil wurde gegen den Entity-Export vom 04.10.2026 mit 819 Entitäten geprüft.

## Funktionen
- Community Dashboard Strategy für Home Assistant 2026.5+
- responsive Live-Anlagenansicht für Smartphone und Desktop
- Registry-/Register-basierte Entity-Erkennung statt fester Namen
- Heizung, Warmwasser, Energie, SG Ready und Diagnose
- lokale 24-h-SVG-Verläufe ohne externe Bibliothek
- integrierter Datencheck für deaktivierte oder fehlende Entities
- sichere Schreib-Allowlist
- Raum-Solltemperatur über das passende VVM-S320-Register 40207
- optionale EVCC-Status- und Modusanzeige
- Light/Dark Theme und reduzierte Bewegung

## Installation
1. Repository auf GitHub veröffentlichen.
2. In HACS unter **Frontend → Benutzerdefinierte Repositorys** die Repository-URL als Kategorie **Dashboard** hinzufügen.
3. NIBE Control installieren und Home Assistant/Browser neu laden.
4. **Einstellungen → Dashboards → Dashboard hinzufügen → Community-Dashboards → NIBE Control**.

## Empfohlene Entities
Der Datencheck im Dashboard zeigt exakt, welche zusätzlichen Entities für die vollständige Ansicht noch deaktiviert sind. Es werden keine Entities automatisch aktiviert.

Für die Raum-Solltemperatur muss `number.room_sensor_set_point_value_climate_system_1_40207` aktiviert sein.

## Sicherheit
`sensor.current_power_32177` wird nicht als Gesamtleistung genutzt. Dafür ist Register 32306 vorgesehen; 31807 bleibt die Außeneinheit. GP1 31103/31637 wird bis zum Livevergleich nicht automatisch gewählt. Kein rohes `number.*` oder `switch.*` wird bedienbar gemacht.

## Entwicklung
```bash
npm test
npm run build
npm run check
```

## Lizenz
MIT. NIBE ist eine Marke des jeweiligen Rechteinhabers; dieses Community-Projekt ist nicht mit NIBE Energy Systems verbunden.
