// Erzeugt aus Kontakte.csv eine Datei Kontakte_Links.csv mit einem persönlichen Link je Kontakt.
// Aufruf: node generate_links.js [Basis-URL] [Eingabe.csv] [Ausgabe.csv]
// Beispiel: node generate_links.js https://dominikbette.github.io/asw_weihnachten/
'use strict';
const fs = require('fs');

const base = process.argv[2] || 'index.html';
const input = process.argv[3] || 'Kontakte.csv';
const output = process.argv[4] || 'Kontakte_Links.csv';

const text = fs.readFileSync(input, 'utf8').replace(/^\uFEFF/, '');
const lines = text.split(/\r?\n/).filter((l) => l.trim() !== '');
const header = lines.shift().split(';').map((h) => h.trim());
const col = (name) => {
  const i = header.indexOf(name);
  if (i < 0) throw new Error('Spalte fehlt in ' + input + ': ' + name);
  return i;
};
const iLang = col('Sprache'), iKuvert = col('Anrede_Kuvert'), iKarte = col('Anrede_Karte'), iSig = col('Signatur');

const sep = base.includes('?') ? '&' : '?';
const rows = lines.map((line) => {
  const c = line.split(';').map((v) => v.trim());
  const lang = c[iLang].toLowerCase();
  if (lang !== 'de' && lang !== 'en') throw new Error('Unbekannte Sprache "' + c[iLang] + '" in: ' + line);
  const q = new URLSearchParams({ lang, kuvert: c[iKuvert], anrede: c[iKarte], signatur: c[iSig] });
  return line + ';' + base + sep + q.toString().replace(/\+/g, '%20');
});

fs.writeFileSync(output, '\uFEFF' + [header.join(';') + ';Link', ...rows].join('\r\n') + '\r\n', 'utf8');
console.log(rows.length + ' Links nach ' + output + ' geschrieben.');
