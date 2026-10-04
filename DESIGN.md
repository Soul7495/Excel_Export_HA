# NIBE Control — Design System

## North Star
Eine ruhige technische Gebäudeautomation mit der Verständlichkeit einer guten Consumer-App. Der Anlagenfluss ist die visuelle Signatur: Außenluft → Wärmepumpe → System → Heizkreis/Warmwasser.

## Visual language
- Hintergrund und Karten kommen ausschließlich aus Home-Assistant-Themevariablen.
- Funktionsfarben: Wärmepumpen-Grün `#287f75`, Heizfluss `#dc704e`, Wasser `#3c7d9d`.
- Zahlen sind kompakt, kontrastreich und tabellarisch lesbar; technische Kürzel bleiben sekundär sichtbar.
- Runde Ecken sind funktional abgestuft: 22 px Anlagenbild, 18 px Hauptkarten, 14 px Messwerte.

## Layout
- Desktop: Anlagenbild über drei Funktionskarten und sechs kompakten Messwerten.
- Smartphone: einspaltige Hauptkarten, Messwerte im 2er-Raster, vereinfachtes Anlagenbild.
- Vier klare Modi: Übersicht, Verläufe, Datencheck, Diagnose.

## Motion
Nur der aktive Verdichter und ein aktiver Wärmefluss bewegen sich. `prefers-reduced-motion` deaktiviert alle Animationen.

## Safety
Bedienung ist kein Nebenprodukt schreibbarer Entities. Ausschließlich Klima-Sollwert und von `water_heater` tatsächlich angebotene Modi sind freigegeben.

## Runtime mapping
Die normativen Farben werden als `--nc-*` Variablen im Root der Komponente definiert. Oberflächen, Text, Fehler- und Fokusfarben erben aus dem aktiven Home-Assistant-Theme.
