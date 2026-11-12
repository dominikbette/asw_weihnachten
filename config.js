/*
 * Texte der Weihnachtskarte (Deutsch / Englisch).
 *
 * Platzhalter in den Texten:
 *   {anrede}    Anrede auf der Karte   (Spalte Anrede_Karte)
 *   {signatur}  Signatur auf der Karte (Spalte Signatur)
 *   {kuvert}    Anrede auf dem Kuvert  (Spalte Anrede_Kuvert)
 *
 * Die Personalisierung erfolgt über URL-Parameter (siehe README.md):
 *   index.html?lang=de&kuvert=Herr%20Dominik&anrede=Lieber%20Dominik&signatur=Deine%20ASW
 */
window.KARTE_CONFIG = {
  defaultLanguage: 'de',

  de: {
    htmlLang: 'de',
    title: 'Frohes Fest – Weihnachtskarte',
    description: 'Eine animierte Weihnachtskarte mit Kuvert, Schneekugel und Grußbotschaft.',

    envelope: {
      address: '{kuvert}',
      postmarkText: 'WEIHNACHTSPOST · 24.12. ·',
      postmarkYear: '2026',
      stampTop: 'FROHES',
      stampBottom: 'FEST'
    },

    front: {
      greeting: 'Frohes Fest'
    },

    back: {
      // Jeder Eintrag ist ein Absatz. Leere Absätze werden weggelassen.
      paragraphs: [
        '{anrede},',
        'wir wünschen glückliche und besinnliche Feiertage und alles Gute fürs Neue Jahr!',
        '{signatur}'
      ]
    }
  },

  en: {
    htmlLang: 'en',
    title: 'Happy Holidays – Christmas Card',
    description: 'An animated Christmas card with an envelope, a snow globe and a greeting.',

    envelope: {
      address: '{kuvert}',
      postmarkText: 'CHRISTMAS MAIL · 24.12. ·',
      postmarkYear: '2026',
      stampTop: 'HAPPY',
      stampBottom: 'HOLIDAYS'
    },

    front: {
      greeting: 'Happy Holidays'
    },

    back: {
      paragraphs: [
        '{anrede},',
        'we wish you a joyful and peaceful festive season and all the best for the New Year!',
        '{signatur}'
      ]
    }
  }
};
