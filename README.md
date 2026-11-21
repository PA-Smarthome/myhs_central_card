# MYHS Central Card

Eine eigenständige Lovelace-Karte mit **16 frei konfigurierbaren Status-Kacheln** und **vollständigem visuellem Editor**. Die Karte ist für jede Home-Assistant-Installation gedacht. Sie enthält **keine festen Benutzer- oder Entitäts-IDs** und benötigt **keine `button-card`**.

![Vorschau mit frei erfundenen Beispieldaten](images/preview.png)

## Visuell bearbeiten – direkt im Home-Assistant-Menü

![Visueller Editor (Demonstrationsansicht)](images/editor.png)

1. Dashboard öffnen → **Dashboard bearbeiten**.
2. **Karte hinzufügen** → **Zentralübersicht (universell)** auswählen.
3. Für eine bestehende Karte **Karte bearbeiten** öffnen.
4. Im **visuellen Menü** die gewünschte Kachel aufklappen. Dort kann man:
   - Kacheltyp wählen, Kacheln **hinzufügen / entfernen / ein- und ausblenden / umsortieren**.
   - **Datenquelle** wählen: automatische Erkennung, ausgewählte Entitäten oder Gruppen/Helfer.
   - Eigene **Entitäten aus dem Home-Assistant-Entitätswähler** zuordnen (auch mehrere).
   - **Bereich** filtern (bei automatischer Erkennung), optional Entitäts-Präfix filtern.
   - **Icon** (`mdi:` oder `local:`), **Beschriftung**, **Navigationsziel** und **aktive Farbe** festlegen.
   - **Spaltenzahl** (1–4), Abstand und die Anzeige von Untertiteln festlegen.
5. **Speichern**. Die Karte erzeugt die Lovelace-Konfiguration selbst – **kein YAML erforderlich**.

### Die 16 Kacheltypen

| Typ | Angezeigter Status | Automatische Erkennung |
| --- | --- | --- |
| Sicherheit | Zustand der Alarmzentrale | `alarm_control_panel` (bei mehreren auswählen) |
| Fenster | Geöffnete Fenster | `binary_sensor` mit `device_class: window/opening` |
| Licht | Aktive Leuchten nach Bereich | `light` |
| Energie | Aktive Steckdosen/Geräte | `switch` mit Geräteklasse `outlet/plug` |
| Heizung | Räume in Heiz-/Auto-Modus | `climate` mit `heat`, ohne `cool` in `hvac_modes` |
| Klima | Kühlen / Heizen / Lüften | `climate` mit `cool` in `hvac_modes` |
| Audio | Wiedergabe/Pause in Räumen | `media_player` mit Geräteklasse `speaker/receiver` |
| Beschattung | Offen, geschlossen, teilweise | `cover`; optionale Automatik-Entität |
| Media | Fernseher an | `media_player` mit Geräteklasse `tv` |
| Lüftung/Raumluft | Räume/Sensoren außerhalb der Grenzwerte | Entitäten auswählen, Grenzwert oder gute Zustände festlegen |
| Zutritt | Tür verriegelt / entriegelt / blockiert | `lock` (bei mehreren auswählen) |
| Wecker | Anzahl aktiver Wecker | Entitäten auswählen |
| Präsenz | Bewegung in Räumen | `binary_sensor` mit `motion/presence/occupancy` |
| Anwesenheit | Personen anwesend | `person` (andere Zonen optional) |
| Fahrzeuge | Fahrzeuge in gewähltem Zustand | Entitäten auswählen, Fahrzustand definieren |
| Automatik | Aktivierte Automationen | `automation` |

**Hinweis zur automatischen Erkennung:** Diese nutzt Home-Assistant-Domänen und Geräteklassen, keine Wörter aus Entitäts-IDs wie `sonos` oder `heizung`. Geräte ohne passende Geräteklasse bitte über **„Entitäten auswählen“** bzw. **„Gruppe / Helfer verwenden“** zuordnen. Automatisch erkannte Aggregat-Entitäten mit `entity_id`-Mitgliedern werden zum Zählen auf ihre Mitglieder aufgelöst. Wenn die Installation keine Geräte-/Bereichszuordnung bietet, wird statt der Anzahl **Räume** ggf. die Anzahl **Geräte** angezeigt.

## Farben

Verwendet ausschließlich die **vorhandenen Home-Assistant-Theme-Variablen**: `--success-color`, `--error-color`, `--warning-color`, `--info-color`, `--orange-color`, `--cyan-color`, `--purple-color`, `--pink-color` und weitere Standard-Palettenfarben (`--red-color`, `--green-color`, `--amber-color`, …). **Keine `--custom_*`-Variablen.** Die jeweils aktive Farbe kann im visuellen Editor eingestellt werden. Alarm und Schloss benutzen standardmäßig **zustandsabhängige Farben**. Die Farbverläufe werden per CSS erzeugt, passend zu hellen und dunklen Themes.

## Installation

### Option A – über HACS / Marketplace mit öffentlichem GitHub-Repository

1. Den Inhalt dieses Projektordners in ein **eigenes öffentliches GitHub-Repository** hochladen, z. B. `lovelace-central-overview-card`. Die `hacs.json` muss **im Repository-Hauptverzeichnis** liegen, die JavaScript-Datei in `dist/`.
2. Das Repository in HACS/Marketplace als **benutzerdefiniertes Repository vom Typ Dashboard** hinzufügen. Je nach Home-Assistant-Version heißt der Bereich **HACS** oder **Marketplace**.
3. Die Karte installieren und Home Assistant im Browser neu laden.
4. Die Karte in **Dashboard bearbeiten → Karte hinzufügen** auswählen. Der visuelle Editor ist direkt enthalten.

**Wichtig:** Ein ZIP kann **nicht einfach** in HACS als Repository importiert werden. HACS/Marketplace installieren aus einem GitHub-Repository; das ZIP enthält die Dateien, die man dort hochlädt.

Zur Vorbereitung der öffentlichen Veröffentlichung ist eine GitHub-Action `.github/workflows/validate.yml` enthalten. Eine Aufnahme in den öffentlichen HACS-Katalog muss separat beantragt werden und wird nicht durch das ZIP garantiert.


### Mini-YAML-Beispiel (optional, nicht nötig für den Editor)

```yaml
type: custom:central-overview-card
columns: 2
gap: 8
tiles:
  - kind: windows
    label: Fenster
    source: auto
    tone: error
    navigation_path: '#fenster'
  - kind: lights
    label: Licht
    source: auto
    tone: warning
  - kind: people
    label: Zuhause
    source: auto
    tone: pink
```

Die **Standardkonfiguration** enthält automatisch alle 16 Kacheln – mit dem visuellen Editor braucht man nichts von Hand einzutragen.

## Eigenschaften für Fortgeschrittene

- `tiles[].source`: `auto`, `selected`, `group`
- `tiles[].entities`: Array von Entitäts-IDs bei `selected`
- `tiles[].entity`: Gruppen-/Helfer-Entität bei `group`, optional Alarm oder Schloss bei `auto`
- `tiles[].area`: Bereich-ID zum Filtern bei `auto`
- `tiles[].prefix`: optionaler ID-Präfix-Filter bei `auto`
- `tiles[].automation_entity`: Entität der Beschattungsautomatik
- `tiles[].good_states`: erlaubte Textzustände bei der Raumluftkarte, durch Kommata getrennt
- `tiles[].threshold` und `tiles[].comparison`: numerischer Grenzwert (`above` oder `below`)
- `tiles[].active_state`: Bewegungszustand bei Fahrzeugen, z. B. `on` oder `off`
- `alarm_home_legacy`: veraltete Anzeige des Zustands `armed_home` als „unscharf“; **standardmäßig deaktiviert** (Home Assistant interpretiert diesen Zustand als „scharf zu Hause“)

Die Status-Karten sind **nur zur Anzeige und Navigation** gedacht. Ein Klick auf eine Kachel kann zu einer Home-Assistant-Ansicht oder einem Hash-Anker führen; er schaltet keine Geräte oder Sicherheitsfunktionen.

## Tests

```bash
node --check dist/central-overview-card.js
node tests/smoke.cjs
# Zusätzlich optional: Python + Playwright + Chromium
python tests/browser_smoke.py
```

Die Beispielbilder wurden in einem lokalen Browser aus dieser Karte mit **synthetischen Testzuständen** erzeugt. Die JavaScript-Syntax, Zustandsberechnungen und Editor-Ereignisse wurden geprüft. **Nicht** in einer produktiven Home-Assistant-Installation oder über den öffentlichen HACS-Prozess getestet.

## Lizenz

MIT, siehe `LICENSE`.
