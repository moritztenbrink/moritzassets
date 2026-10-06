"""Baut die Artefakte in artifact/ aus ihren *.template.html und data/*.csv.

Jede Seite bekommt nur die Daten-Keys, die sie braucht (PAGES). Templates mit dem
Platzhalter /*__SHEET__*/"" bekommen zusätzlich das UI-Asset-Sheet als data:-URI.
Fehlt eine CSV, wird nur die Seite übersprungen, die sie braucht (Exit-Code 1).

Aufruf:  python3 tools/build_sheet.py
"""
import base64
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SHEET = ROOT / "ref" / "ui-asset-sheet.webp"
SHEET_MARK = '/*__SHEET__*/""'

WAFFEN = ["guns", "melee", "throw", "scopes", "cons", "list", "assets"]
PAGES = {
    "waffenkammer": WAFFEN,
    "asset-katalog": WAFFEN,
    "ui-katalog": ["ui", "uimig"],
}

FILES = {
    "guns": "schusswaffen.csv",
    "melee": "nahkampf.csv",
    "throw": "wurfwaffen.csv",
    "scopes": "visiere.csv",
    "cons": "consumables.csv",
    "list": "waffenliste.csv",
    "assets": "assets.csv",
    "ui": "ui_assets.csv",
    "uimig": "ui_migration.csv",
}


def convert(value):
    try:
        return float(value) if any(c in value for c in ".e") else int(value)
    except ValueError:
        return value


def load(name):
    with open(DATA_DIR / name, encoding="utf-8", newline="") as f:
        return [{k: convert(v) for k, v in row.items()} for row in csv.DictReader(f)]


def sheet_uri():
    data = base64.b64encode(SHEET.read_bytes()).decode("ascii")
    return json.dumps(f"data:image/webp;base64,{data}")


def main():
    keys = list(dict.fromkeys(k for page_keys in PAGES.values() for k in page_keys))
    data = {key: load(FILES[key]) for key in keys if (DATA_DIR / FILES[key]).exists()}
    skipped = 0
    for page, page_keys in PAGES.items():
        missing = [FILES[k] for k in page_keys if k not in data]
        if missing:
            print(f"artifact/{page}.html übersprungen: data/{', data/'.join(missing)} fehlt")
            skipped += 1
            continue
        template = ROOT / "artifact" / f"{page}.template.html"
        output = ROOT / "artifact" / f"{page}.html"
        payload = json.dumps({k: data[k] for k in page_keys}, ensure_ascii=False, separators=(",", ":"))
        html = template.read_text(encoding="utf-8").replace("/*__DATA__*/null", payload)
        if SHEET_MARK in html:
            html = html.replace(SHEET_MARK, sheet_uri())
        output.write_text(html, encoding="utf-8")
        print(f"{output.relative_to(ROOT)} geschrieben ({len(html) // 1024} KB)")
    return 1 if skipped else 0


if __name__ == "__main__":
    sys.exit(main())
