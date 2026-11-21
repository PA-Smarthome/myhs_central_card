# MYHS Central Card

**MYHS Cards for Home Assistant**  
**Version 1.0.7 · 16 Kacheltypen · Visueller Editor**

Eine moderne, frei konfigurierbare Übersichtskarte für Home Assistant. Die MYHS Central Card bündelt wichtige Statusinformationen deines Smart Homes in einem kompakten, übersichtlichen Raster – mit dynamischen Farbverläufen, Home-Assistant-Theme-Farben und einem visuellen Editor.

![MYHS Central Card – Vorschau](images/preview.png)

*Die Vorschau verwendet Beispieldaten.*

## Funktionen

- **16 Status-Kacheltypen:** Sicherheit, Fenster, Licht, Energie, Heizung, Klima, Audio, Beschattung, Medien, Raumluft, Zutritt, Wecker, Präsenz, Anwesenheit, Fahrzeuge und Automationen.
- **Visueller Editor:** Kacheln hinzufügen, duplizieren, entfernen, verschieben und mit einem Auge individuell ein- oder ausblenden.
- **Übersichtliche Bearbeitung:** Jede Kachel hat eine eigene, deutlich sichtbare Schaltfläche **Bearbeiten**.
- **Flexible Quellen:** Automatische Erkennung, ausgewählte Entitäten sowie Gruppen und Helfer.
- **Symbole:** Native Icon-Auswahl von Home Assistant; `mdi:`-Icons sowie weitere in Home Assistant vorhandene Icon-Sammlungen, sofern unterstützt. Manuelle Eingabe möglich.
- **Layout & Design:** Ein bis vier Spalten, anpassbare Abstände, Farben aus dem Home-Assistant-Theme, sanfte Farbverläufe und Navigationsziele.
- **Änderungen rückgängig machen:** Rückgängig/Wiederholen während der geöffneten Bearbeitungssitzung.
- **Universell:** Keine fest vorgegebenen persönlichen Entitäts-IDs.

## Vorschau des Editors

![Kompakte Kachelliste](images/editor-overview.png)

Das **Auge** blendet nur die gewählte Kachel ein oder aus; **Bearbeiten** öffnet ihre Einstellungen. Ausgeblendete Kacheln bleiben in der Editor-Liste sichtbar.

![Geöffnete Kacheleinstellungen](images/editor.png)

Alle Einstellungen lassen sich über **Dashboard bearbeiten → Karte bearbeiten** vornehmen. YAML ist nicht erforderlich.

## Installation

<!-- ha-marketplace:exclude-start -->
### Über HACS / Home Assistant Marketplace

1. Öffentliches GitHub-Repository erstellen und die Dateien aus dem Projektpaket in dessen Hauptverzeichnis hochladen.
2. Das Repository als benutzerdefiniertes **Dashboard**-Repository in HACS/Marketplace hinzufügen.
3. Die Karte installieren, die Home-Assistant-Oberfläche neu laden und unter **Karte hinzufügen** die **MYHS Central Card** auswählen.

Für die Veröffentlichung und das GitHub-Release siehe [GitHub-Anleitung](GITHUB-UPLOAD.md).

### Manuell

1. `dist/central-overview-card.js` nach `/config/www/central-overview-card.js` kopieren.
2. Unter **Einstellungen → Dashboards → Ressourcen** das JavaScript-Modul `/local/central-overview-card.js` registrieren.
3. Home Assistant neu laden und die Karte hinzufügen.
<!-- ha-marketplace:exclude-end -->

## Kacheltypen

| Typ | Status | Erkennung/Quelle |
| --- | --- | --- |
| Sicherheit | Alarmanlagenzustand | `alarm_control_panel` |
| Fenster | Geöffnete Fenster | `binary_sensor` mit Fenster-/Öffnungsklasse |
| Licht | Eingeschaltete Lichter | `light` |
| Energie | Aktive Steckdosen/Geräte | `switch` mit passender Geräteklasse |
| Heizung | Heizbetrieb | Heizungsbezogene `climate`-Entitäten |
| Klima | Kühlen/Heizen/Lüften | Kühlfähige `climate`-Entitäten |
| Audio | Wiedergabe/Pause | `media_player` für Lautsprecher/Receiver |
| Beschattung | Offen, zu, teilweise | `cover` |
| Medien | Aktive Fernseher | `media_player` für Fernseher |
| Raumluft | Grenzwert-/Zustandshinweise | Eigene Sensoren wählen |
| Zutritt | Schlosszustand | `lock` |
| Wecker | Aktive Wecker | Eigene Entitäten wählen |
| Präsenz | Bewegung/Präsenz | Passende `binary_sensor`-Geräteklassen |
| Anwesenheit | Personen zu Hause | `person` |
| Fahrzeuge | Fahrzeugstatus | Eigene Entitäten wählen |
| Automationen | Aktivierte Automationen | `automation` |

Die automatische Erkennung verwendet Geräteklassen und Entitätsdomänen. Bei abweichenden Geräten können die gewünschten Entitäten im Editor direkt zugeordnet werden.

## YAML-Konfiguration (optional)

```yaml
type: custom:central-overview-card
columns: 2
gap: 8
tiles:
  - kind: windows
    label: Fenster
    source: auto
    tone: error
  - kind: lights
    label: Licht
    source: auto
    tone: warning
  - kind: people
    label: Zuhause
    source: auto
    tone: pink
```

Der technische Kartentyp bleibt `custom:central-overview-card`, damit bestehende Dashboard-Konfigurationen kompatibel sind. Ohne eigene `tiles`-Liste stehen standardmäßig alle 16 Kacheltypen zur Verfügung.

## Version und Aktualisierung

- **Version in der Karte:** Im visuellen Editor erscheint **Version 1.0.7**.
- **Version in HACS/Marketplace:** Erst ein veröffentlichtes GitHub-Release mit dem Tag `v1.0.7` sorgt dort für eine Versionsanzeige anstelle eines Commit-Hashes. Ein Git-Tag allein genügt nicht.
- **Bestehende höhere Releases:** Wer zuvor `v1.1.7` oder eine andere höhere Version veröffentlicht hat, bekommt `v1.0.7` normalerweise **nicht als automatisches Update** angeboten. Dafür ist eine passende Release-Strategie oder eine neue Repository-Linie nötig.
- **Cache:** Bei manueller Installation kann `/local/central-overview-card.js?v=107` als Ressourcen-URL helfen, die neue Datei zu laden.

## Hinweise

Die Kacheln dienen der **Anzeige und Navigation**; sie schalten keine Geräte direkt. Die optionale Kompatibilitätseinstellung `alarm_home_legacy` betrifft die alte Anzeige von `armed_home`; Home Assistant versteht diesen Zustand normalerweise als „zu Hause scharf“.

Die Entwicklung wurde mit lokalen Syntax-, Logik- und Browserprüfungen begleitet. Eine vollständige Prüfung in jeder Home-Assistant-Version oder Geräteintegration ist damit nicht ersetzt.

## Lizenz

[MIT](LICENSE)
