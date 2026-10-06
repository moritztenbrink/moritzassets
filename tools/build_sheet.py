"""Baut die Artefakte in artifact/ aus ihren *.template.html und data/*.csv.

Aufruf:  python3 tools/build_sheet.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
PAGES = ["waffenkammer", "asset-katalog"]

FILES = {
    "guns": "schusswaffen.csv",
    "melee": "nahkampf.csv",
    "throw": "wurfwaffen.csv",
    "scopes": "visiere.csv",
    "cons": "consumables.csv",
    "list": "waffenliste.csv",
    "assets": "assets.csv",
}


def convert(value):
    try:
        return float(value) if any(c in value for c in ".e") else int(value)
    except ValueError:
        return value


def load(name):
    with open(DATA_DIR / name, encoding="utf-8", newline="") as f:
        return [{k: convert(v) for k, v in row.items()} for row in csv.DictReader(f)]


def main():
    data = {key: load(name) for key, name in FILES.items()}
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    for page in PAGES:
        template = ROOT / "artifact" / f"{page}.template.html"
        output = ROOT / "artifact" / f"{page}.html"
        html = template.read_text(encoding="utf-8").replace("/*__DATA__*/null", payload)
        output.write_text(html, encoding="utf-8")
        print(f"{output.relative_to(ROOT)} geschrieben ({len(html) // 1024} KB)")


if __name__ == "__main__":
    main()
