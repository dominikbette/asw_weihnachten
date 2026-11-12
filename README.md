# Weihnachtskarte

## Texte (Deutsch / Englisch)

Alle Texte der Karte stehen in [config.js](config.js), getrennt für `de` und `en`:
Vorderseite (`front`), Rückseite (`back.paragraphs`, ein Eintrag je Absatz) und Kuvert (Adresse, Poststempel,
Briefmarke). Platzhalter: `{anrede}`, `{signatur}`, `{kuvert}`.

## Personalisierung

Sprache, Anrede auf dem Kuvert, Anrede auf der Karte und Signatur stehen base64url-kodiert (JSON) im
URL-Parameter `d`, nicht im Klartext:

```
index.html?d=eyJsYW5nIjoiZW4iLCJrdXZlcnQiOiJGcmF1IEJldHRpbmEiLCJhbnJlZGUiOiJMaWViZSBGcmF1IE1laWVyIiwic2lnbmF0dXIiOiJJaHJlIEFTVyJ9
```

Das ist nur Kodierung, keine Verschlüsselung: Wer den Link hat, kann ihn dekodieren. Fehlt `d`, bleiben die
personalisierten Felder leer.

## E-Mail-Versand

[send_mails.py](send_mails.py) (nur Python-Standardbibliothek) erzeugt für jeden Kontakt aus `Kontakte.csv`
(Spalten `Sprache;Anrede_Kuvert;Anrede_Karte;Signatur;Email`, `Sprache` = `DE` oder `EN`) den Link und sendet die Mail.
Betreff und Text der Mail stehen oben im Skript (`MAILS`).

```
python send_mails.py https://dominikbette.github.io/asw_weihnachten/ --dry-run
python send_mails.py https://dominikbette.github.io/asw_weihnachten/ --export Kontakte_Links.csv
python send_mails.py https://dominikbette.github.io/asw_weihnachten/
```

SMTP-Zugangsdaten per Umgebungsvariablen (PowerShell):

```
$env:SMTP_HOST = "smtp.example.org"; $env:SMTP_PORT = "587"
$env:SMTP_USER = "name@example.org"; $env:SMTP_PASSWORD = "..."
$env:MAIL_FROM = "name@example.org"   # optional
```

## Veröffentlichen (GitHub Pages)

*Settings → Pages → Deploy from a branch → `main` / `(root)`*. `Kontakte*.csv` steht in der `.gitignore`
und wird nicht veröffentlicht; die Seite ist mit `noindex` für Suchmaschinen markiert.
