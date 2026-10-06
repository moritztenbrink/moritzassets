# moritzassets

Design-Assets für Brick-Force.

- [`WAFFEN_SHEET.md`](WAFFEN_SHEET.md): komplettes Waffen-Design mit Mechaniken, Rückstoß, Visieren, Granaten, Consumables, Animationen und Projektil-FX
- [`data/`](data): alle Werte als CSV (öffnen mit Excel oder Google Sheets)
- [`artifact/waffenkammer.html`](artifact/waffenkammer.html): interaktive Waffenkammer (Simulator, Visiere, Granaten, Consumables). Nach Änderungen an `data/*.csv` neu bauen mit `python3 tools/build_sheet.py`
- [`artifact/asset-katalog.html`](artifact/asset-katalog.html): Asset-Katalog mit allen Basis-Assets, Dateinamen und Prompts für Bild-, 3D- und Sound-Generatoren (Daten in `data/assets.csv`)
