# Projekt auf GitHub veröffentlichen

## Upload

1. Bei https://github.com/new ein neues **Public**-Repository erstellen, z. B. `lovelace-central-overview-card`. Keinen zusätzlichen Repository-Ordner anlegen.
2. `Central-Overview-Card-GitHub-v1.4.zip` auf dem Computer entpacken.
3. Im neuen GitHub-Repository **Add file → Upload files** wählen.
4. **Alle Dateien und Unterordner aus dem entpackten Verzeichnis** hochladen, nicht das ZIP und nicht nur die `.js`-Datei. Bei GitHub muss `hacs.json` direkt im Hauptverzeichnis liegen und `dist/central-overview-card.js` vorhanden sein.
5. Auf **Commit changes** klicken.
6. Unter **Releases → Draft a new release** optional ein Release mit Tag `v1.4.0` erstellen. Ein Release ist für Updates und eine spätere öffentliche Veröffentlichung sinnvoll.
7. In Home Assistant HACS / Marketplace öffnen, benutzerdefiniertes Repository hinzufügen: die URL `https://github.com/DEIN-NAME/lovelace-central-overview-card` angeben und Kategorie **Dashboard** wählen.
8. Nach Installation das Dashboard neu laden. Unter **Dashboard bearbeiten → Karte hinzufügen** `Zentralübersicht (universell)` wählen. Dann alles im **visuellen Editor** einstellen.

## Zu beachten

- Die `.github/workflows/validate.yml` ist eine **versteckte Datei** (Ordnername beginnt mit Punkt). Prüfe nach dem Upload, ob die Datei mit hochgeladen wurde. Falls nicht, in GitHub **Add file → Create new file** wählen und als Pfad `.github/workflows/validate.yml` eingeben. Den Dateiinhalt kannst du aus dem entpackten Projekt kopieren.
- Nicht alte Versionen mit der v1.4 mischen. Ersetze bei einem bereits bestehenden Repository vor einem Release die alte `dist/central-overview-card.js`.
- Für die Icons werden die **integrierten `mdi:`-Symbole von Home Assistant** genutzt. Unter **Karte bearbeiten** ist dafür der native Icon-Picker integriert.
- Es werden keine persönlichen Entitäten fest vorgegeben.
- Lokale Syntax-/Browser-Tests wurden ausgeführt; ein Test auf einem echten Home-Assistant-System ist noch nicht erfolgt.
