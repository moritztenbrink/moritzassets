"""Baut die Artefakte in artifact/ aus ihren *.template.html und data/*.csv.

Aufruf:  python3 tools/build_sheet.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
INTRO_ALLE = (
    "Alle Basis-Waffen, Nahkampfwaffen, Granaten, Visiere, Items, Projektile und Effekte. Assets mit dem Abzeichen "
    "<b style=\"color:var(--brass)\">Basis</b> gehören zum Basis-Set, also eins pro Mechanik. Skin-Varianten wie "
    "_G, _MAX oder Q_… nutzen dasselbe Modell und stehen nicht extra drin. Die Prompts sind auf Englisch, weil "
    "Generatoren damit am besten arbeiten. Stil, Hintergrund und Generator gelten für alle Prompts."
)

# (Vorlage, Ausgabe, Ersetzungen)
PAGES = [
    ("waffenkammer", "waffenkammer", {}),
    ("asset-katalog", "asset-katalog", {
        "__TITLE__": "Brick-Force Asset-Katalog",
        "__EYEBROW__": "Brick-Force · Alle Assets &amp; Prompts",
        "__H1__": "Asset-Katalog",
        "__INTRO__": INTRO_ALLE,
        '/*__MODE__*/"alle"': '"alle"',
    }),
]

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


def embed(page_html):
    """Verpackt eine Seite als JS-String für ein iframe-srcdoc (mit eigenem Dokument-Gerüst)."""
    doc = (
        '<!doctype html><html lang="de"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<style>body{margin:0}</style></head><body>" + page_html + "</body></html>"
    )
    return json.dumps(doc, ensure_ascii=False).replace("</", "<\\/")


def main():
    data = {key: load(name) for key, name in FILES.items()}
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    built = {}
    for template_name, output_name, replacements in PAGES:
        template = ROOT / "artifact" / f"{template_name}.template.html"
        output = ROOT / "artifact" / f"{output_name}.html"
        html = template.read_text(encoding="utf-8").replace("/*__DATA__*/null", payload)
        for old, new in replacements.items():
            html = html.replace(old, new)
        if "/*__WK__*/" in html:
            html = html.replace('/*__WK__*/""', embed(built["waffenkammer"]))
        built[output_name] = html
        output.write_text(html, encoding="utf-8")
        print(f"{output.relative_to(ROOT)} geschrieben ({len(html) // 1024} KB)")


if __name__ == "__main__":
    main()
