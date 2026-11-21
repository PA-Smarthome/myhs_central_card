# MYHS Central Card v1.1.4

## Behoben

- **Kachel-Sichtbarkeit:** Kacheln lassen sich direkt in der Übersicht ausblenden und wieder einblenden. Neue Aktionen „Alle anzeigen“ und „Alle ausblenden“. Statusliste und Kartenvorschau werden beim Speichern aktualisiert.
- **Eigene Icons:** Ein gewähltes `mdi:`-Icon wird auch bei dynamischen Zuständen von Schlössern und Beschattungen beibehalten. Zusätzlich zum Home-Assistant-Symbolwähler gibt es eine zuverlässige manuelle Eingabe.
- **Entitätsauswahl:** Direkte Eingabe von Entitäts-IDs sowie Gruppen, falls ein Home-Assistant-Auswahlmenü fehlt.
- **Zuverlässige Statusanzeige:** Nicht verfügbare Fenster und Beschattungen werden nicht länger als vollständig geschlossen/offen dargestellt; fehlerhafte Grenzwerte werden erkannt.
- **Visueller Editor:** Wechsel zwischen sichtbaren und ausgeblendeten Kacheln sowie Speichern und erneutes Laden getestet.

## Unverändert

- 16 universelle Kacheltypen, ursprünglicher Farbverlauf, Home-Assistant-Theme-Farben und visuelle Konfiguration.
- Kartentyp `custom:central-overview-card` und JavaScript-Dateiname bleiben kompatibel mit bestehenden Dashboards.

## Aktualisierung

Datei `dist/central-overview-card.js` auf GitHub ersetzen, committen und ein **reguläres** Release mit dem Tag `v1.1.4` vom aktualisierten Stand veröffentlichen. Danach HACS/Marketplace aktualisieren und das Home-Assistant-Frontend neu laden. Bei einer früher veröffentlichten höheren Version ist ein noch höherer Release-Tag erforderlich.

## Tests

Automatisierte Node.js- und Chromium-Tests wurden ausgeführt; eine vollständige Prüfung in einer echten Home-Assistant-Installation (insbesondere iOS und herstellerspezifische Geräte) steht noch aus.
