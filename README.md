# Weihnachtskarte

## Texte (Deutsch / Englisch)

Alle Texte der Karte stehen in [config.js](config.js), getrennt für `de` und `en`:
Vorderseite (`front`), Rückseite (`back.paragraphs`, ein Eintrag je Absatz), Kuvert (Poststempel, Briefmarke)
und Briefmarke). Platzhalter: `{anrede}`, `{signatur}`, `{kuvert}`.

## Personalisierung

Pro Empfänger werden Sprache, Anrede auf dem Kuvert, Anrede auf der Karte und Signatur per URL übergeben:

```
index.html?lang=en&kuvert=Frau%20Bettina&anrede=Liebe%20Frau%20Meier&signatur=Ihre%20ASW
```

Parameter, die nicht angegeben werden, bleiben leer.

Die Links für alle Kontakte aus [Kontakte.csv](Kontakte.csv) (Spalten `Sprache;Anrede_Kuvert;Anrede_Karte;Signatur`,
`Sprache` = `DE` oder `EN`) erzeugt:

```
node generate_links.js https://example.org/asw_weihnachten/index.html
```

Das Ergebnis steht in `Kontakte_Links.csv` (zusätzliche Spalte `Link`).

## Veröffentlichen (GitHub Pages)

*Settings → Pages → Deploy from a branch → `main` / `(root)`*. `Kontakte*.csv` steht in der `.gitignore`
und wird nicht veröffentlicht; die Seite ist mit `noindex` für Suchmaschinen markiert.
