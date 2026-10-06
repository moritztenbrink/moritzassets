"""Baut artifact/waffenkammer.html aus artifact/waffenkammer.template.html und data/*.csv.

Aufruf:  python3 tools/build_sheet.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE = ROOT / "artifact" / "waffenkammer.template.html"
OUTPUT = ROOT / "artifact" / "waffenkammer.html"

FILES = {
    "guns": "schusswaffen.csv",
    "melee": "nahkampf.csv",
    "throw": "wurfwaffen.csv",
    "scopes": "visiere.csv",
    "cons": "consumables.csv",
    "list": "waffenliste.csv",
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
    html = TEMPLATE.read_text(encoding="utf-8").replace("/*__DATA__*/null", payload)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"{OUTPUT.relative_to(ROOT)} geschrieben ({len(html) // 1024} KB)")


if __name__ == "__main__":
    main()
