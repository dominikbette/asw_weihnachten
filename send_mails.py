"""Versendet die personalisierte Weihnachtskarte per E-Mail.

Der Link enthält die persönlichen Angaben base64url-kodiert (?d=...), nicht im Klartext.
Kontakte stehen in Kontakte.csv (Spalten: Sprache;Anrede_Kuvert;Anrede_Karte;Signatur;Email).

Beispiele:
    python send_mails.py https://dominikbette.github.io/asw_weihnachten/ --dry-run
    python send_mails.py https://dominikbette.github.io/asw_weihnachten/ --export Kontakte_Links.csv
    python send_mails.py https://dominikbette.github.io/asw_weihnachten/

SMTP-Zugangsdaten kommen aus Umgebungsvariablen (nicht ins Repository schreiben):
    SMTP_HOST, SMTP_PORT (Standard 587, STARTTLS; 465 = SSL), SMTP_USER, SMTP_PASSWORD, MAIL_FROM (optional)
"""
import argparse
import base64
import csv
import json
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage
from email.utils import formataddr

# {anrede} = Spalte Anrede_Karte, {signatur} = Spalte Signatur, {link} = persönlicher Link
MAILS = {
    "de": {
        "subject": "Frohe Weihnachten!",
        "body": "{anrede},\n\nwir haben eine Weihnachtskarte vorbereitet:\n{link}\n\n{signatur}\n",
    },
    "en": {
        "subject": "Merry Christmas!",
        "body": "{anrede},\n\nwe have prepared a Christmas card:\n{link}\n\n{signatur}\n",
    },
}


def read_contacts(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        rows = []
        for line, raw in enumerate(reader, start=2):
            row = {(k or "").strip(): (v or "").strip() for k, v in raw.items()}
            if not any(row.values()):
                continue
            row["Sprache"] = row.get("Sprache", "").lower()
            if row["Sprache"] not in MAILS:
                sys.exit(f"{path}, Zeile {line}: Unbekannte Sprache '{row['Sprache']}' (erlaubt: DE, EN)")
            if "@" not in row.get("Email", ""):
                sys.exit(f"{path}, Zeile {line}: Ungültige E-Mail-Adresse '{row.get('Email', '')}'")
            rows.append(row)
        return rows


def build_link(base_url, contact):
    payload = {
        "lang": contact["Sprache"],
        "kuvert": contact["Anrede_Kuvert"],
        "anrede": contact["Anrede_Karte"],
        "signatur": contact["Signatur"],
    }
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    encoded = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    return f"{base_url}{'&' if '?' in base_url else '?'}d={encoded}"


def build_message(contact, link, sender):
    text = MAILS[contact["Sprache"]]
    values = {"anrede": contact["Anrede_Karte"], "signatur": contact["Signatur"], "link": link}
    msg = EmailMessage()
    msg["Subject"] = text["subject"]
    msg["From"] = sender
    msg["To"] = contact["Email"]
    msg.set_content(text["body"].format(**values))
    return msg


def send(messages):
    try:
        host, user, password = os.environ["SMTP_HOST"], os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"]
    except KeyError as e:
        sys.exit(f"Umgebungsvariable fehlt: {e.args[0]}")
    port = int(os.environ.get("SMTP_PORT", "587"))
    context = ssl.create_default_context()
    smtp = smtplib.SMTP_SSL(host, port, context=context) if port == 465 else smtplib.SMTP(host, port)
    with smtp:
        if port != 465:
            smtp.starttls(context=context)
        smtp.login(user, password)
        for msg in messages:
            smtp.send_message(msg)
            print(f"Gesendet an {msg['To']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("base_url", help="URL der veröffentlichten Karte, z. B. https://dominikbette.github.io/asw_weihnachten/")
    parser.add_argument("--csv", default="Kontakte.csv", help="Kontaktliste (Standard: Kontakte.csv)")
    parser.add_argument("--dry-run", action="store_true", help="Nur anzeigen, nichts senden")
    parser.add_argument("--export", metavar="DATEI", help="Links zusätzlich in eine CSV-Datei schreiben")
    args = parser.parse_args()

    contacts = read_contacts(args.csv)
    links = [build_link(args.base_url, c) for c in contacts]

    if args.export:
        with open(args.export, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Sprache", "Email", "Link"])
            for c, link in zip(contacts, links):
                writer.writerow([c["Sprache"].upper(), c["Email"], link])
        print(f"{len(links)} Links nach {args.export} geschrieben.")

    sender = os.environ.get("MAIL_FROM") or os.environ.get("SMTP_USER", "")
    messages = [build_message(c, link, sender) for c, link in zip(contacts, links)]

    if args.dry_run:
        for msg in messages:
            print(f"--- An: {msg['To']} | Betreff: {msg['Subject']}\n{msg.get_content()}")
        return
    send(messages)


if __name__ == "__main__":
    main()
