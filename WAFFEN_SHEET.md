# Waffen-Sheet – Brick-Force

Komplettes Design für alle Waffen, Visiere, Granaten und Consumables.
Grundlage ist der Code von [Brick-Force-Aurora/Brick-Force](https://github.com/Brick-Force-Aurora/Brick-Force) (`Assembly-CSharp`).
Alle Parameternamen (`fAtkPow`, `fRecoilPitch`, …) entsprechen genau den Feldern, die der Server an
`WeaponModifier.UpdateWpnMod` / `UpdateWpnModEx` schickt. So lassen sich die Werte direkt übernehmen.

| Datei | Inhalt |
|---|---|
| `WAFFEN_SHEET.md` | Dieses Dokument: Regeln, Mechaniken, Animationen, FX |
| `data/schusswaffen.csv` | Werte der 11 Schusswaffen-Klassen |
| `data/nahkampf.csv` | Werte der 4 Nahkampf-Klassen |
| `data/wurfwaffen.csv` | Werte der 7 Granaten-/Bomben-Klassen |
| `data/visiere.csv` | 9 Visiere inkl. Zoom-Genauigkeit |
| `data/consumables.csv` | Heiltränke, Munitionskisten, Buffs |
| `data/waffenliste.csv` | **Jede Waffe** aus `Weapon.BY` → Klasse + Abweichungen |

**Legende:** `Engine` = so funktioniert es im Code bereits. `NEU` = Vorschlag, der neuen Code braucht.

---

## 1. Grundregeln

### 1.1 Leben & Trefferzonen
- Spieler haben **100 HP** (`LocalController.GetMaxHp`).
- Schaden = `fAtkPow × Abstandsfaktor × Zonenfaktor` (`Gun.CalcAtkPow`, `HitPart.damageFactor`).

| Zone (`HitPart.TYPE`) | `damageFactor` | Hinweis |
|---|---|---|
| BRAIN (Kopf-Kern) | **2.2** | Präziser Kopftreffer. Mit Visier wird die Ebene `CoreBrain` geprüft |
| HEAD | **1.6** | Rand vom Kopf |
| BODY | 1.0 | Oberkörper |
| ARM | 0.75 | |
| FOOT | 0.6 | Beine/Füße |

### 1.2 Schadensabfall (Engine)
- Bis `fEffectiveRange`: voller Schaden.
- Zwischen `fEffectiveRange` und `fRange`: fällt **linear auf 0**.
- Ab `fRange`: kein Schaden mehr.
- Explosionen: `Schaden × (Radius − Abstand) / Radius` (linear vom Zentrum).

### 1.3 Wucht / Verlangsamung (`fRigidity`, Engine)
Ein Treffer bremst das Ziel: `Laufgeschwindigkeit × (1 − Rigidity)`.
0.15 = kaum spürbar (Pistole), 0.6 = stark (Sniper), 1.0 = Ziel steht (Taser).

### 1.4 Bewegung (`fSpeedFactor`, Engine)
Multipliziert die Laufgeschwindigkeit. Leere Hände = 1.5, Messer 1.12, Sniper 0.88, Minigun 0.75.

### 1.5 Genauigkeit (Engine, `Accuracy.cs`)
Jeder Schuss landet in einem von zwei Kegeln (Werte = Anteil der Bildschirmbreite):
- **Innerer Kegel** (`Accurate…`): wird mit `fAccuracy` % Wahrscheinlichkeit getroffen.
- **Äußerer Kegel** (`Inaccurate…`): alle anderen Schüsse.
- Jeder Schuss vergrößert beide Kegel um `…Spread`, bis `…Max` erreicht ist.
- Pro Sekunde schrumpfen sie um `…Center` zurück bis `…Min`.
- Beim Laufen wird `…Min` mit `fMoveInaccuracyFactor` multipliziert.
- Ducken/Zielen („genauer zielen“) deckelt die Streuung auf die Mitte zwischen Min und Max.
- Mit Visier gelten die `fZ…`-Werte (siehe Kapitel 5).

### 1.6 Rückstoß
- **Engine:** Jeder Schuss hebt die Kamera um `fRecoilPitch` Grad und dreht sie um `fRecoilYaw` Grad (`CameraController.Pitchup`). Die Kamera stellt sich danach nicht von selbst zurück.
- **NEU (empfohlen):**
  1. Yaw mit zufälligem Vorzeichen (links/rechts).
  2. Die ersten 3 Schüsse nur 60 % Pitch, damit Antippen belohnt wird.
  3. Rückstellung: 50 % des Kamera-Hubs wandern in 0.3 s zurück.

### 1.7 Feuerrate & Feuermodi
- `fRateOfFire` ist in **Schuss pro Minute**. Pause zwischen Schüssen = 60 / RPM (`Gun.IsCoolDown`).
- **Auto:** Feuer halten (`canCyclic`).
- **Semi:** ein Schuss pro Klick.
- **Burst-3:** `semiAuto = true` mit `semiAutoMaxCyclicAmmo = 3`.
- **Bolt/Pump:** Semi mit niedriger RPM. Die Repetier-Animation füllt die Pause.
- **Einzelschuss (Werfer/Armbrust):** `IsMuzzle = false`, echtes Projektil mit `misSpeed`.

### 1.8 Nachladen & Ziehen
- `fReloadSpeed` = Abspielgeschwindigkeit von `reload_h`. Referenzlänge des Clips: **2.0 s**, also `fReloadSpeed = 2.0 / Zielzeit`.
- `fDrawSpeed` = Abspielgeschwindigkeit von `SwitchWeapon`. Referenzlänge: **0.6 s**, also `fDrawSpeed = 0.6 / Zielzeit`.
- Bei leerem Magazin: Clip `empty` + Dry-Fire-Sound, oder automatisches Nachladen (Consumable `auto_reload`).

---

## 2. Schusswaffen

### 2.1 Klassenübersicht
Alle Werte stehen in `data/schusswaffen.csv`. Die TTK gilt für Körpertreffer innerhalb der effektiven Reichweite.

| Klasse | Modus | Schaden | RPM | Magazin / Reserve | Nachladen | Reichweite (eff./max.) | Pitch / Yaw | Wucht | Tempo | Schüsse Körper / Kern | TTK Körper |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Pistole | Semi | 26 | 400 | 12 / 48 | 1.6 s | 20 / 60 m | 1.20 / 0.30 | 0.15 | 1.00 | 4 / 2 | 450 ms |
| MP | Auto | 20 | 850 | 30 / 120 | 2.0 s | 18 / 70 m | 0.55 / 0.35 | 0.20 | 1.00 | 5 / 3 | 282 ms |
| Sturmgewehr | Auto | 28 | 650 | 30 / 120 | 2.4 s | 45 / 150 m | 0.85 / 0.25 | 0.30 | 0.95 | 4 / 2 | 277 ms |
| Kampfgewehr | Semi | 40 | 420 | 20 / 80 | 2.7 s | 70 / 200 m | 1.60 / 0.30 | 0.40 | 0.92 | 3 / 2 | 286 ms |
| Scharfschütze | Bolt | 95 | 45 | 5 / 25 | 3.0 s | 250 / 400 m | 4.50 / 0.50 | 0.60 | 0.88 | 2 / 1 | 1333 ms |
| Schrotflinte | Pump | 12 × 8–11 | 70 | 7 / 28 | 3.0 s | 8 / 35 m | 3.50 / 0.60 | 0.50 | 0.95 | 1–2 / 1 | 0–857 ms |
| MG | Auto | 24 | 1000 | 100 / 200 | 5.0 s | 60 / 200 m | 0.90 / 0.50 | 0.35 | 0.82 | 5 / 2 | 240 ms |
| LMG | Auto | 26 | 650 | 60 / 180 | 4.0 s | 55 / 180 m | 0.70 / 0.35 | 0.30 | 0.87 | 4 / 2 | 277 ms |
| Minigun | Auto (Anlauf) | 16 | 1800 | 200 / 200 | 6.0 s | 35 / 120 m | 0.35 / 0.40 | 0.25 | 0.75 | 7 / 3 | 200 ms + 0.5 s |
| Werfer | Einzeln | 120 (Zentrum) | 40 | 1 / 4 | 3.5 s | – / 300 m | 5.00 / 0.80 | 0.70 | 0.80 | 1 | – |
| Armbrust | Einzeln | 85 | 50 | 1 / 20 | 1.8 s | 120 / 250 m | 2.00 / 0.20 | 0.50 | 0.92 | 2 / 1 | 1200 ms |

**Faustregeln:**
- Nah: Schrotflinte > MP > Sturmgewehr.
- Mittel: Sturmgewehr ≈ LMG > Kampfgewehr.
- Fern: Scharfschütze > Kampfgewehr.
- Schwere Waffen bezahlen ihre Feuerkraft mit Tempo (0.75–0.87) und langem Nachladen.

### 2.2 Klassen im Detail

#### Pistole (Slot AUX)
- **Rolle:** Zweitwaffe für Notfälle. Wird schnell gezogen und ist präzise beim ersten Schuss.
- **Mechanik:** Semi. Klick-Spam ist durch 400 RPM begrenzt. Läuft man mit der Pistole, ist man nicht langsamer.
- **Varianten:** Revolver (Anaconda, Deagle): 48–52 Schaden, 150–180 RPM, starker Rückstoß. Maschinenpistole (Glock 18): Auto, 1100 RPM.
- **Rückstoß:** kurzer, steiler Kick nach oben, kaum seitlich. Kommt schnell zurück.

#### Maschinenpistole
- **Rolle:** Sturmangriff auf kurze Distanz. Höchste Mobilität unter den Hauptwaffen.
- **Mechanik:** Auto. Streuung wächst langsam pro Schuss, wird beim Laufen aber deutlich größer.
- **Rückstoß:** kleine, schnelle Kicks mit leichtem Seitenzittern (Yaw 0.35).

#### Sturmgewehr
- **Rolle:** Allrounder für jede Distanz.
- **Mechanik:** Auto. Mit Visier bei Feuerstößen von 3–5 Schuss sehr präzise.
- **Varianten:** M16 als Burst-3. Daewoo K11 mit Unterlauf-Granatwerfer (Kapitel 2.3).
- **Rückstoß:** gleichmäßig nach oben steigend, leicht nach rechts.

#### Kampfgewehr (Battle Rifle)
- **Rolle:** Mittel- bis Fernkampf. Mit 3 Körpertreffern ein Kill.
- **Mechanik:** Semi. Großer Spread-Zuwachs pro Schuss, also wird Timing belohnt.
- **Rückstoß:** kräftiger Kick (1.6°), der fast ganz zurückfedert (NEU-Rückstellung).

#### Scharfschützengewehr
- **Rolle:** Kill auf Distanz mit einem Treffer in Kopf oder Kern.
- **Mechanik:**
  - Bolt-Action (45 RPM, 1.33 s pro Schuss).
  - Ohne Visier fast nutzlos (`fAccuracy` 10).
  - Mit Visier 98 % Genauigkeit.
  - `zoomKeep = false`: Nach dem Schuss zoomt die Waffe heraus und muss neu ins Visier.
  - Mit Visier wird der Kopf gegen `CoreBrain` geprüft. Kerntreffer = 209 Schaden.
- **Varianten:** AWM (110 Schaden, Körpertreffer tötet). Barrett M82A1 (Semi, 10 Schuss, zerstört Bricks).
- **Rückstoß:** sehr hoher Kick (4.5°). Waffe springt sichtbar aus dem Bild.

#### Schrotflinte
- **Rolle:** One-Shot-Waffe auf Nahdistanz für Gänge und Brick-Häuser.
- **Mechanik:**
  - Pro Schuss werden 8–11 Kugeln abgefeuert (`minBuckShot = 8`, `maxBuckShot = 12`; der obere Wert ist exklusiv, `Shutgun.cs`).
  - Jede Kugel würfelt ihre Streuung selbst.
  - Ab 9 Treffern mit je 12 Schaden ist der Gegner tot.
- **NEU:** Patronenweises Nachladen (0.4 s pro Patrone, mit Feuer abbrechbar).
- **Rückstoß:** starker Kick nach oben und hinten, die Kamera ruckelt kurz.

#### Maschinengewehr (MG)
- **Rolle:** Sperrfeuer und Verteidigung.
- **Mechanik:**
  - Auto mit 100er-Gurt.
  - Im Stehen ungenau (`fAccuracy` 60).
  - Ducken deckelt die Streuung auf die halbe Spanne (Engine: „genauer zielen“). So entsteht ein Zweibein-Gefühl.
- **Rückstoß:** konstant mittel, dazu deutliches Seitenwackeln (Yaw 0.5).

#### Leichtes MG (LMG)
- **Rolle:** Mobileres MG. Mehr Munition als ein Sturmgewehr, schwerer als eines.
- **Mechanik:** Auto, 60er-Magazin. Die Streuung zwischen Sturmgewehr und MG.
- **Rückstoß:** ruhig und gleichmäßig.

#### Minigun
- **Rolle:** Spezialwaffe. Höchster Schadensoutput, sehr langsam.
- **Mechanik:**
  - **NEU Anlauf:** Feuer halten → 0.5 s Rotor-Anlauf → Dauerfeuer.
  - Feuer-Sound läuft als Loop (`Weapon.StartFireSound` / `EndFireSound` gibt es schon).
- **Rückstoß:** gering pro Schuss, aber durch die Menge ein stetiges Hochwandern.

#### Werfer (Raketen- / Granatwerfer)
- **Rolle:** Flächenschaden und Brick-Zerstörung.
- **Mechanik:**
  - Echtes Projektil (`IsMuzzle = false`, `CreateBigShoot`).
  - Startimpuls `misSpeed` = 35. Explosion mit `Radius1stWpn` = 5 m.
  - Granate mit Fallkurve (`LAUNCHER.GRANADE`), Rakete fliegt gerade (`LAUNCHER.ROCKET`).
  - Rauchspur kommt aus `missileSmokeEff`.
- **Rückstoß:** großer Kick (5°), kurzes Kamerawackeln.

#### Armbrust
- **Rolle:** Leise Präzisionswaffe mit sichtbarer Flugkurve.
- **Mechanik:**
  - Physischer Bolzen (`misSpeed` = 60) mit Schwerkraft.
  - Ohne Rauchspur (`IsCrossbowType`).
  - Der Bolzen bleibt im Ziel stecken (`ParentFollow`).
  - Hydra: Sprengbolzen (Radius 2.5 m).
  - Magierstab: Orb ohne Fallkurve (`IsStaffType`).

### 2.3 Zweitwaffe: Unterlauf-Granatwerfer (Engine)
Gilt für Gewehre mit `Launcher = GRANADE`, z. B. die Daewoo K11.

| Parameter | Wert |
|---|---|
| Auslösen | Rechtsklick (`K_FIRE2`), wenn kein Visier vorhanden ist |
| `maxLauncherAmmo` | 2 |
| `damage2ndWpn` | 100 |
| `radius2ndWpn` | 4.5 m |
| `fThrowForce` (Startimpuls) | 25 |
| `recoilPitch2ndWpn` / `recoilYaw2ndWpn` | 3.0 / 0.4 |
| Animation | Waffe: `bigfire`, Figur: `sniping_h` |

---

## 3. Nahkampfwaffen (Slot MELEE)

Werte in `data/nahkampf.csv`.

| Klasse | Leicht / Schwer | `fSlashSpeed` | Dauer leicht / schwer | Reichweite | Winkel | Wucht | Tempo | Rücken |
|---|---|---|---|---|---|---|---|---|
| Messer | 35 / 70 | 1.40 | 0.35 / 0.75 s | 1.6 m | 70° | 0.30 | 1.12 | ×2.0 |
| Werkzeug | 45 / 85 | 1.00 | 0.45 / 0.90 s | 1.9 m | 90° | 0.50 | 1.08 | ×1.5 |
| Schwer | 60 / 110 | 0.75 | 0.60 / 1.20 s | 2.2 m | 110° | 0.70 | 1.02 | ×1.5 |
| Energie | 50 / 95 | 1.20 | 0.40 / 0.85 s | 2.0 m | 100° | 0.40 | 1.10 | ×1.5 |

**Mechanik:**
- **Leichter Schlag** (Linksklick): Clip `slash_h`, Geschwindigkeit = `fSlashSpeed` (Engine).
- **Schwerer Schlag** (Rechtsklick): Clip `slash_big_h`. Mehr Schaden, aber langsamer.
- **Trefferfenster** (Engine): Animation-Events `SlashStart` / `EnterValidRange` / `LeaveValidRange` / `SlashEnd`. Nur in diesem Fenster wird ein Treffer gezählt. Pro Schlag gibt es höchstens 1 Treffer pro Ziel.
- **NEU Rückentreffer:** Liegt der Winkel zur Blickrichtung des Opfers unter 60°, wird mit dem Faktor multipliziert. Ein schwerer Messerangriff von hinten tötet sofort.
- **NEU Combo:** Leichte Schläge wechseln zwischen links und rechts (`slash_h` gespiegelt).
- **Brick-Schaden:** Schwere Waffen können Bricks beschädigen, Messer nicht.
- **Haltung:** Mit Nahkampfwaffe ist man am schnellsten (Tempo 1.02–1.12).

**Animation (Zeitanteile des Clips):**

| Clip | Ausholen | Trefferfenster | Zurück |
|---|---|---|---|
| `slash_h` | 0–30 % | 30–55 % | 55–100 % |
| `slash_big_h` | 0–45 % | 45–65 % | 65–100 % |

---

## 4. Granaten & Wurfwaffen (Slot BOMB)

Werte in `data/wurfwaffen.csv`.

| Klasse | Auslöser | Schaden | Radius | Zünder | Wurfkraft | Effekt |
|---|---|---|---|---|---|---|
| Splitter | Zeit | 110 | 6 m | 3.0 s | 15 | Kochen möglich (NEU) |
| Zeitbombe / C4 | Zeit | 150 | 7 m | 5.0 s | 8 | Haftet (NEU), hoher Brick-Schaden |
| Sensor-Mine | Annäherung 2.5 m | 120 | 5 m | scharf nach 1.5 s | 10 | Piept 0.4 s vor der Explosion, hält 60 s |
| Fernzünder | 2. Klick | 140 | 6.5 m | manuell | 10 | Werfen, dann mit Linksklick zünden |
| Blendgranate | Zeit | 0 | 15 m | 1.5 s | 15 | Blendet bis 3.5 s (`continueTime`) |
| Rauch | Zeit | 0 | 6 m | 1.5 s | 14 | Wolke 12 s (`persistTime`) |
| Gift | Aufprall | 10 + 8/s | 5 m | – | 14 | Wolke 6 s, Wucht 0.4 in der Wolke |

**Mechanik:**
- Schaden fällt linear vom Zentrum ab und wird mit dem Zonenfaktor des getroffenen Körperteils multipliziert (Engine, `Grenade.CalcPowFrom`).
- **Werfen:** Clip `throw_h`, ca. 0.8 s:
  1. Stift ziehen (0–30 %)
  2. Ausholen (30–60 %)
  3. Loslassen bei 60 %
  4. Nachschwung
- **NEU Kochen:** Wer Feuer nach dem Stiftziehen hält, lässt den Zünder schon laufen. Am Bildschirmrand erscheint ein Ring-Timer.
- **NEU Unterhand-Wurf:** Rechtsklick wirft mit halber Kraft (`throwForce × 0.5`).
- **Blendung:** Schaut man direkt hin, gilt die volle Dauer. Steht man seitlich, die Hälfte. Mit dem Rücken zur Granate nur 0.5 s.
- **Warnung:** Gegner sehen im Radius ein Granaten-Symbol (`ProjectileAlert` gibt es schon).

---

## 5. Visiere / Scopes

Werte in `data/visiere.csv`. Basis-FOV 60°, `fZFov = 2 × atan(tan(30°) / Vergrößerung)`.

| Visier | Zoom | `fZFov` | `fZCamSpeed` | Stufen | `zoomKeep` | Zielzeit | Overlay | Glanz |
|---|---|---|---|---|---|---|---|---|
| Kimme & Korn | 1.15× | 53.3 | 0.90 | – | ja | 0.15 s | 3D | nein |
| Rotpunkt | 1.3× | 47.9 | 0.85 | – | ja | 0.18 s | 3D + Punkt | nein |
| Holo | 1.5× | 42.1 | 0.80 | – | ja | 0.20 s | 3D + Ring | nein |
| Zielfernrohr 2× | 2× | 32.2 | 0.65 | – | ja | 0.25 s | Vollbild | nein |
| Zielfernrohr 4× | 4× | 16.4 | 0.45 | – | ja | 0.30 s | Vollbild | ja |
| Sniper 6× | 6× | 11.0 | 0.35 | – | **nein** | 0.35 s | Fadenkreuz | ja |
| Sniper 4×/10× | 4× → 10× | 16.4 → 6.6 | 0.25 | 1 (`midfovs = [16.4]`) | **nein** | 0.40 s | Fadenkreuz | ja |
| Anti-Material 8× | 8× | 8.3 | 0.30 | – | ja | 0.40 s | Fadenkreuz | ja |

**Mechanik:**
- **Engine:**
  - Rechtsklick schaltet das Visier um (`Scope.ToggleScoping`).
  - Mit `midstep > 0` schaltet jeder Rechtsklick eine Stufe weiter, bis wieder herausgezoomt wird.
  - `zoomKeep = false` zoomt nach jedem Schuss heraus (Bolt-Sniper).
  - `fZCamSpeed` senkt die Mausempfindlichkeit.
  - Im Visier gelten die eigenen Genauigkeitswerte (`fZAccuracy` …). Laufen bestraft dabei stärker (`fZMoveInaccuracyFactor` bis 6).
- **NEU Schwanken:** Ab 6× schwankt das Bild in einer 8er-Figur mit 0.25° Ausschlag. Shift hält 3 s den Atem an, danach 2 s Abklingzeit.
- **NEU Glanz:** Ab 4× sehen Gegner im Sichtfeld der Linse ein kurzes Blitzen. Das ist das Konterspiel gegen Sniper.
- **NEU Zielzeit:** Bis zur vollen Zielzeit gelten noch die Hüft-Genauigkeitswerte.

---

## 6. Consumables (Heiltränke & Co.)

Werte in `data/consumables.csv`. Im Engine laufen sie über `ShooterTools` / `ShooterTool` mit:
- eigener Taste
- `cooltime`
- `actionClip` (Sound beim Benutzen)
- `errorClip` (Sound, wenn die Nutzung nicht möglich ist, z. B. bei vollem Leben)
- Sperre für bestimmte Raumtypen (`disableByRoomType`)

| Engine-Name | Name | Effekt | Abklingzeit | Nutzzeit | Status |
|---|---|---|---|---|---|
| `heal30` | Heiltrank (klein) | +30 HP | 15 s | 0.6 s | Engine |
| `heal50` | Heiltrank (mittel) | +50 HP | 25 s | 0.8 s | Engine |
| `heal` | Heiltrank (groß) | +100 HP (voll) | 40 s | 1.0 s | Engine |
| `auto_heal` | Regenerations-Elixier | Nach 5 s ohne Schaden +5 HP/s | passiv | – | Engine |
| `speedup` | Tempo-Trank | Laufen ×1.75 für 6 s | 45 s | 0.5 s | Engine |
| `heartbeat_radar` | Herzschlag-Sensor | Gegner in 25 m für 5 s auf der Minimap | 30 s | 0.3 s | Engine |
| `*_ammo` (6×) | Munitionskiste | +2 Magazine (Schwer +1, Granate +1) | 30–45 s | 0.8 s | Engine |
| `auto_reload` | Auto-Nachladen | Lädt bei leerem Magazin automatisch nach | passiv | – | Engine |
| `respawn` | Sofort-Respawn | Respawn ab 2 s nach dem Tod | – | – | Engine |
| `just_respawn` | Direkt-Respawn | Automatischer Respawn ohne Wartezeit | passiv | – | Engine |
| `armor_potion` | Rüstungstrank | +25 Schild für 15 s | 45 s | 0.8 s | NEU |
| `antidote` | Gegengift | Entfernt Gift und Blendung | 30 s | 0.5 s | NEU |
| `adrenaline` | Adrenalin | Immun gegen Wucht/Verlangsamung für 5 s | 40 s | 0.4 s | NEU |

**Regeln:**
- Heilung geht nie über die maximalen HP.
- Die Heil-Abklingzeit wird durch den Item-Effekt `hp_cooltime` verkürzt (Engine).
- **NEU Nutzzeit:** Die Waffe wird kurz gesenkt und es läuft `drink_h` / `use_h` / `inject_h`. Schießen oder Sprinten bricht ab, ohne die Abklingzeit zu verbrauchen.
- Andere Spieler sehen die Heilung als FX (`PEER_CONSUME` → `TPController.Heal()`).

**Trank-Assets:** Flasche mit Korken, Größe S/M/L passend zu klein/mittel/groß.
- Farben: Heilung **grün**, Tempo **blau**, Rüstung **gelb**, Gegengift **weiß**.
- Icon-Paar wie im Engine: `enable` (farbig) und `disable` (grau).

---

## 7. Animationen

### 7.1 Clip-Namen (müssen exakt so heißen)

| Wo | Clip | Wofür |
|---|---|---|
| Waffen-Modell (1st Person) | `idle`, `idle1`, `idle2` | Ruhe und Zufalls-Animationen |
| | `fire` | Schuss. Bei Dauerfeuer springt die Engine auf 25 % der Cliplänge zurück |
| | `empty` | Abzug bei leerem Magazin |
| | `bigfire` | Werfer / Unterlauf |
| Figur (Bip) | `idle_h`, `run_h` | Haltung |
| | `reload_h` | Nachladen, Geschwindigkeit = `fReloadSpeed` |
| | `SwitchWeapon` | Waffe ziehen, Geschwindigkeit = `fDrawSpeed` |
| | `fireAnimation` (pro Waffe) | Schuss-Haltung des Körpers |
| | `sniping_h` | Zweitwaffe abfeuern |
| | `slash_h`, `slash_big_h` | Nahkampf |
| | `throw_h` | Granate |
| | `drink_h`, `use_h`, `inject_h` | Consumables (NEU) |

Sound-Events im Reload-Clip (`Weapon.GadgetSound`): `CLIPOUT`, `CLIPIN`, `BOLTUP`, sowie `DRYFIRE` beim leeren Abzug.

### 7.2 Timing pro Klasse

| Klasse | `fire` | Nachladen (Events in % des Clips) | Ziehen | Besonderheit |
|---|---|---|---|---|
| Pistole | 0.08 s, Schlitten 2 cm zurück, Mündung +4° | 1.6 s – ClipOut 20, ClipIn 55, BoltUp 85 (nur wenn leer) | 0.4 s | Bei leerem Magazin bleibt der Schlitten hinten |
| MP | 0.06 s | 2.0 s – 20 / 55 / 85 | 0.5 s | |
| Sturmgewehr | 0.08 s | 2.4 s – 25 / 60 / 85 | 0.6 s | |
| Kampfgewehr | 0.12 s | 2.7 s – 25 / 60 / 85 | 0.7 s | |
| Scharfschütze | 0.25 s + Repetieren 1.0 s (BoltUp 50 %) | 3.0 s – Bolt auf 15, Out 30, In 60, BoltUp 90 | 0.8 s | Herauszoomen nach dem Schuss |
| Schrotflinte | 0.15 s + Pumpen 0.55 s (BoltUp 40 %) | 3.0 s (NEU: 0.4 s pro Patrone) | 0.6 s | |
| MG | 0.05 s | 5.0 s – Deckel 15, Gurt raus 30, Gurt rein 60, Deckel zu 85 | 1.2 s | |
| LMG | 0.09 s | 4.0 s – 25 / 60 / 85 | 1.0 s | |
| Minigun | Anlauf 0.5 s → Loop → Auslauf 0.6 s | 6.0 s – Kasten raus 30, rein 70 | 1.5 s | Läufe drehen sich |
| Werfer | `bigfire` 0.4 s | 3.5 s – Rakete einsetzen 60 | 1.0 s | |
| Armbrust | `bigfire` 0.2 s | 1.8 s – Sehne spannen 40, Bolzen 75 | 0.7 s | |

**Regeln für Animatoren:**
- Der `fire`-Clip muss kürzer sein als 60 / RPM, sonst verschluckt er Schüsse.
- Das Bild bei 25 % muss sich als Neustart-Punkt eignen.
- Jede Waffe bekommt `idle1` und `idle2` (Waffe kurz ansehen, Magazin prüfen) für längere Pausen.

---

## 8. Projektile & Impact-FX

Passend zum Asset-Sheet (Seitenansicht: Geschoss + Leuchtspur links, Impact rechts).

| Klasse | Kaliber | Projektil-Sprite | Leuchtspur | Mündungsfeuer | Hülse | Impact |
|---|---|---|---|---|---|---|
| Pistole | 9×19 mm | kurz, rund, Messing (32×10 px) | 0.6 m warmweiß, jeder Schuss | S | klein | Loch S, wenig Splitter |
| MP | 9×19 mm | wie Pistole | 0.6 m, jeder 2. Schuss | S, flackernd | klein | S + Funken |
| Sturmgewehr | 5.56×45 / 7.62×39 | spitz, lang (48×10) | 1.0 m gelb-orange, jeder 3. | M | mittel | M + Splitterkranz |
| Kampfgewehr | 7.62×51 mm | spitz (56×12) | 1.2 m, jeder Schuss | M | groß | M–L |
| Scharfschütze | 7.62×51 / .338 / .50 BMG | lang (64×12, .50: 80×16) | 2.0 m + Luftschliere 0.3 s | L + Rauch | groß | L, Krater in der Mitte |
| Schrotflinte | 12 Gauge | rote Hülse (48×20) + 8–11 Schrotkugeln | 8–11 Mini-Spuren à 0.3 m | L | rote Hülse | Gruppe aus 8–11 kleinen Löchern |
| MG | 7.92×57 / 7.62×51 | 56×12 | 1.2 m rot-orange, jeder 2. | L | Gurtglieder + Hülsen | M |
| LMG | 5.56×45 / .30-06 | 48×10 | 1.0 m, jeder 3. | M | mittel | M–L |
| Minigun | 7.62×51 mm | 48×10 | durchgehender Strahl | XL, dreht sich | Hülsenstrom | viele S |
| Werfer | Rakete / 40 mm | 3D-Mesh + Rauchspur | – | `misslieMuzzleFireEff` | – | `missileExplosionEff` + Brick-Trümmer |
| Armbrust | Bolzen | 3D-Mesh, ohne Rauch | dünne Linie | – | – | Bolzen bleibt stecken |

**Hinweise:**
- Schusswaffen treffen im Engine sofort (Raycast). Die Leuchtspur ist rein optisch und fliegt mit etwa 400 m/s vom Lauf zum Treffpunkt.
- Im Referenzbild stimmen einige Kaliber nicht. In der Tabelle oben stehen die richtigen:
  - MP: 9 mm statt 5.56 mm
  - Sturmgewehr: 5.56 mm (AK: 7.62×39)
  - LMG: 5.56 mm oder .30-06

**Impact je Oberfläche:**

| Oberfläche | Effekt |
|---|---|
| Brick | Splitter in Brick-Farbe + Staub |
| Metall | Funken |
| Glas | Bruch (zerstörbar) |
| Holz | Späne |
| Wasser | Spritzer |
| Spieler | `hitImpact`. Unter 12: `hitImpactChild`, also Sterne statt Blut |
| Glückstreffer | `luckyImpact`, goldener Stern |

Einschusslöcher (`BulletMark`) bleiben 10 s, höchstens 64 gleichzeitig.

**Dateinamen:**
- `prj_<klasse>.png`
- `fx_muzzle_<s|m|l|xl>`
- `fx_impact_<oberfläche>_<s|m|l>`
- `snd_<waffe>_<fire|dry|clipout|clipin|boltup>`

---

## 9. Varianten, Upgrades, Haltbarkeit

### 9.1 Namens-Suffixe in `Weapon.BY`

| Suffix | Bedeutung | Werte |
|---|---|---|
| keins | Basiswaffe | wie in `waffenliste.csv` |
| `_G`, `_R`, `_B`, `_W`, `_C`, `_O`, `_S`, `_T`, `_A`, `02` | Farb- / Gold-Skin | gleich wie die Basis |
| `_SPECIAL` | Sonderedition | Basis + eigener Skin / eigenes Visier |
| `_MAX` | voll aufgerüstet | Basis + alle Upgrades auf Stufe 5 |
| `Q_…` | Event- / Saison-Variante | gleich wie die Basis |

Faustregel: Skins ändern nie die Werte. So bleibt das Balancing über alle rund 400 Einträge sauber.

### 9.2 Upgrades (Engine: `PimpManager`, 5 Stufen)

| Upgrade-Slot | Wirkt auf | Vorschlag pro Stufe |
|---|---|---|
| 0 Schaden | `AtkPow` | Schusswaffe +1, Nahkampf +2, Granate +5 |
| Wucht | `Rigidity` (`AddUpgradedShockf`) | +0.02 (max. 1.0) |
| 2 Rückstoß | `recoilPitch` | −3 % vom Basiswert |
| 3 Feuerrate | `rateOfFire` | +2 % vom Basiswert |
| 4 Munition | `maxAmmo` | +10 % Reserve |
| 5 Schlaggeschwindigkeit | `slashSpeed` (Nahkampf) | +0.05 |

### 9.3 Haltbarkeit (Engine)
- Jede Waffe hat `durabilityMax`.
- Verschlissene Waffen machen weniger Schaden (`applyDurabilityDamage`, Grenze `brokenRatio` = 0.4).
- Vorschlag: 1 Haltbarkeitspunkt pro Match.

---

## 10. Waffenliste

Die vollständige Zuordnung jeder Waffe steht in **`data/waffenliste.csv`**:
- Spalten: Engine-Name, Anzeigename, Klasse, Munition, Abweichungen von der Klasse, Visier, Besonderheit.
- Spalte `zuordnung`:
  - `fest` = reale Waffe mit eindeutiger Klasse.
  - `Vorschlag` = Event- oder Fantasy-Waffe, deren Typ aus dem Namen abgeleitet ist. Bitte im Spiel gegenprüfen.

| Klasse | Waffen |
|---|---|
| Pistole | BM9, BWP38, BWPP, Luger P08, BC1900, Glock 18, Anaconda, Desert Eagle, Taser |
| MP | Uzi, MP40, PPSh-41, K1, MP7 |
| Sturmgewehr | M16, AK-47, M4, StG 44, K2, FAMAS, G36K, HK416, L85A2, Beryl, C8A1, F2000, K11, Steyr AUG |
| Kampfgewehr | SCAR-H, HK417 |
| Scharfschütze | SSG 69, Mosin M91, AWM, JNG-90, TRG-42, Barrett M82A1 |
| Schrotflinte | Winchester 1893 |
| MG | MG 42, M60 |
| LMG | M1918 BAR |
| Minigun | Vulcan |
| Armbrust | Armbrust, Condor, Hornet, Hydra, Magierstab |
| Messer | Kampfmesser (BMK), M7 Bajonett |
| Werkzeug | Schraubenschlüssel, Rohrzange, Schlagstock, Bratpfanne, Event-Sticks |
| Schwer | Spielzeughammer, Event-/Turnier-Hammer, Feldspaten |
| Energie | Lichtschwert (blau/rot) |
| Granaten | Granate, KG-400, KGS-440, Zeitbombe, Sensorbombe, Fernzünder, Blend, Rauch, Gift, Event-Bomben |
| Event (Vorschlag) | Eraser, Predator, Ravager, Delta, Eco, Bard, Matiazo, Drake 3000, Gamma, Tsunamirama, Hellfire, Shaft, X-Wing, Needle, Moonlight, Oblivion, Wild-West-Reihe, Wasser-Reihe, Xmas-Reihe |
