# moritzassets

Design-Assets für Brick-Force.

- [`WAFFEN_SHEET.md`](WAFFEN_SHEET.md): komplettes Waffen-Design mit Mechaniken, Rückstoß, Visieren, Granaten, Consumables, Animationen und Projektil-FX
- [`data/`](data): alle Werte als CSV (öffnen mit Excel oder Google Sheets)
- [`artifact/waffenkammer.html`](artifact/waffenkammer.html): interaktive Waffenkammer (Simulator, Visiere, Granaten, Consumables). Nach Änderungen an `data/*.csv` neu bauen mit `python3 tools/build_sheet.py`
- [`artifact/asset-katalog.html`](artifact/asset-katalog.html): Asset-Katalog mit allen Basis-Assets, Dateinamen und Prompts für Bild-, 3D- und Sound-Generatoren (Daten in `data/assets.csv`)

## UI-Neuaufbau

- [`UI_KONZEPT.md`](UI_KONZEPT.md): neue UI-Struktur mit globalem Hauptmenü, Screen-Map, Design-Tokens aus dem Asset-Sheet, Komponenten, Motion- und Partikel-Spec, Unity-Umsetzung, Replays für alle Spieler
- [`artifact/ui-prototyp.html`](artifact/ui-prototyp.html): klickbarer, animierter Prototyp aller Hauptscreens im Gold-Look
- [`artifact/ui-katalog.html`](artifact/ui-katalog.html): Struktur (jedes alte Fenster → neuer Ort) und Prompt-Bibliothek für alle UI-Elemente mit dem Asset-Sheet als Stilreferenz (Daten in `data/ui_assets.csv` und `data/ui_migration.csv`, neu bauen mit `python3 tools/build_sheet.py`)
- [`data/ui_migration.csv`](data/ui_migration.csv): alle 67 Einträge des UI-Inventars mit Knöpfen, Unterdialogen, altem und neuem Zugang. Prüfen mit `python3 tools/check_ui_migration.py`
- [`ref/`](ref): Quellen, also das UI-Inventar (`Brixel_UI-Inventar.html`) und das Asset-Sheet (`ui-asset-sheet.webp`)
