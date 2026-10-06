"""Prüft data/ui_migration.csv gegen das UI-Inventar in ref/Brixel_UI-Inventar.html.

Aufruf:
  python3 tools/check_ui_migration.py             Prüfen (Exit-Code 1 bei Fehlern)
  python3 tools/check_ui_migration.py --skeleton  Gerüst nach data/ui_migration.skeleton.csv schreiben

Geprüft wird:
  - jeder Eintrag (<details class="ui">) aus dem Inventar steht genau einmal in der CSV (Bereich, Titel, Klasse)
  - die CSV enthält keine Einträge, die es im Inventar nicht gibt
  - jeder Knopf-Text (<span class="ui-label">) des Eintrags steht in der Spalte knoepfe
  - neuer_ort ist ausgefüllt und status ist einer der erlaubten Werte
"""
import csv
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INVENTORY = ROOT / "ref" / "Brixel_UI-Inventar.html"
CSV_FILE = ROOT / "data" / "ui_migration.csv"
SKELETON = ROOT / "data" / "ui_migration.skeleton.csv"

COLUMNS = ["bereich", "titel", "klasse", "knoepfe", "unterdialoge", "neuer_ort", "zugang_alt", "zugang_neu",
           "modi", "bedingungen", "ebene_alt", "ebene_neu", "status"]
STATUS = {"bleibt", "verschoben", "zusammengelegt", "aufgeteilt", "NEU-Teil", "entfällt"}
SEP = " | "


class Inventory(HTMLParser):
    """Sammelt je details.ui: Bereich, Titel, Klasse, Chips, Zwischenüberschriften und Knopf-Texte."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.entries, self.section, self.cur, self.grab, self.depth = [], "", None, None, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "")
        if tag == "section" and "group" in cls:
            self.section = a.get("data-title", "")
        if tag == "details" and cls == "ui":
            self.cur = {"bereich": self.section, "titel": "", "klasse": "", "chips": [], "h4": [], "labels": []}
            self.depth = 0
        if self.cur is None:
            return
        if tag == "details":
            self.depth += 1
        target = {"h3": "titel", "h4": "h4"}.get(tag)
        if tag == "span" and cls == "cls":
            target = "klasse"
        elif tag == "span" and cls.startswith("chip"):
            target = "chips"
        elif tag == "span" and cls == "ui-label":
            target = "labels"
        if target:
            self.grab = [target, tag, ""]

    def handle_data(self, data):
        if self.grab:
            self.grab[2] += data

    def handle_endtag(self, tag):
        if self.grab and tag == self.grab[1]:
            key, _, text = self.grab
            text = " ".join(text.split())
            if isinstance(self.cur[key], list):
                self.cur[key].append(text)
            else:
                self.cur[key] = text
            self.grab = None
        if tag == "details" and self.cur is not None:
            self.depth -= 1
            if self.depth == 0:
                self.entries.append(self.cur)
                self.cur = None


def unique(items):
    return list(dict.fromkeys(items))


def load_inventory():
    parser = Inventory()
    parser.feed(INVENTORY.read_text(encoding="utf-8"))
    return parser.entries


def key(row):
    return (row["bereich"], row["titel"], row["klasse"])


def skeleton(entries):
    with open(SKELETON, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for e in entries:
            ord_ = [c for c in e["chips"] if c.startswith("Ord ")]
            rest = [c for c in e["chips"] if not c.startswith("Ord ")]
            w.writerow({"bereich": e["bereich"], "titel": e["titel"], "klasse": e["klasse"],
                        "knoepfe": SEP.join(unique(e["labels"])), "unterdialoge": SEP.join(unique(e["h4"])),
                        "zugang_alt": SEP.join(rest), "ebene_alt": SEP.join(ord_)})
    print(f"{SKELETON.relative_to(ROOT)} geschrieben ({len(entries)} Einträge)")


def check(entries):
    with open(CSV_FILE, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        missing_cols = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        rows = list(reader)
    errors = [f"Spalte fehlt: {c}" for c in missing_cols]
    if errors:
        return errors
    by_key = {}
    for row in rows:
        if key(row) in by_key:
            errors.append(f"doppelt: {key(row)}")
        by_key[key(row)] = row
    inv_keys = {key(e) for e in entries}
    for k in by_key:
        if k not in inv_keys:
            errors.append(f"nicht im Inventar: {k}")
    for e in entries:
        row = by_key.get(key(e))
        if row is None:
            errors.append(f"fehlt: {key(e)}")
            continue
        listed = {s.strip() for s in row["knoepfe"].split("|")}
        for label in unique(e["labels"]):
            if label not in listed:
                errors.append(f"Knopf fehlt in {e['titel']}: {label}")
        if not row["neuer_ort"].strip():
            errors.append(f"neuer_ort leer: {e['titel']}")
        if row["status"].strip() not in STATUS:
            errors.append(f"status ungültig in {e['titel']}: {row['status']!r}")
    return errors


def main():
    entries = load_inventory()
    if "--skeleton" in sys.argv:
        skeleton(entries)
        return 0
    errors = check(entries)
    labels = sum(len(unique(e["labels"])) for e in entries)
    if errors:
        print("\n".join(errors))
        print(f"{len(errors)} Fehler")
        return 1
    print(f"OK: {len(entries)}/{len(entries)} Einträge, {labels} Knopf-Texte zugeordnet")
    return 0


if __name__ == "__main__":
    sys.exit(main())
