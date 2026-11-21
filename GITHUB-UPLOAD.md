# Projekt auf GitHub veröffentlichen

## Upload

1. Bei https://github.com/new ein neues **Public**-Repository erstellen, z. B. `lovelace-central-overview-card`. Keinen zusätzlichen Repository-Ordner anlegen.
2. `MYHS-Central-Card-GitHub-v1.1.4.zip` auf dem Computer entpacken.
3. Im neuen GitHub-Repository **Add file → Upload files** wählen.
4. **Alle Dateien und Unterordner aus dem entpackten Verzeichnis** hochladen, nicht das ZIP und nicht nur die `.js`-Datei. Bei GitHub muss `hacs.json` direkt im Hauptverzeichnis liegen und `dist/central-overview-card.js` vorhanden sein.
5. Auf **Commit changes** klicken.
6. **Wichtig für Updates:** Unter **Releases → Draft a new release** ein neues **reguläres GitHub-Release** mit dem Tag `v1.1.4` vom aktualisierten Standard-Branch veröffentlichen. **Publish release** auswählen. Kein Pre-release und keinen nur lokal angelegten Tag verwenden.
7. In Home Assistant HACS / Marketplace öffnen, benutzerdefiniertes Repository hinzufügen: die URL `https://github.com/DEIN-NAME/lovelace-central-overview-card` angeben und Kategorie **Dashboard** wählen.
8. Nach Installation das Dashboard neu laden. Unter **Dashboard bearbeiten → Karte hinzufügen** `MYHS Central Card` wählen. Dann alles im **visuellen Editor** einstellen.

## Zu beachten

- Die `.github/workflows/validate.yml` ist eine **versteckte Datei** (Ordnername beginnt mit Punkt). Prüfe nach dem Upload, ob die Datei mit hochgeladen wurde. Falls nicht, in GitHub **Add file → Create new file** wählen und als Pfad `.github/workflows/validate.yml` eingeben. Den Dateiinhalt kannst du aus dem entpackten Projekt kopieren.
- Nicht alte Versionen mit der v1.1.4 mischen. Ersetze bei einem bereits bestehenden Repository vor einem Release die alte `dist/central-overview-card.js`.
- Für die Icons werden die **integrierten `mdi:`-Symbole von Home Assistant** genutzt. Unter **Karte bearbeiten** ist dafür der native Icon-Picker integriert.
- Es werden keine persönlichen Entitäten fest vorgegeben.
- Lokale Syntax-/Browser-Tests wurden ausgeführt; ein Test auf einem echten Home-Assistant-System ist noch nicht erfolgt.

## Editor-Update prüfen auf iPhone

Nach dem neuen GitHub-Release in HACS / Marketplace **Update information** und anschließend **Redownload / Aktualisieren** wählen, anschließend die Home-Assistant-App vollständig beenden und neu starten. Unter **Karte bearbeiten** erscheint die Versionsanzeige **Version 1.1.4** im Kopfbereich. Die neue Ansicht bietet direkte Sichtbarkeitsschalter, „Alle anzeigen/ausblenden“, manuelle `mdi:`-Icon-Eingabe und einen Fallback für Entitätsgruppen. Falls nicht, ist noch alter Code geladen. Bei manueller Ressource die URL auf `/local/central-overview-card.js?v=114` ändern und anschließend komplett neu laden.

**Hinweis zu bestehenden GitHub-Releases:** Wenn das Repository bereits ein höheres Release (z. B. `v1.4.4`) enthält, betrachtet HACS ein neues `v1.1.4` ggf. nicht als Update. Die Anzeige im Karteneditor ist unabhängig vom GitHub-Tag.

## GitHub-Repository-Beschreibung

In GitHub rechts bei **About → Zahnrad → Description** exakt folgenden Text eintragen:

`MYHS Cards for Home Assistant`

Die Datei `README.md` ändert diese kurze GitHub-/HACS-Beschreibung nicht automatisch. Damit HACS `v1.1.4` statt einer Commit-Kennung wie `db97120` zeigt, muss außerdem auf GitHub ein **reguläres Release** mit Tag `v1.1.4` veröffentlicht werden.

**Wichtig:** Falls auf GitHub bereits ein Release `v1.1.4` oder höher existiert, einen **neuen, höheren Release-Tag** verwenden und auch die im JavaScript angezeigte Versionsnummer entsprechend anpassen. Ein erneuter Commit unter derselben Version erzeugt kein zuverlässiges neues Update.
