# MYHS Central Card 1.0.7 – GitHub-Upload

## Dateien hochladen

1. Die ZIP-Datei **MYHS-Central-Card-GitHub-v1.0.7.zip** entpacken.
2. Auf GitHub ein öffentliches Repository anlegen oder das vorhandene öffnen.
3. **Den gesamten Inhalt des entpackten Projektordners direkt ins Hauptverzeichnis** hochladen (nicht das ZIP und nicht einen zusätzlichen Unterordner). Die Dateien `hacs.json` und `README.md` müssen im Hauptverzeichnis liegen.
4. Prüfen, dass `dist/central-overview-card.js` und `.github/workflows/validate.yml` vorhanden sind. Versteckte `.github`-Ordner werden beim Upload gelegentlich übersehen.
5. Änderungen mit **Commit changes** bestätigen.

## Version 1.0.7 auf GitHub veröffentlichen

1. Im Repository **Releases → Draft a new release** öffnen.
2. Den Tag **`v1.0.7`** vom gerade aktualisierten Hauptbranch erstellen.
3. Titel: **`MYHS Central Card v1.0.7`**.
4. Inhalt aus `RELEASE-NOTES-v1.0.7.md` übernehmen.
5. Als **normales Release** veröffentlichen, nicht als Pre-release.

HACS/Marketplace zeigt die Version des **veröffentlichten GitHub-Releases** an. Wird nur ein Commit hochgeladen, kann dort stattdessen eine Commit-Kennung erscheinen.

**Wichtig bei bestehenden Repositories:** Falls bereits ein höherer Release-Tag (z. B. `v1.1.7`) existiert, ist `v1.0.7` eine **niedrigere** Version und wird regulär nicht als Update erkannt. Das Paket kann als neue Versionslinie in einem frischen Repository veröffentlicht oder bewusst manuell installiert werden. Lösche frühere Releases nicht unüberlegt, wenn andere Nutzer sie installiert haben.

## HACS-/Marketplace-Installation

1. GitHub-Repository-URL als benutzerdefiniertes Repository vom Typ **Dashboard** hinzufügen.
2. **MYHS Central Card** installieren.
3. In Home Assistant **Dashboard bearbeiten → Karte hinzufügen** wählen.
4. Über den visuellen Editor Kacheln einstellen.

## Repository-Beschreibung

Unter **About → Description** auf GitHub eintragen:

`MYHS Cards for Home Assistant`

## Kompatibilität

Der technische Kartentyp bleibt `custom:central-overview-card`. Es ist keine Änderung bestehender Dashboards erforderlich. Für manuelle Installation und mögliche Cache-Probleme siehe `README.md`.
