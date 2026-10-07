# UI-Konzept – Brixel

Design-Bibel für den Neuaufbau der Spiel-Oberfläche: Struktur, Look, Komponenten, Motion, Partikel, Sound und Unity-Umsetzung.
Grundlage sind das UI-Inventar (`ref/Brixel_UI-Inventar.html`, Stand 06.10.2026, **67 Einträge**) als Feature-Liste und das Asset-Sheet (`ref/ui-asset-sheet.webp`) als Stilvorlage.
Struktur und Abläufe folgen großen Games (Valorant, Fortnite, CoD, Apex). Keine Funktion aus dem Inventar geht verloren; `tools/check_ui_migration.py` prüft das maschinell.

| Datei | Inhalt |
|---|---|
| `UI_KONZEPT.md` | Dieses Dokument |
| `data/ui_migration.csv` | Jeder der 67 Inventar-Einträge mit allen Knopf-Texten → neuer Ort (Detail zu Kapitel 8) |
| `data/ui_assets.csv` | Alle UI-Assets mit ID, 9-Slice, Zuständen und Prompt-Motiv (IDs werden hier referenziert) |
| `artifact/ui-katalog.html` | Prompt-Bibliothek und durchsuchbare Migration |
| `artifact/ui-prototyp.html` | Klickbarer Prototyp |

**Legende**

| Zeichen | Bedeutung |
|---|---|
| **NEU** | Gibt es heute nicht oder weicht vom Inventar ab. Bei geänderten Einschränkungen steht die Begründung dabei. |
| „…“ | Text genau so, wie er im Inventar steht (Platzhalter wie `n`, `X`, `<Map>` bleiben Platzhalter) |
| GROSS | Knopf-Beschriftung wie im Code |
| P · B · M · A | Plaza · Bauplatz · Match · Asset-Karte |
| Ord / Ebene | alte / neue Zeichenreihenfolge der Canvas (höher liegt oben) |
| abgeleitet | Wert nicht im Sheet gemessen, sondern aus gemessenen Werten abgeleitet |
| › | Pfad im Menü, z. B. KARRIERE › Bestenlisten |

## Inhalt
1. [Ziel & Prinzipien](#1-ziel--prinzipien)
2. [Vorbilder](#2-vorbilder)
3. [Screen-Map](#3-screen-map)
   - [3a. TEAM-Funktionen (NEU)](#3a-team-funktionen-neu)
4. [Kleines Esc-Menü & Bauplatz-Fenster](#4-kleines-esc-menü--bauplatz-fenster)
5. [Tab-Liste](#5-tab-liste)
6. [Navigations-Flows](#6-navigations-flows)
7. [Welt: was entfällt](#7-welt-was-entfällt)
8. [Migration (67 Einträge)](#8-migration-67-einträge)
9. [Canvas-Ebenen](#9-canvas-ebenen)
10. [Skalierung & UI-Größe](#10-skalierung--ui-größe)
11. [Design-Tokens](#11-design-tokens)
12. [Komponenten-Katalog](#12-komponenten-katalog)
13. [Kampf-HUD](#13-kampf-hud)
14. [Baumodus-HUD](#14-baumodus-hud)
15. [Motion-Spec](#15-motion-spec)
16. [Partikel-Spec](#16-partikel-spec)
17. [Sound-Hooks](#17-sound-hooks)
18. [Unity-Umsetzung](#18-unity-umsetzung)
19. [Replays für alle Spieler](#19-replays-für-alle-spieler)
20. [Offene Punkte & Entscheidungen](#20-offene-punkte--entscheidungen)
21. [Dateien & Pflege](#21-dateien--pflege)

---

## 1. Ziel & Prinzipien

### 1.1 Ziel
- **Ein Hauptmenü statt verstreuter Wege.** Heute erreicht man Fenster über Plaza-Stationen (E), das Esc-Menü und Querverweise, und jedes Fenster ist anders gebaut. Neu gibt es in der Plaza einen **Hub** mit 6 Reitern. Auf Bauplatz, Asset-Karte und im Match öffnet Esc ein **kleines Esc-Menü**.
- **Ein Look** aus dem Asset-Sheet: goldene Platten mit Fasen, Lippe und Nieten auf nachtschwarzem Grund.
- **Ultra smooth und clean:** Menüs animieren mit Federn und Staffelung, Spielzustände im HUD schalten sofort, und Partikel gibt es dort, wo etwas gewonnen wird.
- **Nichts geht verloren:** Alle 67 Einträge, jeder Unterdialog, jeder Knopf-Text, jeder Zähler und jeder Zugangsweg haben einen neuen Ort.

### 1.2 Prinzipien

| # | Prinzip | Regel | Prüffrage |
|---|---|---|---|
| 1 | Ein globales Menü | P: Hub mit LOBBY · SPIELEN · ERSTELLEN · SPIND · LADEN · KARRIERE. B, A, M: kleines Esc-Menü (Kapitel 4). Keine Funktion ist nur über die Welt erreichbar. | Erreicht man die Funktion mit Esc und höchstens 3 Schritten? |
| 2 | Stationen sind Deko | Plaza-Gebäude, Stationen und Portale gehören nicht zur UI: kein Stations-Hinweis, kein Stations-Fenster, kein Teleport (Kapitel 7). | Verweist ein Text noch auf eine Station? |
| 3 | Konsistenz | Eine Komponente je Zweck (eine Tab-Liste, ein Dialog, ein Toast, eine Karte). Die Primäraktion steht immer unten rechts, Zurück ist immer Esc bzw. Gamepad-B. | Gibt es zwei Bauweisen für dasselbe? |
| 4 | Lesbarkeit | Mindestens 14 px bei 1080p. Kontrast für Text mindestens 4,5 : 1, für Grafik 3 : 1 (Werte in 11.2). Zähler mit gleich breiten Ziffern. Gold markiert Aktion und Fokus, Fließtext ist nie gold. | Ist der Text auf dem dunkelsten Hintergrund noch lesbar? |
| 5 | Controller-first-Fokus | Jedes Element ist per Steuerkreuz erreichbar (PadNavigator). Der Fokus-Ring ist sichtbar, und die Tastenhinweise wechseln mit dem Eingabegerät. | Kommt man ohne Maus überall hin und wieder zurück? |
| 6 | Barrierefreiheit | Stufen und Status nie nur über die Farbe zeigen, sondern immer mit Name und Symbol. Dazu Farbsehen-Modi, **NEU** „Animationen reduzieren“ und **NEU** UI-Größe (Einstellungen › Barrierefreiheit). | Funktioniert der Screen in Graustufen und mit reduzierter Bewegung? |
| 7 | Animation mit Zweck | Menüs animieren, um Herkunft, Ergebnis und Status zu zeigen. Spielzustände im HUD schalten sofort; Effekte verzögern nie die Anzeige (15.2). Animationen blockieren nie die Eingabe. | Würde der Screen ohne die Animation etwas verschweigen? |
| 8 | Ruhe | Sauberes Raster, großzügige Abstände, eine Primäraktion je Ansicht, nichts überladen. | Was kann weg? |
| 9 | Einschränkungen bleiben | Schalter, Rollen, „nur Inhaber“, „nicht im Match“ und Modus-Grenzen bleiben wie im Inventar. Jede Änderung ist **NEU** markiert und begründet (3.14). | Steht die Änderung in 3.14? |

---

## 2. Vorbilder
Welche Muster woher kommen, in eigenen Worten beschrieben. Übernommen wird das Prinzip, nicht das Aussehen. Der Look kommt allein aus dem Sheet.

| Muster bei uns | Vorbild | Was wir daraus übernehmen |
|---|---|---|
| LOBBY mit eigener Figur, Party-Figuren und großem SPIELEN-Knopf unten rechts | Fortnite, Valorant | Die Startseite zeigt die Gruppe als Figuren. Leere Plätze laden zum Einladen ein, und der wichtigste Knopf ist immer an derselben Stelle. |
| Modus-Karte über dem SPIELEN-Knopf mit WECHSELN | Fortnite | Der gewählte Modus steht sichtbar über dem Startknopf. Ein Klick führt zur Modus-Auswahl. |
| Reiter oben mit LB/RB-Hinweisen, Fußleiste mit Tastenhinweisen im Konsolen-Stil | CoD, Apex | Die Navigation ist mit Schultertasten blätterbar. Die Hinweise unten passen sich dem Eingabegerät an und sind mit der Maus klickbar. |
| Sozial-Panel, das rechts einfährt | Valorant, CoD | Freunde, Party und Clan liegen in einem Panel über dem Menü, statt eine eigene Seite zu sein. |
| ZUSCHAUEN direkt in der Freundes-Zeile | Fortnite | Wer einem Freund zusehen will, sucht ihn nicht in einer zweiten Liste. |
| System-Knopf mit Dropdown (Einstellungen, Hilfe, Beenden) | Fortnite | Selten genutzte Systemfunktionen liegen gesammelt hinter einem Knopf oben rechts. |
| Karriere mit Match-Verlauf, Replays und Highlights | Fortnite, Overwatch, Valorant | Alles über das eigene Spiel liegt an einem Ort, auch die Aufzeichnungen. |
| Kleines Esc-Menü im Spiel über dem geblurrten Bild | Valorant, CoD | Im laufenden Spiel stehen nur Spiel-Aktionen bereit, kompakt und schnell wieder weg. |
| Tab-Liste halten, zum Bedienen anheften | Counter-Strike, Valorant | Halten zeigt die Liste. Erst ein bewusster Klick gibt den Mauszeiger frei für Stumm, Melden und Profil. |
| Einstellungen mit Kategorien oben und Beschreibungs-Panel rechts | CoD, Apex | Jede Zeile erklärt sich rechts mit Text und Vorschau. |
| Barrierefreiheit als eigener Reiter, UI-Größe als Einstellung | CoD, Fortnite, Apex | Hilfen sind gebündelt statt in anderen Seiten versteckt. |
| Bau-Leiste unten Mitte mit Plätzen 1–9, Werkzeuge mit Tasten | Fortnite (Baumodus), Minecraft (Schnellleiste) | Der aktive Platz ist angehoben, und das Werkzeug zeigt seine Taste. |
| Popup-Warteschlange beim Start (Neuigkeiten → Belohnung → Einführung) | Fortnite, Apex | Popups kommen nacheinander statt übereinander. |
| Such-Pille mit Timer, auch bei geschlossenem Menü | Fortnite, Apex | Man kann während der Suche weiter herumlaufen und sieht trotzdem den Stand. |
| Ergebnis-Sequenz mit Titelkarte, Belohnungs-Zählern und Rang-Balken | Valorant, Apex, CoD | Eine kurze, überspringbare Sequenz vor der Tabelle. |
| Gesundheit/Rüstung unten links, Waffe und Munition unten rechts, Schadens-Rest im Balken | Apex, CoD | Die Werte sind sofort richtig, und ein heller Rest zeigt, wie viel gerade verloren ging. |
| Gold-Platten, Truhen, Strahlenkranz, Goldstaub | Mobile-Strategiespiele im Stil des Sheets (z. B. Clash Royale) | Belohnungen fühlen sich „wertig“ an, ohne die Bedienung zu stören. |

---
## 3. Screen-Map

### 3.1 Überblick
```
Brixel-UI
├─ System-Screen: Ladebildschirm, Anmeldung, Fehler ............................ Ebene 100
├─ Plaza (P)
│  ├─ Welt + HUD (Basis-HUD, MissionsWidget, Party-Liste, Einführung-Karte, Such-Pille)
│  └─ HUB  [Esc / Start] ...................................................... Ebene 40
│     ├─ Top-Leiste: Logo · LB · LOBBY  SPIELEN  ERSTELLEN  SPIND  LADEN  KARRIERE · RB
│     │              Such-Pille · Kristalle Splitter Brix · Sozial · Glocke · Post · TEAM · Profil · System
│     ├─ LOBBY ........ (Unterseite Neuigkeiten)
│     ├─ SPIELEN ...... Schnellspiel · Server-Browser · Gewertet · Turniere · Zuschauen
│     ├─ ERSTELLEN .... Meine Maps · Mitbauen · Vorlagen · Map-Galerie
│     ├─ SPIND ........ Loadout · Aussehen · Inventar · Werkstatt · Testgelände
│     ├─ LADEN ........ Empfohlen · Katalog · Glücksbrett
│     ├─ KARRIERE ..... Profil · Match-Verlauf · Replays & Highlights · Waffen-Mastery · Erfolge · Tagesmissionen · Bestenlisten
│     ├─ TEAM-Seite (Schild, nur Staff, Kapitel 3a): Moderation · Spielerverwaltung · Wirtschaft · Live-Betrieb · Entwicklung · Verwaltung
│     ├─ System-Dropdown: Einstellungen · Hilfe und Support · Fehler melden · Foto-Modus · Spiel beenden
│     ├─ Glocke-Verlauf (NEU)
│     └─ Fußleiste: Statuszeile · Tastenhinweise
├─ Bauplatz (B): Bau-HUD · kleines Esc-Menü (BAUPLATZ VERWALTEN; TEAM nur Staff, NEU) ... Ebene 40
├─ Asset-Karte (A): kleines Esc-Menü (TEAM nur Staff) ................................ Ebene 40
├─ Match (M): Kampf-HUD/Bau-HUD · kleines Esc-Menü · Warteraum · Tab-Liste · Funkrad · Ergebnis
├─ Spiel-Overlays 30–34: Warteraum 30 · Tab-Liste 31 · Funkrad 33 · Palette, Bauvorlagen-Werkzeug 34
├─ Coachmarks der Einführung (über dem Hub) ......................................... Ebene 41
├─ Sozial-Panel (P über Hub; B, A über SOZIAL; nicht im Match) ...................... Ebene 42
├─ Ergebnis 43 · Einstellungen (Vollbild) 44 · Ergebnis-Sequenz 45 · ReplayViewer 46
├─ Dialoge · Hilfe und Support 50 · Profil 51 · Melden 52 · Spieler-Aktionen 53
└─ Popups 58 · Foto-Modus 60 · Benachrichtigungen/Toasts/Wartungsband 70
```
Neu sind (**NEU**): der Hub mit allen Reitern und Leisten, das kleine Esc-Menü, das Sozial-Panel, die TEAM-Seite als Vollbild, das System-Dropdown, die Glocke, die Tab-Liste als eine Komponente, Bau- und Kampf-HUD in der neuen Aufteilung. Die Inhalte darin kommen aus dem Inventar und stehen in „…“ bzw. als GROSS-Knöpfe.

### 3.2 Hub-Anatomie (nur P)
Der Hub liegt über der geblurrten Plaza (Blur 8 px, Abdunkeln 45 %, `bg_vignette`); in der LOBBY steht dahinter `bg_hub_backdrop` mit dem Podest. Die Maße sind logische Pixel bei 1920×1080 (Skalierung siehe Kapitel 10).

| Zone | Maße | Inhalt (von links nach rechts) | Verhalten |
|---|---|---|---|
| Top-Leiste | Höhe 72 | Logo „BRIXEL“ · LB-Hinweis (Tastatur: Q) · 6 Reiter LOBBY · SPIELEN · ERSTELLEN · SPIND · LADEN · KARRIERE · RB-Hinweis (Tastatur: E) | Aktiver Reiter: `tab_active` mit gleitendem `tab_underline`. Zähler-Badges am Reiter (3.11). |
| Top-Leiste rechts | – | **NEU** Such-Pille (nur während einer Suche: Timer + ABBRECHEN; ersetzt den blockierenden Warten-Dialog) · Pillen Kristalle · Splitter · Brix (**NEU**: „+“ an Kristalle → LADEN) · **NEU** Sozial-Knopf (Freunde/Party, „n online“, Badge „n neu“) · **NEU** Glocke · Post (Umschlag, „99+“) · **NEU** TEAM-Schild (rot, nur Staff) · **NEU** Profil-Chip (Rang-Abzeichen, XP-Ring) · **NEU** System-Knopf | Profil-Chip → KARRIERE › Profil. Sozial-Knopf → Sozial-Panel. Post → Sozial-Panel › Post (breite Seite). TEAM-Schild → TEAM-Seite. System-Knopf → Dropdown. |
| Unterreiter-Leiste | Höhe 52 | Unterreiter des aktiven Reiters | LT/RT bzw. 1–9; Zähler je Unterreiter |
| Inhalt | Rand 48, 12 Spalten, Abstand 24 | Seite des Unterreiters | Seitenwechsel siehe 15.7 |
| Fußleiste | Höhe 56 | links Statuszeile (ersetzt die Statuszeile aus `UiFactory.Window`; ohne Meldung steht der Ort „\<Map\> \| n Spieler“, wie früher im Kopf des Esc-Menüs). Rechts **NEU** die Tastenhinweise im Konsolen-Stil, je Gerät: Tastatur „Esc Zurück“ · „Q/E Reiter“ · „Enter Auswählen“ · „F Sozial“; Gamepad „B Zurück“ · „LB/RB Reiter“ · „A Auswählen“ · „Y Sozial“; je Kontext „X Details“. Auf oberster Ebene heißt Zurück „Zurück ins Spiel“ (ersetzt „WEITER“). | Hinweise wechseln mit dem zuletzt benutzten Gerät und sind mit der Maus klickbar. |
| Ambient | ganze Fläche | **NEU** Goldstaub `fx_gold_dust` hinter dem Inhalt (16.1) | aus bei „Animationen reduzieren“ |

**System-Dropdown** (**NEU**; Zahnrad oben rechts, Gamepad View):

| Eintrag | Ziel | Bedingung |
|---|---|---|
| Einstellungen | Einstellungen (Vollbild) | immer |
| Hilfe und Support · neue Antwort | Hilfe und Support (Ebene 50) | Schalter |
| Fehler melden | Hilfe und Support, Formular mit Kategorie „Fehler im Spiel“ (FEHLER MELDEN) | Schalter |
| Foto-Modus | Foto-Modus (Hub schließt) | P (Regeln wie heute) |
| Spiel beenden (rot) | **NEU** Bestätigung „Spiel beenden?“ → Spiel zu | immer |

„Zur Plaza“ gilt heute nur außerhalb der Plaza („außer Plaza“). Weil der Hub nur in der Plaza existiert, erscheint der Eintrag dort nie; er steht in den kleinen Esc-Menüs (Kapitel 4).

### 3.3 LOBBY (Start-Reiter, **NEU**)

| Bereich | Inhalt | Ziel / Verhalten |
|---|---|---|
| Mitte: Party-Bühne (**NEU**) | Eigene Figur (Aussehen aus SPIND) und Party-Mitglieder als Figuren auf `lobby_podium`. Der Leiter trägt die Krone, darunter stehen Name, Kennzeichen (`UiNameBadges`), Ort („hier“, „offline“ …) und **NEU** ein Bereit-Haken. Leere Plätze bis „PARTY n / m“ zeigen „+“. | „+“ → Sozial-Panel › Freunde (Einladen). Klick auf ein Mitglied → Profil-Popup. Klick auf die eigene Figur → SPIND › Aussehen. |
| unten rechts: Modus-Karte (**NEU**) | Gewählter Modus (Modus-Symbol `mode_*`) und Kanal (Anfänger · Offen · Veteranen · Clan), Knopf WECHSELN | WECHSELN → SPIELEN › Schnellspiel |
| unten rechts: SPIELEN | Großer goldener Knopf `btn_play_hero` | Startet den Schnellstart (wie SCHNELLSTART heute) mit Modus und Kanal der Modus-Karte → Such-Pille. Während der Suche zeigt der Knopf Timer und ABBRECHEN (**NEU**). In einer Party gilt die heutige Regel inkl. Unterdialog „Allein beitreten?“. |
| links oben: Karussell (**NEU** im Menü) | Folien wie auf der Bühnen-Leinwand: Ankündigung, Saison, News, „Event läuft“ / „Event“, Map der Woche, Clan des Monats, die besten drei; Punkte-Reihe; Wechsel alle ~8 s | Klick → LOBBY › Neuigkeiten |
| links: Event-Bonus | Chip „Gerade: …“ | Klick → Neuigkeiten |
| links: Tagesmissionen | Widget „TAGESMISSIONEN“, „neu in …“, 3 Zeilen mit Balken, Wert oder „erledigt“ | Klick → KARRIERE › Tagesmissionen |
| links: Tägliche Belohnung | Truhe `reward_chest_closed` mit Badge „abholbar“ | Klick → Popup „Tägliche Belohnung“. Nur mit Schalter. |
| links: Einführung | Karte „Einführung i/n: \<Schritt\>“ für neue Spieler | Klick → Einführung-Dialog |

**Unterseite Neuigkeiten** (**NEU**-Name, alt Fenster „Bühne“; Esc bzw. Gamepad-B → LOBBY):

| Block | Inhalt und Knöpfe |
|---|---|
| Kopf | Bonus-Zeile „Gerade: …“ |
| links | „Ankündigungen (n)“; „Events (n)“ mit „LÄUFT …“ / „BEGINNT …“ |
| rechts | „Map der Woche“ mit IN DER GALERIE (→ ERSTELLEN › Map-Galerie, Detail) · „Clan des Monats“ mit CLAN ANSEHEN (→ Overlay mit Clan-Seite und Mitgliedern, ZURÜCK) · „Die besten drei“ (→ KARRIERE › Bestenlisten) |
| unten | **NEU** „Was ist neu in \<Version\>“ wieder aufrufbar |

### 3.4 SPIELEN

| Unterreiter | Inhalt (Inventar) | Knöpfe | Unterdialoge |
|---|---|---|---|
| Schnellspiel (**NEU** als Seite) | Kanal-Segmente Anfänger · Offen · Veteranen · Clan (mit Rangbereich). Kachel „Alle Modi“ (= heutiger SCHNELLSTART) und 11 Modus-Kacheln: Team-Deathmatch, Deathmatch, Flaggenjagd, Entschärfung, Bauen und Zerstören, Freier Fall, Verteidigung, Zombie-Ausbruch, Kopfgeld, Ausbruch, Gemeinsam bauen | Kachel wählen (setzt die Modus-Karte der LOBBY) · SCHNELLSTART | Warten „Suche ein Match …“ / „Server wird gestartet …“ mit ABBRECHEN; **NEU**: Der Dialog blockiert nicht mehr. Esc bzw. Gamepad-B schließt ihn, die Suche läuft als Such-Pille weiter. · „Allein beitreten?“ |
| Server-Browser (**NEU**-Name, alt „Arena / Räume“) | „Räume finden, eigene erstellen oder direkt losspielen.“ · Kanal-Segmente · Modus-Auswahl („Alle Modi“ und Modi) · Spalten RAUM / MODUS / MAP / SPIELER / STATUS · Zeile mit Vorschau, Schloss, Herz bei Freunden, „[A] gegen [B]“ | RAUM ERSTELLEN · AKTUALISIEREN · Zeile: BEITRETEN / „GESPERRT“ / „VOLL“ / „ENDET“ / „LÄUFT“ | „Passwort“ (Feld, BEITRETEN / ABBRECHEN) · Warten · „Allein beitreten?“ (ALLEIN BEITRETEN / ABBRECHEN) |
| Server-Browser › Ansicht „Raum erstellen“ | „Raum“: Name, Modus, Kanal, Gegner-Clan, Passwort · „Spiel“: Spieler (Regler), Zeitlimit, Ziel, Team-Balance, Beitritt im Spiel, Waffen (Alle / Nur Nahkampf / Nur Pistolen / Nur Gewehre / Nur Scharfschützen), Wetter (Klar/Regen/Nebel/Schnee/Wechselnd), Tageszeit (Tag/Abend/Nacht/Wechselnd) · rechts „MAP“-Karten | ZURÜCK · RAUM ERSTELLEN | – |
| Gewertet | „Gewertete Matches“, Saison-Zeile, 2 Karten (Team-Deathmatch, Entschärfung) mit Rang, Wertung, Siege | SUCHEN · SUCHE ABBRECHEN · BESTENLISTE (→ KARRIERE › Bestenlisten, Chip Gewertet) | – |
| Turniere | links Segmente Anmeldung offen / Läuft / Beendet / Abgesagt; rechts Details mit Belohnungen und Baum bzw. Runden („Großes Finale“, „Verliererbaum, Runde n“ …); Felder „Name des Teams“, „Mitspieler (Namen mit Komma)“ | ZUSCHAUEN (→ SPIELEN › Zuschauen, vorgefiltert → Live im ReplayViewer, wie heute) · ANMELDEN · ABMELDEN · ZUM MATCH · **NEU** REPLAY an beendeten Matches | – |
| Zuschauen | Live-Liste: Freund / Turnier / Clan-Krieg / Spielteam · Modus · Verzögerung · Zuschauer | ZUSCHAUEN / „VOLL“ · AKTUALISIEREN | – (öffnet den ReplayViewer live) |

Die Kopf-Knöpfe der alten Arena werden verteilt: SCHNELLSTART → LOBBY SPIELEN bzw. Schnellspiel, GEWERTET und TURNIERE → eigene Unterreiter, RAUM ERSTELLEN → Server-Browser. Das Fenster-SCHLIESSEN aller alten Panels ist im Hub Esc bzw. Gamepad-B.

### 3.5 ERSTELLEN (P)

| Unterreiter | Inhalt (Inventar) | Knöpfe | Unterdialoge |
|---|---|---|---|
| Meine Maps | Kopf „MEINE MAPS · EINE MAP JE SLOT …“; Karten mit Vorschaubild, „SLOT n“, „Map in Slot n“ / „Neuer Bauplatz“ / „Leer“ / „Gesperrt“, „Wird gerade bebaut · n/m“ / „Niemand da“ | BETRETEN · Blättern ZURÜCK / WEITER · **NEU** „Gesperrt“ verlinkt LADEN › Katalog › Map-Slots | – (Toast „Die Map wird vorbereitet.“ bleibt) |
| Mitbauen | Kopf „MAPS, BEI DENEN ICH MITBAUE“; Karten wie oben | BETRETEN · ZURÜCK / WEITER | – |
| Vorlagen (**NEU** auch in P) | Chips Geteilt / Meine; Neu / Beste; Zeilen mit „▲ n“, „▼ n“; Blättern ‹ / › | LÖSCHEN · TEILEN / NICHT TEILEN · ÜBERNEHMEN nur auf dem Bauplatz (in P ausgegraut mit Hinweis **NEU** „Nur auf dem Bauplatz“) | – |
| Map-Galerie | „Map-Galerie“, „Maps der Community: ansehen, bewerten, herunterladen und darauf spielen.“ · Sortier-Chips Neu · Beliebt heute · Beliebt Woche · Top · Hall of Fame · Eigene · Heruntergeladen · Modus-Auswahl · Suche „Map suchen …“ · Karten mit „HALL OF FAME“ / „OFFIZIELL“ / „GESPERRT“ / „AUSGEBLENDET“, ▲▼, Spiele, Preis, Version, Downloads, Kommentare · Detail: Bild, „BEWERTUNG“, „ZAHLEN“, „BESCHREIBUNG“, „VERSIONEN“, „KOMMENTARE (n)“ | SUCHEN · ZURÜCK / „Seite x / y“ / WEITER · DAUMEN HOCH / DAUMEN RUNTER · SENDEN · HERUNTERLADEN (n BRIX) · MELDEN · RAUM AUF DIESER MAP ERSTELLEN (→ Server-Browser › „Raum erstellen“ mit vorgewählter Map) · ZUR LISTE | „Map melden“: „GRUND“ (Anstößiger Inhalt, Anstößiger Name, Spam, Farming, Sonstiges), „DETAILS (FREIWILLIG)“, ABBRECHEN / MELDEN · „In einen Slot herunterladen“: Chips „SLOT“ (1–6: leer / belegt / gesperrt), Warnung, ABBRECHEN / HERUNTERLADEN / ÜBERSCHREIBEN |

„Dieser Bauplatz“ und „Veröffentlichen“ gibt es nur im Bauplatz-Fenster auf B (4.5).

### 3.6 SPIND (P)
Die Vorschau der eigenen Figur steht auf allen Unterreitern links.

| Unterreiter | Inhalt (Inventar) | Knöpfe | Unterdialoge / Overlays |
|---|---|---|---|
| Loadout (**NEU**-Name, alt „Ausrüstung“) | Effekt-Leiste (Summen der Attribute); Slot-Gruppen Waffen · Kleidung · Accessoires · „Hotbar – wirkt in Modi mit Gefahr“ · „Werkzeug und Flug – wirkt auf dem Bauplatz“; Slot-Karte: Item, „leer“, „Klicken zum Belegen“, Sterne | – | „\<Slot\> belegen“: Karte „Ablegen“, Item-Karten mit „AUSRÜSTEN“ / „AUSGERÜSTET“, ZURÜCK |
| Aussehen | „So sehen dich die anderen Spieler.“; Farbreihen Haut, Oberteil, Hose, Schuhe; Formreihe „Körper“ mit < / > („Variante n“) | SPEICHERN · ABBRECHEN | – |
| Inventar | Filter-Chips Alle, Waffen, Kleidung, Access., Verbrauch, Werkzeug, Gems; Raster mit Abzeichen „AN“; Detail: Laufzeit, „BONI“, „UPGRADES“ | ZERLEGEN (+n SPLITTER) · IN DER WERKSTATT AUFWERTEN · ABLEGEN · AUSRÜSTEN | – |
| Werkstatt | Liste „Aufwertbar“ / „Nicht aufwertbar“; Detail mit Sternen, „ATTRIBUT WÄHLEN“ (Stufen-Karten, „MAX“), „GEM“-Karten, Chance und Gebühr | VERSUCHEN / „KEIN GEM“ / „ZU WENIG BRIX“ · ZERLEGEN | Ergebnis „Erfolg!“ / „Kein Erfolg“ mit WEITER · „ITEM ZERLEGEN“ mit ENDGÜLTIG ZERLEGEN / ABBRECHEN |
| Testgelände (**NEU**-Name, alt „Waffenständer“) | „Leihwaffen zum Ausprobieren …“; Waffenkarten (Klasse · Slot, Werte) | Leihwaffe wählen (rüstet sie wie heute aus) · EIGENE AUSRÜSTUNG | – |

Zum Testgelände gehört kein Teleport und kein Weg in der Welt. Geschossen wird wie heute am Schießstand in der Plaza; Ziele und Schießstand-Karte sind Welt-UI bzw. Kampf-HUD.

### 3.7 LADEN (P)

| Unterreiter | Inhalt (Inventar) | Knöpfe | Unterdialoge / Overlays |
|---|---|---|---|
| Empfohlen (**NEU**) | Große Karten für Event-Items, Rabatte („-n %“) und neue Items, gleiche Karte wie im Katalog | wie Katalog-Detail | wie Katalog |
| Katalog | Kopf „Laden“, „Waffen, Kleidung und Ausrüstung für Brix. Preise gelten je Laufzeit.“. Kategorie-Leiste aus den Inhalten: Waffen · Kleidung · Accessoires · Verbrauch · Bau-Werkzeuge · Flug · Map-Slots · Gems · Event. Waffen-Filter-Chips: Alle, Hauptwaffe, Sekundärwaffe, Nahkampf, Spezial. Karten: Symbol, Name, Typ, „ab …“, Schloss „Rang n“, Abzeichen „BESITZ“ / „AKTIV“ / „-n %“. Detail: Name, Typ („stapelbar“, „Abklingzeit“), Sperre; Balken Schaden, Feuerrate, Magazin, Nachladen; „BONI“; Besitz-Zeile; Chips „LAUFZEIT“: 1 Tag, 7 Tage, 30 Tage, Dauerhaft | KAUFEN · Preis / „GESPERRT“ / „DAUERHAFT IM BESITZ“ · VERSCHENKEN (→ Sozial › Post, „Neue Nachricht“ mit Geschenk) | „KAUF BESTÄTIGEN“: Guthaben, Ladekreisel, JETZT KAUFEN / ABBRECHEN |
| Katalog im Geschenk-Modus | Aufruf aus Post „AUS DEM LADEN“: **NEU** Banner „Geschenk für X“ (`reward_banner`) | **NEU** ZURÜCK ZUR NACHRICHT · VERSCHENKEN übernimmt das Item als Geschenk | wie Katalog |
| Glücksbrett | Kopf „Glücksbrett“, „Saison · endet in · n von m Feldern offen“, Münz-Pille; Raster mit „?“-Feldern, Blättern < / >, „Seite“; Seitenleiste „LETZTER GEWINN“, „NOCH IM BRETT“ | TAGESMÜNZE ABHOLEN / „NÄCHSTE MÜNZE IN …“ · QUOTEN | Gewinn: Stufe (Gewöhnlich / Ungewöhnlich / Selten / Episch / Hauptgewinn), SUPER · „Quoten“: GEWINN / STUFE / FELDER / CHANCE, SCHLIESSEN |

Außerhalb der Plaza (B, A) zeigt „AUS DEM LADEN“ in der Post den Hinweis „Nur in der Plaza“ mit ZUR PLAZA (**NEU**; heute öffnete sich dort das Laden-Fenster). Grund: Den Hub gibt es nur in der Plaza (3.14 #23). AUS DEM INVENTAR und OHNE gehen überall.

### 3.8 KARRIERE (P)

| Unterreiter | Inhalt (Inventar) | Knöpfe |
|---|---|---|
| Profil | Kopf: Rang-Abzeichen, Name, Kennzeichen, „Rang n · Name“, XP-Balken (Guthaben steht in der Top-Leiste). Kacheln Matches, Siege, Niederlagen, Kills je Tod, Kills, Assists, Kopftreffer, Spielzeit. Tabelle MODUS / MATCHES / SIEGE / NIEDERL. / KILLS / TODE / ASSISTS / KOPFTREFFER / K/T | – |
| Match-Verlauf (**NEU**) | Liste der eigenen Matches: Datum, Modus, Map, Ergebnis, K/T, Punkte | REPLAY (→ ReplayViewer, Kapitel 19) |
| Replays & Highlights (**NEU**) | Chips Meine Replays · Highlights („Spielzug der Runde“) · Turnier-Replays; Karten mit Map, Modus, Dauer, Alter | ABSPIELEN · **NEU** LÖSCHEN (nur eigene Highlights) |
| Waffen-Mastery | Stufen-Balken „Stufe n / m“, Punkte, „-n % im Laden“ | – |
| Erfolge | Karten mit Fortschritt und „+n Brix“ | – |
| Tagesmissionen | Karten mit „+XP · +Brix · +1 Münze“, Reset-Zeile | – |
| Bestenlisten | „Bestenlisten“, „Die besten 100 Spieler …“; Chips Rang · Kills · Siege · Clans · Saison (bei laufender Saison) · Gewertet; Filter Modus (Kills, Siege), Warteschlange Team-Deathmatch / Entschärfung (Gewertet); Spalten PLATZ / SPIELER bzw. CLAN / RANG bzw. MITGLIEDER / XP, KILLS, SIEGE, PUNKTE oder WERTUNG; Zeile „Dein Platz“ | MEIN PROFIL (→ KARRIERE › Profil) |

**Fremdes Profil** bleibt ein Popup (Ebene 51) mit den Reitern Übersicht und Waffen-Mastery und allen Knöpfen: FREUND ENTFERNEN / ANFRAGE ANNEHMEN / „ANFRAGE GESENDET“ / ALS FREUND · PARTY EINLADEN · FLÜSTERN · POST · SPERREN / ENTSPERREN · MELDEN · BESTENLISTEN · SCHLIESSEN, dazu **NEU** KONTO-AKTE ÖFFNEN (nur Staff mit Leserecht, auch im Match; 3a.5). In P öffnen POST (Sozial-Panel › Post › Neue Nachricht an X) und BESTENLISTEN (KARRIERE › Bestenlisten) ihre Ziele. In B und A öffnet POST das Sozial-Panel; BESTENLISTEN zeigt „Nur in der Plaza“ mit ZUR PLAZA (**NEU**). **Im Match sind POST und BESTENLISTEN ausgeblendet (NEU)**: Es gibt dort weder Sozial noch Hub-Seiten (Begründung 3.14 #17).
**Eigenes Profil außerhalb des Hubs** (B, A, M): dasselbe Popup im Eigen-Modus mit allen 4 Reitern (Übersicht · Waffen-Mastery · Erfolge · Tagesmissionen), geöffnet über die eigene Zeile der Tab-Liste (Kapitel 5).

### 3.9 Sozial-Panel, TEAM-Seite

**Sozial-Panel** (**NEU** als Panel statt Fenster; rechts einfahrend, Breite 560, Ebene 42; in P über den Sozial-Knopf, F bzw. Gamepad-Y oder einen „+“-Platz der LOBBY, in B und A über SOZIAL im kleinen Esc-Menü, **nicht im Match** wie heute). Die Reiter-Chips tragen die Zähler wie heute.

| Reiter | Inhalt (Inventar) | Knöpfe |
|---|---|---|
| Freunde | Feld + Anfrage; „Freunde (n / max, n online)“ mit Ort; „Anfragen an dich“; „Von dir gesendet“ | ANFRAGE SENDEN · Zeile: EINLADEN · FLÜSTERN · FOLGEN · **NEU** ZUSCHAUEN (nur wenn der Freund live in einem Match ist; in B/A „Nur in der Plaza“) · **NEU** Profil · ANNEHMEN / ABLEHNEN · ZURÜCKZIEHEN |
| Party | Feld + Einladen; „Mitglieder (n / m)“; „Einladungen an dich“; „Offene Einladungen der Party“ | EINLADEN · PARTY GRÜNDEN · RAUSWERFEN · LEITUNG GEBEN · PARTY VERLASSEN · AUFLÖSEN · ZUM LEITER · PARTY FOLGEN: AN/AUS |
| Clan | ohne Clan: „Clan gründen“, „Einladungen an dich“; mit Clan: Emblem, Werte, Kurzliste | CLAN GRÜNDEN · CLAN-RANGLISTE (→ KARRIERE › Bestenlisten › Clans; in B/A „Nur in der Plaza“, **NEU**) · Öffnen der breiten Clan-Seite |
| Post | Chips Eingang / Ausgang, Kurzliste mit „Geschenk“ | NEUE NACHRICHT · Öffnen der breiten Post-Seite |
| Plazas | „Plazas mit Bekannten (n)“ (ersetzt „Zu Freunden wechseln“) | AKTUALISIEREN · WECHSELN / „VOLL“ |
| Gesperrt | Feld, Liste, Erklärung „Was eine Sperre bewirkt“ | SPERREN · ENTSPERREN |

**Breite Seiten** (das Panel fährt auf 1280 Breite aus; Esc → zurück zum schmalen Panel):

| Seite | Inhalt (Inventar) | Knöpfe | Overlays |
|---|---|---|---|
| Clan-Seite › Übersicht | Emblem, Werte, „Mitglieder“, Einladen-Feld, „Offene Einladungen“ | RAUSWERFEN · ZUM OFFIZIER/MITGLIED · LEITUNG GEBEN · ZURÜCKZIEHEN · BEARBEITEN · RANGLISTE (wie CLAN-RANGLISTE) · CLAN AUFLÖSEN · CLAN VERLASSEN · KASSE UND STUFE · CLAN-KRIEGE | „Clan gründen/bearbeiten“: NAME, KÜRZEL, BESCHREIBUNG, EMBLEM-Editor, VORSCHAU, GRÜNDEN · Preis bzw. SPEICHERN, ABBRECHEN |
| Clan-Seite › Kasse und Stufe | Titel „[TAG] Name“; „STUFE n“ mit Balken; „KASSE“: Betrag; Mitglied + Betrag; Chips „BANNER“; Liste „KASSENBUCH“ | EINZAHLEN · AUSZAHLEN | – |
| Clan-Seite › Clan-Kriege | Liste „KRIEGE“; „HERAUSFORDERN“: Gegner-Kürzel, Start in Minuten, Teamgröße, Aufstellung; Chips „Spiel 1–3: Modus“ | BEITRETEN · ZUSCHAUEN (→ SPIELEN › Zuschauen, vorgefiltert → Live im ReplayViewer, verdrahtet wie bei Turniere; in B/A „Nur in der Plaza“ mit ZUR PLAZA, **NEU**) · ANNEHMEN · ABLEHNEN · ABSAGEN · HERAUSFORDERN | – |
| Post-Seite | Chips Eingang / Ausgang, Liste mit „Geschenk“, Blättern | NEUE NACHRICHT | Lesen: „GESCHENK“, SCHLIESSEN, LÖSCHEN, ANTWORTEN · „Neue Nachricht“: AN, BETREFF, TEXT, GESCHENK (AUS DEM INVENTAR / AUS DEM LADEN / OHNE), SENDEN, ABBRECHEN · „Geschenk aus dem Inventar“ mit ZURÜCK |

Für alle Sozial-Ansichten gilt der gemeinsame Bestätigungsdialog (z. B. „Clan auflösen?“, „Nachricht löschen?“, „Leitung übergeben?“) mit OK bzw. Aktion und ABBRECHEN.

**TEAM-Seite** (**NEU** als Vollbild-Seite; Staff). Zugang: in P über das rote TEAM-Schild, in A und (**NEU**) B über TEAM im kleinen Menü, dazu KONTO-AKTE ÖFFNEN in den Spieler-Aktionen (**NEU**, 3a.5). Chat-Befehle öffnen den Baukasten wie heute ohne Modus-Sperre: in P, B und A die TEAM-Seite direkt beim jeweiligen Menü (in B und A als Einzelseite `page.team` ohne Hub-Leisten, Ebene 40), **im Match** den Baukasten als eigenes Modal (Ebene 50, wie heute), jeweils mit dem Argument `[name]` (z. B. `/spieler [name]`, `/replays [name]`). Schild und Menü-Eintrag gibt es im Match nicht (wie heute „nicht im Match“). Die Seite hat eine linke Liste der Rollen-Menüs und wird vom Baukasten (`ServerMenuPanel`) gerendert; es erscheinen nur die Menüs, die die Rolle darf.

| Menü | Chat-Befehl | Rollen | Inhalt (Inventar) |
|---|---|---|---|
| Moderation | /meldungen | Moderator, Admin | Filter Offen / Erledigt / Abgewiesen / Alle, Zeilen je Meldung, „Zurück“ / „Weiter“; Detail „Meldung“ mit Ziel, Grund, Details, Gemeldet von, Status, Feld „Notiz“; Abweisen, Erledigen, Map ausblenden, Map sperren, Map freigeben, Kommentar ausblenden; „Zurück zur Liste“ |
| Spieler | /spieler [name] | Moderator, Admin | Suche (Feld Name, „Suchen“, Trefferzeilen); Detail: Name, Rang, Status, Aufenthalt, Grund, Auswahl Sperre und Stumm; Sperren, Stummschalten, Kicken, Sperre aufheben, Stumm aufheben; beim eigenen Konto und bei geschützten Staff-Konten nur ein Hinweis; „Zurück zur Suche“ |
| Replays | /replays [name] | Moderator, Admin | Feld „Spieler oder Replay-ID“, „Suchen“; Zeilen „Map (Modus)“ mit Dauer und Alter; Klick öffnet die Replay-Ansicht |
| Bühne | /buehne | Moderator, Admin (Events nur Admin) | Info Bühne, Event-Bonus; „Bühne stummschalten“ / „freigeben“; „Ankündigungen“ (Zeilen mit „Beenden“; Titel, Text, Art, Dauer, Banner; „Ankündigen“); „Events“ (Name, Beschreibung, Start, Dauer, XP-Faktor, Brix-Faktor; „Event planen“); „Map der Woche“ (Aktuell, Map, Für; „Festlegen“, „Wieder automatisch“); „Event-Hosts“ (Konto, Für; „Freischalten“ / „Entziehen“); „Auf die Bühne holen“ |
| Entwickler | /entwickler, /asset-karte | Entwickler, Admin | „Inhalte, Instanzen und Werkzeuge“: Inhaltsversion, Waffen-Version, Overlay, Instanzen, Asset-Karte; „Asset-Karte betreten“, „Asset-Aufnahmen“, „Inhalte neu laden“ |
| Verwaltung | /rolle | Admin | „Rolle setzen“ (Konto, Rolle player / moderator / developer / admin / owner (**NEU**, admin und owner nur durch OWNER), Grund); „XP setzen“ (Konto, XP gesamt, Grund) |

Der Renderer bekommt neue Skins für alle 8 Element-Arten: Heading, Text, Info (Label/Wert), Row (klickbare Karte), Button (Normal / Primary / Danger / Muted, gruppierbar), Field, Select (Stepper), Separator. Dazu kommen die Meldungszeile, die Bestätigung „Bist du sicher?“ (JA, AUSFÜHREN / ABBRECHEN, Ebene 50) und die Effekte Wechsel, Client-Werkzeug (Asset-Aufnahmen), Inhalte neu laden, Bühne aktualisieren und Replay ansehen. Das alte SCHLIESSEN ist Esc bzw. Gamepad-B.

**Ausbau (NEU, Kapitel 3a):** Die Menüs dieser Tabelle bleiben mit allen Inhalten und liegen in Kategorien: Moderation (Meldungen, Spieler, Replays, **NEU** Chat-Live, Sanktions-Verlauf) · **NEU** Spielerverwaltung (Konto-Akte) · **NEU** Wirtschaft · Live-Betrieb (Bühne, **NEU** Instanzen & Server, Wartung planen, Feature-Schalter) · Entwicklung (Entwickler, **NEU** Debug-Overlay, Client-Logs) · Verwaltung (Rollen & Rechte, **NEU** Staff-Liste, Audit-Log, Sicherheit, Freigaben). Dazu kommen ein roter Staff-Kopf mit eigenem Rollen-Badge, die Suche, die Rechte-Matrix, Sicherheitsregeln und 12 neue Element-Arten.

### 3.10 Einstellungen, System-Screens, HUD, Match, Popups

**Einstellungen** (Vollbild, Ebene 44; aus dem System-Dropdown oder dem kleinen Esc-Menü; SCHLIESSEN führt dorthin zurück, woher man kam; HUD und Einführung-Karte bleiben ausgeblendet, solange die Einstellungen offen sind):

| Teil | Inhalt |
|---|---|
| Kategorie-Reiter oben (LB/RB) (**NEU**, alt Seitenleiste links) | Grafik · Sound · Steuerung · Controller · Sprachchat · Allgemein · **NEU** Barrierefreiheit |
| Mitte | Zeilen mit Titel; Abschnitte wie heute |
| rechts | Beschreibungs-Panel (**NEU**): Beschreibung der fokussierten Zeile, bei Grafik und UI-Größe mit Vorschaubild |
| Fußleiste | ZURÜCKSETZEN · **NEU** ÜBERNEHMEN/SCHLIESSEN (ein Knopf: ÜBERNEHMEN, solange Änderungen offen sind, sonst SCHLIESSEN). ZUR PLAZA und SPIEL BEENDEN stehen jetzt im kleinen Esc-Menü bzw. System-Dropdown (**NEU**). |
| Bestätigung | „Anzeige beibehalten?“ mit 15-s-Countdown: BEIBEHALTEN / ZURÜCK (n) |

| Kategorie | Inhalt (Inventar) |
|---|---|
| Grafik | Anzeige: Anzeigemodus (Fenster / Vollbild / Randlos), Auflösung (Automatisch und Liste), VSync, Bildrate begrenzen, Bildrate im Hintergrund · Qualität: Qualitätsstufe (Niedrig / Mittel / Hoch / Ultra / Benutzerdefiniert), Schatten (Aus / Niedrig / Hoch), Schattendistanz (m), Kantenglättung (Aus / FXAA / SMAA / MSAA 4x), Texturqualität, Texturfilterung (Aus–16x), Umgebungsverdeckung, Sichtweite, Render-Skalierung (%) · Bild: Nachbearbeitung, Bloom, Bewegungsunschärfe, Wettereffekte reduzieren, Helligkeit (%), Sichtfeld (°) |
| Sound | Lautstärke (%): Gesamtlautstärke, Effekte, Oberfläche, Umgebung, Musik, Sprachchat · Wiedergabe: Stumm im Hintergrund, Ausgabegerät (Systemstandard und Geräte) |
| Steuerung | Maus und Verhalten: Empfindlichkeit horizontal, vertikal, beim Zielen; Y-Achse umkehren; Sprinten (Halten / Umschalten) · Tastenbelegung (Haupt- und Zweittaste je Aktion, Esc fest), Tabelle unverändert |
| Controller | Sticks: Info, Empfindlichkeit, Y-Achse umkehren, Totzone, Zielhilfe · Belegung: Info „Neu belegen“, Gruppen wie bei der Tastatur |
| Sprachchat | Sprechen: Sprachchat (Aus / Push-to-Talk / Sprachaktivierung), Info „Datenschutz“ · Tasten: Push-to-Talk, Team-Funk, Party-Funk · Mikrofon: Eingabegerät, Mikrofon-Lautstärke, Aktivierungsschwelle, Eingangspegel, Rauschsperre, Rauschunterdrückung (+ Stärke), Mikrofon testen, Zustand · Wiedergabe: Sprach-Lautstärke, Sprecher anzeigen · Spieler: je Spieler Lautstärke und STUMM / AUFHEBEN, „In Hörweite, n m …“; ohne Spieler „Niemand sonst hier“ |
| Allgemein | Sprache: Automatisch (System) und Sprachen, „(Beta)“ · Anzeigen im Spiel: Namensschilder, Bildrate anzeigen, Ping anzeigen, **NEU** UI-Größe (Klein 85 % / Mittel 100 % / Groß 120 %) · Party folgen; Chat-Schriftgröße (pt); Kamera beim Betreten (Automatisch / 1. Person / 3. Person) · Hilfe: Support ÖFFNEN, Fehler melden MELDEN |
| Barrierefreiheit (**NEU**) | Farbsehen: Normal, Rot-Grün (Protan), Rot-Grün (Deutan), Blau-Gelb (Tritan) (verschoben aus Grafik › Barrierefreiheit) · **NEU** Animationen reduzieren (an/aus) · **NEU** UI-Größe (dieselbe Einstellung wie unter Allgemein) |

**Hilfe und Support** (`SupportPanel`, Ebene 50; Schalter; in P über das System-Dropdown, in B und M über das kleine Menü, überall über Einstellungen › Allgemein › Support ÖFFNEN):

| Teil | Inhalt (Inventar) |
|---|---|
| links | „MEINE TICKETS“, NEUES TICKET, FEHLER MELDEN |
| Formular | Kategorie-Chips (Fehler im Spiel, Konto und Anmeldung, Spieler melden, Shop und Spielwährung, Vorschlag, Sonstiges), Betreff, Text, Chip „Screenshot anhängen“ (**NEU**: nimmt das letzte Spielbild ohne Menü), SENDEN |
| Ticket-Ansicht | Nachrichten (Support/System/Du), Antwortfeld, ANTWORTEN, TICKET SCHLIESSEN; Punkt „neue Antwort“ am Ticket |

**Kontext-Popups** (überall, auch im Match):

| Popup (Ebene) | Inhalt (Inventar) |
|---|---|
| Spieler-Aktionen (53) | Titel = Name, Status „Spricht gerade.“ / „Hier.“ / „Stumm geschaltet – …“; „LAUTSTÄRKE“: Regler, STUMM / AUFHEBEN; „MELDEN“: SPIELER, CHAT, SPRACHCHAT; „BAUPLATZ“ (Inhaber): BAURECHT GEBEN/NEHMEN, RAUSWERFEN; „RAUM“ (Raumleiter): ENTFERNEN; **NEU** „TEAM“ (nur Staff mit Leserecht): KONTO-AKTE ÖFFNEN (3a.5); PROFIL, SCHLIESSEN; grüner Sprecher-Punkt in der Zeile. Aufrufer wie heute: Tab-Liste (früher Spielerliste und Punktestand), Warteraum, Ergebnis, Bauplatz-Mitbauer, Replay-Liste (Live). |
| Melden (52) | „X melden“, „Die Moderation sieht sich die Meldung an …“; „WAS MELDEST DU?“ (Spieler / Chat / Sprachchat); „GRUND“ (Schummeln, Belästigung, Anstößiger Name, Spam, Sprachchat-Missbrauch, Sonstiges); „DETAILS (FREIWILLIG)“, bei Chat mit den letzten Zeilen vorbefüllt; MELDEN, ABBRECHEN |
| Profil (51) | 3.8 |
| Dialoge (50) | gemeinsamer Bestätigungsdialog (OK bzw. Aktion / ABBRECHEN), „Bist du sicher?“, „Anzeige beibehalten?“ und alle Unterdialoge der Seiten |

**System-Screen** (Ebene 100): Ladebildschirm, Anmeldung, Fehler wie heute: Logo „BRIXEL“, Zeile „Bauen. Treffen. Spielen.“, Status, Detail, Fortschrittsbalken, „Version x   Protokoll y“. Statuszeilen „Anmeldung wird geprüft“ · „Verbinde mit dem Server“ · „Welt wird geladen“ · „Charakter wird erstellt“ · „Instanz wird gewechselt“ · „Verbindung verloren – verbinde neu …“. Fehlerkarte mit Titel „Konto gesperrt“ · „Vom Server entfernt“ · „Wartung“ · „Verbindung fehlgeschlagen“ · „Anmeldung nicht möglich“ und den Details aus `GameClient.Fail`, z. B. „Bitte starte Brixel über den Launcher.“, „Die Spielinhalte brauchen eine neuere Version …“, „Alle Hubs sind gerade voll …“, „Der Server … ist nicht erreichbar.“. Knöpfe ERNEUT VERSUCHEN (nicht bei Ticket-, Sitzungs-, Versions- oder Sperr-Fehlern) und BEENDEN.

**HUD-Familie** (Ebene 9–13; Details in Kapitel 13 und 14):

| Teil | Klasse | Modi | Neu gestaltet als |
|---|---|---|---|
| Basis-HUD: Info-Leiste „\<Map\> \| n Spieler \| \<Name\>“, Post-Zähler „99+“ (nur bei ungelesener Post), FPS/Ping „n FPS   n ms Ping“, einfaches Fadenkreuz (ohne Kampf-HUD, nicht in der Frontkamera), Hinweis unten Mitte, Chat (9 sichtbare Zeilen, Verlauf 200, Kennzeichen vor dem Namen, Farben für Funk „[Funk] X: …“ und Flüstern, Eingabefeld „Nachricht schreiben“ mit Modal `chat`, Enter öffnet und sendet, Mausrad und Bild auf/ab blättern) · VoiceHud: Mikrofon-Pille „Aus“ / „Kein Mikrofon“ / „Sprichst“ / „Team-Funk“ / „Party-Funk“ / „Stumm“ / „Hört zu“, Modus „Nähe“ oder „Map-weit“, Sprecherliste „Name (Bühne)“ / „(Funk)“ / „+N weitere“ · MissionsWidget rechts (nur P, nicht klickbar): „TAGESMISSIONEN“, „neu in …“, 3 Zeilen mit Balken, Wert oder „erledigt“ | HudController | alle | HUD; Toast (Standard 3,5 s) wandert in die Toast-Ebene 70 (**NEU**) |
| Brick-Leiste | HudController | B, M-Bauphase | Bau-HUD (Kapitel 14) |
| Kampf-HUD inkl. Zielfernrohr, Blendung, Todesbildschirm, Schießstand-Karte | CombatHud | M, Schießstand | Kapitel 13 |
| Match-Kopf | MatchHud | M | Kapitel 13 |
| Ziele | ObjectiveHud | M | Kapitel 13 |
| Radar | RadarHud | M | Kapitel 13 |
| Überleben | SurvivalHud | M (Verteidigung, Zombie) | Kapitel 13 |
| Party-Liste rechts „PARTY n / m“ | PartyHud | P, B, A (nicht im Match) | HUD-Liste; die Karten wandern in die Benachrichtigungen |
| Einführung-Karte | TutorialHud | P (nicht im Match, nicht bei offenen Einstellungen) | HUD-Karte; führt per Coachmark (**NEU**, Ebene 41 über dem Hub) durch die Hub-Reiter |
| Such-Pille (**NEU** im HUD) | – | P, solange gesucht wird und der Hub zu ist | kleine Pille oben Mitte mit Timer; Esc öffnet den Hub, dort steht ABBRECHEN in der Top-Leiste |

**Match-Screens:**

| Screen | Klasse | Inhalt | Neu |
|---|---|---|---|
| Warteraum | WaitingRoomPanel | Titel = Raum (mit Schloss), Untertitel mit Modus, Map, Kanal und Regeln, Status-Abzeichen („Start in n s“, „Warte auf Spieler (n/m)“, „Bereit: …“); Team-Spalten mit Krone, Kennzeichen, „(Du)“; ENTFERNEN, „•••“, LEITUNG ÜBERGEBEN; Box „LETZTE RUNDE“; VERLASSEN · TEAM WECHSELN · MATCH STARTEN / „WARTET AUF MASTER“ · UMSEHEN · RAUM ÄNDERN; Unterdialoge „RAUM ÄNDERN“ (Zeilen mit < / > für Modus, Map, Ziel, Zeit, Spieler, Waffen, Map-Rotation; ÜBERNEHMEN / ABBRECHEN) und „LEITUNG ÜBERGEBEN“ (ÜBERGEBEN / ABBRECHEN) | Look; Tab-Variante (Kapitel 5) |
| Tab-Liste / Punktestand | ScoreboardPanel + PlayerListPanel | Kapitel 5 | zusammengelegt |
| Funkrad | RadioMenu | Mitte „FUNK“ / „an dein Team“ bzw. „nur in Team-Modi“; 8 Sprüche mit Ziffer 1–8: Folgt mir! · Brauche Hilfe! · Gegner gesichtet! · Deckt mich! · Ziel angreifen! · Ziel verteidigen! · Verstanden. · Negativ.; schließt mit Esc, Z oder Klick auf den Schatten | Radial `hud_radial_segment` |
| Ergebnis-Sequenz | ResultsSequence | Titelkarte SIEG / NIEDERLAGE / UNENTSCHIEDEN / „n. PLATZ“ / INFIZIERT / ÜBERLEBT / VERTEIDIGUNG; Zähler „+n XP“, „+n Brix“, Bonuszeilen; Rangbalken „RANG n“ mit Funken; „Klicken für die Tabelle“; Klick, Leertaste oder Esc überspringen | Timeline 15.8 |
| Ergebnis | ResultsPanel | „Sieg!“ / „Niederlage“ / „Unentschieden“ / „Ergebnis“, Countdown „Zurück zur Plaza in n s“ / „Warteraum …“; Tabelle SPIELER / PUNKTE / K / T / A / ZIEL oder K/T / ZEIT mit „•••“; „DEINE BELOHNUNG“ (Rang, „RANG n!“, XP-Balken, Brix, Bonus, Münzen, Mastery-Extras); „DIESE MAP“: DAUMEN HOCH / DAUMEN RUNTER, Kommentar + SENDEN; „Spielzug der Runde“: ANSEHEN, VIDEO SPEICHERN; ZUR PLAZA, SCHLIESSEN | **NEU** „In Highlights“ beim Spielzug der Runde |
| ReplayViewer | ReplayViewer | Kapitel 19 | für alle Spieler (**NEU**) |
| Foto-Modus | PhotoMode | Infozeile „Foto-Modus · n / 40 m · …“; Filter-Chips Normal, Warm, Kalt, Schwarzweiß, Sepia, Kräftig, Verträumt; Chip „Tiefenschärfe“; Regler Fokus, Blende, Sichtfeld, Rollen; FOTO, ALS VORSCHAUBILD (Inhaber auf dem Bauplatz), BEENDEN; Toasts „Foto gespeichert.“, „Das Bild ist zu groß für ein Vorschaubild.“ | Zugang P-Taste, System-Dropdown (P), kleines Menü (B); im Match nur als Geist/Zuschauer; im Replay immer. **NEU**: blendet die Ebene 70 (Karten, fremde Toasts, Wartungsband) aus und zeigt nur die eigenen Toasts; FOTO nimmt das Bild ohne UI auf. |

**Popups & Benachrichtigungen:**

| Element | Ebene | Inhalt | Regel |
|---|---|---|---|
| Popup-Warteschlange (**NEU**) | 58 (**NEU**: über den Einstellungen; alt 47 < 50) | Reihenfolge: „Was ist neu in \<Version\>“ („Die wichtigsten Änderungen dieser Version.“, LOS GEHT'S; schließt auch mit Esc) → „Tägliche Belohnung“ (Serien-Zeile, 7 Kacheln „TAG n“ / „TAG n · ABGEHOLT“, Statuszeile, ABHOLEN → „ABGEHOLT“, SCHLIESSEN; Plaza, Schalter) → Einführung-Begrüßung („Willkommen in Brixel!“) | Immer nur ein Popup. Die Schlange wartet, solange Einstellungen, ein Dialog, Profil/Melden/Spieler-Aktionen, Foto-Modus, ein Match oder der Ladebildschirm offen sind. |
| Einführung-Dialog | 58 | Titel „Willkommen in Brixel!“ / „Einführung“ / „Einführung abgeschlossen“ / „Einführung übersprungen“; LOS GEHT'S / WEITER / NEU STARTEN, ÜBERSPRINGEN, SCHLIESSEN; Abschluss-Toast „Einführung geschafft! +x Brix“ | P; Aufruf auch über die LOBBY-Karte |
| Belohnungs-Popups | 58 | Rang-Aufstieg außerhalb der Ergebnis-Sequenz, Werkstatt-Ergebnis, Glücksbrett-Gewinn (dort als Overlay der Seite) | Motion 15.8 |
| Benachrichtigungskarten oben rechts | 70 | Party-Einladung (`PartyHudTop`): „X lädt dich in eine Party ein“, „noch n s · n Mitglieder“, ANNEHMEN / ABLEHNEN, Timer-Ring · Folgen-Karte: „Folge X …“ mit Balken, „Ziel · in n s“, ABBRECHEN (Esc bricht ebenfalls ab) · Bühnen-Banner: „\<ART\> · BÜHNE“, Titel, Text, SCHLIESSEN (wartet während einer laufenden Match-Runde wie heute) · Support-Antwort (**NEU** als Karte mit ÖFFNEN) | P, B, A: oben rechts (im Hub unter der Top-Leiste), höchstens 3 gestapelt, die neueste oben. M: rechts **unter dem Killfeed** (ab y = 360, höchstens 2), damit der Killfeed frei bleibt (**NEU**). |
| Toasts | 70 | Standard 3,5 s; Ablehnung (Bau-Ablehnungen) mit rotem Rand + Shake | über allen Menüs (**NEU**) |
| Wartungsband | 70 | oben Mitte „Wartung in m:ss“ und Meldung (Standard „Dein Fortschritt wird gespeichert.“), letzte 15 Min. vor Wartung | über allen Menüs (**NEU**); im Match unter dem Match-Kopf |
| Sanktionen | 70 / 100 | „Du bist stummgeschaltet (…)“, „Dein Konto ist (dauerhaft) gesperrt …“, „Du wurdest vom Server entfernt.“ als Toast und Chat-Systemzeile; Sperre, Kick und Wartungs-Kick als Fehlerkarte im System-Screen („Wartung“) | Eintrag auch in der Glocke (**NEU**) |
| Glocke-Verlauf (**NEU**) | 40 | Dropdown unter der Glocke: die letzten 30 Toasts, Karten und Systemzeilen mit Zeit; Klick springt zum Ziel | nur im Hub |

### 3.11 Zähler & Badges
Alle Zähler des alten Esc-Menüs und der Sozial-Reiter-Chips bleiben erhalten, nur an neuen Orten.

| Zähler (Inventar) | Neuer Ort | Darstellung |
|---|---|---|
| „Freunde und Gruppen · n online · n neu“ | Sozial-Knopf der Top-Leiste („n online“ als Text, „n neu“ als Badge); SOZIAL im kleinen Menü (B, A) zeigt „n online · n neu“ | `badge_counter` rot, Zahl bis „99+“ |
| Sozial-Reiter-Chips (mit Zähler): Freunde · Party · Clan · Post · Gesperrt · Plazas | Reiter-Chips im Sozial-Panel, gleiche Zähler | Badge am Chip |
| „Post · n ungelesen“ | Post-Knopf der Top-Leiste; Reiter Post im Sozial-Panel; HUD-Post-Zähler bleibt | Umschlag mit Badge bis „99+“ |
| „Tägliche Belohnung (· abholbar)“ | Truhe in der LOBBY und Badge am Reiter LOBBY | Text-Etikett „abholbar“, Truhe wackelt sanft |
| „Hilfe und Support · neue Antwort“ | Punkt am System-Knopf und Eintrag „Hilfe und Support · neue Antwort“ im Dropdown (P); HILFE UND SUPPORT im kleinen Menü mit Punkt (B, M); im Fenster Hilfe und Support am Ticket; Glocke | Punkt-Badge (8 px) |
| „Gewertet · Suche läuft“ | Such-Pille (Top-Leiste bzw. HUD), Badge „Suche läuft“ an SPIELEN und am Unterreiter Gewertet | pulsierende Pille |
| Rollen-Menüs (roter Marker) | TEAM-Schild rot | Schild statt Marker |
| **NEU** TEAM-Zähler | TEAM-Schild und linke TEAM-Liste: offene Meldungen (MOD, ADMIN, OWNER), wartende Freigaben (nur OWNER; auch im Staff-Kopf) | `badge_counter` |
| „(bald)“ | Schloss + Etikett „BALD“ (`badge_tag`) an Reiter oder Karte, wo eine Funktion noch nicht freigeschaltet ist | ausgegraut, nicht fokussierbar |
| **NEU** Glocke | Anzahl ungelesener Einträge | Badge |
| Weitere Seiten-Zähler | „Ankündigungen (n)“, „Events (n)“, „KOMMENTARE (n)“, „Plazas mit Bekannten (n)“, „RÜCKGÄNGIG (n)“, „WIEDERHOLEN (n)“ | bleiben im Text |

**Regeln:** Der Reiter-Badge zeigt die Summe seiner Unterreiter-Zahlen. Text-Badges („abholbar“, „Suche läuft“) gewinnen gegen Zahlen. Zahlen über 99 werden „99+“. Ein Badge verschwindet erst, wenn der Inhalt gesehen wurde (Seite geöffnet), nicht schon beim Hover.

### 3.12 Esc-Zurück-Kette (Esc bzw. Gamepad-B)
Esc und Gamepad-B gehen immer genau eine Ebene zurück; Esc ist fest belegt (Steuerung: „Esc fest“). Gamepad-Start wirkt wie Esc (wie heute). Grundregel: Ein offener Unterdialog schließt zuerst, dann die Seite, dann das Menü. Geprüft wird von oben nach unten, der erste Treffer gewinnt:

| # | Zustand (Ebene) | Esc bzw. Gamepad-B bewirkt |
|---|---|---|
| 1 | Texteingabe fokussiert (Chat „Nachricht schreiben“, Suchfelder) | Chat-Eingabe schließt wie heute; in anderen Feldern: Fokus verlassen |
| 2 | Foto-Modus (60) | schließt (wie heute auch P oder BEENDEN) |
| 3 | Popup (58) | schließt das Popup; die Schlange macht weiter |
| 4 | Spieler-Aktionen (53) → Melden (52) → Profil (51) → Dialog, Hilfe und Support oder Baukasten-Modal im Match (50) | schließt das oberste |
| 5 | ReplayViewer (46) | schließt, zurück zum Einstieg |
| 6 | Ergebnis-Sequenz (45) | überspringt (wie heute) |
| 7 | Einstellungen (44) | „Anzeige beibehalten?“ offen → ZURÜCK (n) (**NEU**: sichere Wahl); sonst wie SCHLIESSEN → zurück zum Ursprung |
| 8 | Ergebnis (43) | wie SCHLIESSEN |
| 9 | Sozial-Panel (42) | Overlay (z. B. „Neue Nachricht“) → breite Seite → schmales Panel → Panel zu |
| 10 | Hub (40) | Dropdown → zu; Unterdialog → zu; Detailansicht (z. B. Map-Galerie-Detail, „Raum erstellen“, Clan-Unterseite, Neuigkeiten) → Liste; sonst Hub zu („Zurück ins Spiel“) |
| 11 | kleines Esc-Menü / Bauplatz-Fenster / TEAM-Einzelseite (40) | Unterdialog → Seite → Bauplatz-Fenster → kleines Menü → zu |
| 12 | Spiel-Overlays (30–34) | Palette, Bauvorlagen-Werkzeug, Funkrad schließen · Tab-Liste angeheftet → lösen · Warteraum wie heute |
| 13 | Folgen-Karte aktiv, sonst nichts offen | bricht das Folgen ab (wie heute „Esc bricht ebenfalls ab“); es öffnet sich **kein** Menü |
| 14 | **NEU** Freie Kamera (Staff, 3a.2.7) aktiv | beendet die freie Kamera; es öffnet sich **kein** Menü |
| 15 | nichts offen | P: Hub öffnen (LOBBY) · B, A, M: kleines Esc-Menü öffnen |

### 3.13 Eingabe-Belegung im Menü

Gamepad-Tasten heißen in diesem Dokument immer „Gamepad-A/B/X/Y“, weil Tastatur-B Push-to-Talk ist (Tastenbelegung Sprachchat).

| Aktion | Tastatur / Maus | Gamepad | Wo |
|---|---|---|---|
| Hub bzw. kleines Menü öffnen/schließen | Esc | Start (wirkt wie Esc, wie heute) | überall außer Ladebildschirm |
| Zurück | Esc, Klick auf den Hinweis „Esc Zurück“ | Gamepad-B | Kette 3.12 |
| Auswählen | Enter, Linksklick | Gamepad-A | überall |
| Reiter wechseln | Q / E (**NEU**) | LB / RB | Hub, Einstellungen-Kategorien; im Sozial-Panel die Reiter-Chips |
| Unterreiter | 1–9 (**NEU**) | LT / RT | Hub |
| Sozial-Panel | F (**NEU**) | Gamepad-Y (**NEU**) | Hub; im kleinen Menü (B, A) öffnet Gamepad-Y den Eintrag SOZIAL |
| Kontext („•••“, Details, Vorschau) | Rechtsklick | Gamepad-X (**NEU**) | Listen, Karten |
| System-Dropdown | Klick auf das Zahnrad | View (**NEU**) | Hub |
| Fokus bewegen | Maus, Pfeiltasten (**NEU**) | Steuerkreuz, linker Stick | alle Screens (PadNavigator) |
| Scrollen | Mausrad, Bild auf/ab | rechter Stick (**NEU**) | Listen, Seiten |
| Tab-Liste | Tab halten, Rechtsklick heftet an | Taste „Spielerliste und Punktestand“ halten, Gamepad-A heftet an (**NEU**) | Kapitel 5 |

- Solange ein Textfeld den Fokus hat, sind die Hub-Kürzel Q/E, 1–9 und F aus; die Tasten schreiben dann in das Feld.
- Weil Hub und kleines Menü modal sind, gibt es keinen Konflikt mit Q = Palette, E = Benutzen oder F = Fliegen/Nahkampf.
- Die Glyphen in Fußleiste und Hinweisen kommen aus der aktuellen Belegung (`UiKeybindButton`), nie fest im Text.

### 3.14 Start-Reiter, Deep-Links, Einschränkungen

**Start-Reiter und Deep-Links**

| Auslöser | Ziel |
|---|---|
| Esc / Start in P | Hub › LOBBY (Standard beim Öffnen). Innerhalb einer Sitzung merkt sich jeder Reiter seinen letzten Unterreiter. |
| Profil-Chip | KARRIERE › Profil |
| Post-Knopf, HUD-Post-Zähler | Sozial-Panel › Post |
| Sozial-Knopf, F bzw. Gamepad-Y, „+“-Platz | Sozial-Panel › Freunde |
| TEAM-Schild (P), TEAM im kleinen Menü (A, **NEU** B) | TEAM-Seite |
| Chat-Befehl (/meldungen, /spieler [name], /replays [name], /buehne, /entwickler, /asset-karte, /rolle, **NEU** /akte [name]) | Baukasten beim passenden Menü mit Argument `[name]`: in P als TEAM-Seite im Hub, in B und A als TEAM-Seite (Einzelseite `page.team`), **im Match** als eigenes Modal (Ebene 50, wie heute) |
| **NEU** KONTO-AKTE ÖFFNEN (Spieler-Aktionen, Profil-Popup, Sozial-Panel; nur Staff) | TEAM › Spielerverwaltung › Konto-Akte des Spielers; Ort wie bei den Chat-Befehlen (3a.5) |
| Glocke-Eintrag, Benachrichtigungskarte | Ziel des Eintrags (z. B. Support-Antwort → Hilfe und Support, Ticket) |
| Such-Pille | SPIELEN › Gewertet bzw. Schnellspiel |
| Tagesmissionen-Widget (LOBBY) | KARRIERE › Tagesmissionen. Das HUD-Widget bleibt nicht klickbar; Weg: Esc → LOBBY bzw. KARRIERE › Tagesmissionen. |

**Einschränkungen, die bleiben**

| Regel | Gilt für |
|---|---|
| Schalter | Tägliche Belohnung, Hilfe und Support, Fehler melden; **NEU** dazu Events und Glücksbrett (TEAM › Live-Betrieb › Feature-Schalter, 3a.2.4). Ist der Schalter aus, wird der Eintrag ausgeblendet (wie heute im Esc-Menü). |
| Rollen | TEAM nur mit Rolle; nur Menüs, die die Rolle darf (Tabelle 3.9, **NEU** Rechte-Matrix 3a.3); im Namensschild Rollen-Abzeichen wie heute |
| nur Inhaber / Leitung | Veröffentlichen und ALS VORSCHAUBILD (Inhaber auf dem Bauplatz); „BAUPLATZ“ in Spieler-Aktionen (Inhaber); „RAUM“ › ENTFERNEN (Raumleiter); MATCH STARTEN (Master) |
| nicht im Match | Sozial-Panel, Post, TEAM-Schild bzw. TEAM-Eintrag und TEAM-WERKZEUGE (Chat-Befehle und KONTO-AKTE ÖFFNEN gehen als Modal), Foto-Modus (außer als Geist/Zuschauer), Party-Liste |
| nur Plaza | Hub mit allen Reitern, also auch Gewertet, Turniere, Zuschauen-Liste, Einführung, Tägliche Belohnung, Meine Maps/Mitbauen (früher Bau-Portal); MissionsWidget; Bühnen-Leinwand |
| nur Bauplatz | Bauplatz-Fenster, Palette (Q), Bauvorlagen (X), ÜBERNEHMEN einer Vorlage |
| Hinweis „Nur in der Plaza“ | Weil der Hub nur in der Plaza existiert, braucht keine Hub-Seite diesen Hinweis. Er erscheint dort, wo ein Querverweis in B oder A auf eine Hub-Seite zeigt (3.14 #23): statt der Aktion der Hinweis „Nur in der Plaza“ mit Knopf ZUR PLAZA. |
| Einführung-Karte | nicht im Match und nicht bei offenen Einstellungen |
| HUD | aus, solange die Einstellungen offen sind |

**Was sich ändert (NEU, mit Begründung)**

| # | Änderung | Begründung |
|---|---|---|
| 1 | Funktionen, die nur über eine Plaza-Station gingen (Laden, Garderobe, Arena, Map-Galerie, Waffenständer, Bestenlisten, Glücksbrett, Bühne, Bau-Portal), liegen im Hub. Der Ort bleibt die Plaza. | Große Games bündeln alles im Menü; Laufwege in der Welt kosten Zeit (Fortnite, Valorant). |
| 2 | Hauptmenü nur in P; in B, A, M ein kleines Esc-Menü (Kapitel 4) | Im laufenden Spiel nur Spiel-Aktionen (Valorant, CoD) |
| 3 | MEIN PROFIL steht nicht mehr im Esc-Menü. Eigenes Profil: P über Profil-Chip/KARRIERE, B/A/M über die eigene Zeile der Tab-Liste. | Kompakte In-Game-Menüs; das Profil gehört zur Karriere (Valorant, CoD) |
| 4 | Auf der Asset-Karte (A) stehen Hilfe und Support und Fehler melden nicht im Menü; sie bleiben über EINSTELLUNGEN › Allgemein › Hilfe erreichbar (Support ÖFFNEN, Fehler melden MELDEN). | Kompaktes Menü auf einer Staff-Karte; die Funktion bleibt erreichbar. |
| 5 | TEAM steht im kleinen Menü auf A und B (nur Staff; auf B **NEU** gegenüber dem früheren Planstand, der TEAM dort weggelassen hatte), dazu **NEU** TEAM-WERKZEUGE (3a.2.7). Chat-Befehle gehen weiter überall. | Staff braucht Konto-Akte und Werkzeuge auch auf dem Bauplatz (z. B. Map sperren, Spieler holen); löst 20/O3 |
| 6 | Tab-Liste: Halten statt Umschalten auch in P, B, A; Anheften per Rechtsklick in allen Modi | Einheitliches Verhalten wie bei Punktestand-Listen in Shootern (Counter-Strike, Valorant) |
| 7 | ZUSCHAUEN direkt in der Freundes-Zeile (in P; in B/A „Nur in der Plaza“) | Zuschauen aus der Freundesliste (Fortnite) |
| 8 | Replays für alle Spieler (Kapitel 19) | User-Wunsch; Replays in der Karriere (Fortnite, Overwatch) |
| 9 | Such-Pille auch bei geschlossenem Hub (HUD, P) | Suchstatus bleibt sichtbar, während man herumläuft (Fortnite, Apex). |
| 10 | Toasts, Benachrichtigungen und Wartungsband liegen über allen Menüs (Ebene 70). | Wichtige Hinweise werden nie verdeckt. |
| 11 | Popup-Warteschlange; Glocke mit Verlauf | Keine gestapelten Popups; verpasste Hinweise lassen sich nachlesen (Fortnite, Apex). |
| 12 | Einstellungen: Reiter Barrierefreiheit (Farbsehen verschoben, dazu Animationen reduzieren und UI-Größe), Beschreibungs-Panel, Fußleiste ohne ZUR PLAZA/SPIEL BEENDEN | AAA-Einstellungen (CoD, Apex) |
| 13 | Hilfe und Support liegt über den Einstellungen (Ebene 50 > 44; alt Ord 48 < 50). Im Match öffnet HILFE UND SUPPORT ein eigenes Fenster, weil es dort keinen Hub gibt. | „Einstellungen › Allgemein › Support ÖFFNEN“ muss die Einstellungen nicht schließen. |
| 14 | Vorlagen auch in P durchsuchbar (ÜBERNEHMEN nur auf B); „Gesperrt“-Slot verlinkt LADEN › Map-Slots | kürzere Wege |
| 15 | Bestätigungen „Spiel beenden?“ und „Match verlassen?“ | Schutz vor versehentlichem Beenden; in großen Games Standard |
| 16 | Schnellspiel mit Modus- und Kanalwahl, Modus-Karte, Bereit-Status, LADEN › Empfohlen, „+“ an Kristalle | Lobby-Muster großer Games; Server-Teil offen (Kapitel 20) |
| 17 | Fremdes Profil im Match: POST und BESTENLISTEN ausgeblendet | Im Match gibt es weder Sozial noch Hub-Seiten; große Shooter verlegen soziale Funktionen in die Lobby. |
| 18 | Der Warten-Dialog von Schnellstart und Gewertet blockiert nicht mehr; die Suche läuft als Such-Pille weiter. | Man kann während der Suche weiter im Menü stöbern (Fortnite, Apex). |
| 19 | Foto-Modus blendet Ebene 70 aus (außer den eigenen Toasts); Bildschirmfotos und „Screenshot anhängen“ ohne UI | saubere Bilder |
| 20 | Popups (58) liegen über den Einstellungen (alt 47 < 50); die Popup-Warteschlange wartet, solange Einstellungen offen sind. | Popups kommen nie unter einem anderen Fenster zu liegen. |
| 21 | Bauvorlagen als rechts angedocktes Werkzeug statt Fenster | ECKEN WÄHLEN braucht freie Sicht auf die Welt. |
| 22 | Benachrichtigungskarten im Match rechts unter dem Killfeed | Der Killfeed bleibt frei. |
| 23 | Querverweise in den Hub zeigen in B und A „Nur in der Plaza“ mit ZUR PLAZA: Post „AUS DEM LADEN“, Profil „BESTENLISTEN“, Clan „CLAN-RANGLISTE“/„RANGLISTE“, ZUSCHAUEN (Freundes-Zeile, Clan-Kriege). Heute gingen diese Wege auch dort. | Den Hub gibt es nur in der Plaza (ÄNDERUNG 2); große Games bündeln Shop, Ranglisten und Zuschauen in der Lobby. |

**Umbenennungen (alt → neu, alle NEU)**

| Alt | Neu | Wo |
|---|---|---|
| „WEITER“ | ZURÜCK INS SPIEL (bzw. Hinweis „Zurück ins Spiel“) | kleines Esc-Menü, Hub-Fußleiste |
| „ZUR PLAZA“ (im Match: Match verlassen) | MATCH VERLASSEN | kleines Esc-Menü (M) |
| „Bauplatz verwalten“ (Listeneintrag) | BAUPLATZ VERWALTEN | kleines Esc-Menü (B) |
| „Freunde und Gruppen“ | SOZIAL bzw. Sozial-Panel | kleines Esc-Menü (B, A), Top-Leiste |
| „Zu Freunden wechseln“ | Sozial-Panel › Plazas | – |
| Fenster „Arena“ / Räume | SPIELEN › Server-Browser | Hub |
| Fenster „Bühne“ | LOBBY › Neuigkeiten | Hub |
| Reiter „Ausrüstung“ | SPIND › Loadout | Hub |
| „Waffenständer“ | SPIND › Testgelände | Hub |
| Fenster „Bau-Portal“ | ERSTELLEN › Meine Maps / Mitbauen | Hub |
| „Bauvorlagen“-Fenster | Bauvorlagen-Werkzeug (angedockt) | B |
| Spielerliste / Punktestand | Tab-Liste | alle Modi |

---
## 3a. TEAM-Funktionen (NEU)
Ausbau der TEAM-Seite (3.9) zu einem vollständigen Staff-Bereich: mehr Moderation, eine Konto-Akte je Spieler mit Inventar, allen Währungen und Fortschritt, dazu Wirtschaft, Live-Betrieb und Verwaltung mit Rechte-Matrix und Vier-Augen-Freigabe. Die sechs Rollen-Menüs aus dem Inventar bleiben mit allen Inhalten, Knopf-Texten und Chat-Befehlen erhalten (Tabelle 3.9) und werden nur in Kategorien einsortiert. Das Inventar-Menü „Moderation“ (/meldungen) heißt dabei **Meldungen** (**NEU**-Name), weil „Moderation“ jetzt die Kategorie ist. Alles andere in diesem Kapitel ist **NEU**. Gerendert wird weiter vom Baukasten (`ServerMenuPanel`): Der Server baut jede Seite und prüft jedes Recht, der Client zeigt nur an (3a.7).

### 3a.1 Aufbau der TEAM-Seite
```
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ Top-Leiste des Hubs (nur P)                                                                │
├────────────────────────────────────────────────────────────────────────────────────────────┤
│ TEAM  [ADMIN] Kai · Admin                     FREIGABEN 2 · UNSICHTBAR ○ · FREIE KAMERA    │  ← Staff-Kopf frame_staff_header (rot), Höhe 72
├━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┤  ← Akzentlinie staff.line, 2 px (divider_staff)
│ [Suche] Name, Konto-ID, Replay-ID, Map ┃ KONTO-AKTE                                        │
│ ZULETZT GEÖFFNET                       ┃ ┌──────────────────────────────────────────────┐  │
│   Spieler123 · Konto-Akte       5 Min. ┃ │ [12] Spieler123 [MOD] • Plaza 2 · 4F2A-91C3  │  │  ← Konto-Kopf
│   Replay 88120 · Entschärfung   1 Std. ┃ │ STUMM 2 STD.  TELEPORTIEREN ZU · HOLEN · …   │  │
│ MODERATION                             ┃ └──────────────────────────────────────────────┘  │
│   Meldungen                         12 ┃ Übersicht · Währungen · Inventar · … · Protokoll  │  ← Tabs
│   Spieler                              ┃ ┌──────────────────────────────────────────────┐  │
│   Chat-Live                            ┃ │ Inhalt des Reiters (vom Server gebaut)       │  │
│   Replays                              ┃ │                                              │  │
│   Sanktions-Verlauf                    ┃ │                                              │  │
│ SPIELERVERWALTUNG                      ┃ │                                              │  │
│ ▌ Konto-Akte                           ┃ │                                              │  │
│ WIRTSCHAFT · LIVE-BETRIEB              ┃ │                                              │  │
│ ENTWICKLUNG · VERWALTUNG               ┃ └──────────────────────────────────────────────┘  │
├────────────────────────────────────────────────────────────────────────────────────────────┤
│ Statuszeile                               [Esc] Zurück · [Enter] Auswählen · [1–0] Reiter  │  ← Fußleiste des Hubs
└────────────────────────────────────────────────────────────────────────────────────────────┘
  linke Liste 384 breit (sidebar_panel), Inhalt im 12-Spalten-Raster des Hubs
```

| Zone | Inhalt | Verhalten |
|---|---|---|
| Staff-Kopf (`frame_staff_header`, Höhe 72) | „TEAM“, eigenes Rollen-Badge (`role_owner` / `role_admin` / `role_dev` / `role_mod`), eigener Name und Rolle. Rechts nur für OWNER „FREIGABEN n“ (→ Verwaltung › Freigaben), dazu die Werkzeuge UNSICHTBAR (Schalter) und FREIE KAMERA, soweit die Rolle sie darf (3a.2.7). | Roter Kopf = Staff-Bereich. Er steht auf jeder Staff-Ansicht: TEAM-Seite (P), TEAM-Einzelseite (B, A) und Baukasten-Modal im Match. |
| Akzentlinie (`divider_staff`, `staff.line`, 2 px) | unter dem Staff-Kopf über die volle Breite, am linken Rand des Inhalts, oben an jedem Staff-Dialog und am Block „TEAM“ der Spieler-Aktionen | macht jede Staff-Fläche erkennbar, auch Dialoge über dem Spiel |
| Suchfeld (`input_search`, oben in der linken Liste) | Platzhalter „Spieler, Konto-ID, Replay-ID, Map …“. Treffer gruppiert: SPIELER (Rang-Abzeichen, Name, Rollen-Badge, online/offline) · REPLAYS („Map (Modus)“, Dauer, Alter) · MAPS (Vorschaubild, Name, Inhaber) | sucht 300 ms nach der letzten Eingabe, ab 2 Zeichen; Konto-ID und Replay-ID werden am Muster erkannt und öffnen das Ziel direkt. Spieler → Konto-Akte, Replay → ReplayViewer, Map → Konto-Akte des Inhabers › Maps & Bauplatz mit markierter Map. Treffer ohne Recht erscheinen nicht. Tastatur: Strg+F bzw. „/“ fokussiert das Feld. |
| Zuletzt geöffnet | die letzten 8 Ziele (Konto-Akten, Replays, Maps, Menüs) mit Symbol und Zeit, je Staff-Konto auf dem Server gemerkt | Klick öffnet das Ziel; leer: „Noch nichts geöffnet.“ |
| Linke Liste (`sidebar_panel`, Breite 384) | Kategorien als Abschnittsköpfe (`label`, `gold.light`), darunter ihre Menüs als Seitenleisten-Einträge (Icon + Text + Zähler) | Es erscheinen nur Menüs, die die Rolle sieht (3a.3); eine Kategorie ohne sichtbares Menü fehlt ganz. Kategorien lassen sich einklappen (je Staff-Konto gemerkt), die Kategorie des offenen Menüs bleibt offen. Zähler: Meldungen „offen“, Freigaben „wartend“ (nur OWNER). Kompakt (10.3): Icon-Leiste 72 px, Suche als Lupen-Knopf. |
| Inhalt | Seite des gewählten Menüs, vom Server gebaut: Titel, Untertitel, Meldungszeile, Elemente (3a.6) | scrollt; Primäraktion unten rechts; Nur-Lesen-Seiten tragen das Etikett „NUR LESEN“ |
| Fußleiste | Statuszeile und Tastenhinweise des Hubs, in der Konto-Akte zusätzlich „1–0 Reiter“ | wie 3.2 |

**Orte:** P = Hub-Seite `hub.team` (Top-Leiste bleibt, keine Unterreiter-Leiste) · B, A = Einzelseite `page.team` (Ebene 40) · M = Baukasten-Modal (Ebene 50) mit Staff-Kopf und Akzentlinie, aber ohne linke Liste; es zeigt nur das aufgerufene Menü.

**Zurück:** Esc bzw. Gamepad-B schließt Dialog → Detail (z. B. Konto-Akte, Meldung) → Liste bzw. Suche des Menüs → TEAM-Seite (P: zurück zum Hub, B/A: kleines Esc-Menü, M: zurück ins Spiel). Gamepad-Fokusgruppen: Staff-Kopf, linke Liste, Inhalt (18.8).

### 3a.2 Kategorien und Menüs

| Kategorie | Menü | Chat-Befehl | Rollen (Details 3a.3) | Status |
|---|---|---|---|---|
| Moderation | Meldungen (Inventar „Moderation“) | /meldungen | MOD, ADMIN, OWNER | bleibt, **NEU**-Name |
| | Spieler | /spieler [name] | MOD, ADMIN, OWNER | bleibt, **NEU** KONTO-AKTE ÖFFNEN |
| | Chat-Live | – | MOD, ADMIN, OWNER | **NEU** |
| | Replays | /replays [name] | MOD, ADMIN, OWNER | bleibt |
| | Sanktions-Verlauf | – | MOD, ADMIN, OWNER | **NEU** |
| Spielerverwaltung | Konto-Akte | /akte [name] (**NEU**) | ADMIN, OWNER; MOD Lesen | **NEU** |
| Wirtschaft | Laden-Verwaltung · Glücksbrett-Saison · Massen-Geschenk · Währungs-Statistik | – | ADMIN, OWNER | **NEU** |
| Live-Betrieb | Instanzen & Server · Wartung planen · Feature-Schalter | – | ADMIN, OWNER; DEV Lesen | **NEU** |
| | Bühne (Ankündigungen, Events …) | /buehne | MOD, ADMIN, OWNER (Events nur ADMIN, OWNER); DEV Lesen | bleibt |
| Entwicklung | Entwickler | /entwickler, /asset-karte | DEV, ADMIN, OWNER | bleibt |
| | Debug-Overlay · Client-Logs anfordern | – | DEV, ADMIN, OWNER | **NEU** |
| Verwaltung | Rollen & Rechte (mit „Rolle setzen“) | /rolle | OWNER; ADMIN eingeschränkt | „Rolle setzen“ bleibt, Rest **NEU** |
| | Staff-Liste · Audit-Log · Sicherheit · Freigaben | – | OWNER; ADMIN Lesen | **NEU** |
| Werkzeuge in der Welt | Unsichtbar · Teleport zu Spieler · Spieler holen · Freie Kamera | – | 3a.3 | **NEU** |

MOD behält die Bühne wie heute (Prinzip 9, Einschränkungen bleiben). Deshalb sieht MOD die Kategorie Live-Betrieb nur mit diesem einen Menü.

#### 3a.2.1 Moderation

| Menü | Inhalt | Knöpfe |
|---|---|---|
| Meldungen | wie 3.9: Filter Offen / Erledigt / Abgewiesen / Alle, Zeilen je Meldung, „Zurück“ / „Weiter“; Detail „Meldung“ mit Ziel, Grund, Details, Gemeldet von, Status, Feld „Notiz“ | wie heute: Abweisen, Erledigen, Map ausblenden, Map sperren, Map freigeben, Kommentar ausblenden, „Zurück zur Liste“. **NEU**: KONTO-AKTE ÖFFNEN bei Ziel und „Gemeldet von“ · NEUE SANKTION (Sanktions-Dialog mit dieser Meldung als Beweis) |
| Spieler | wie 3.9: Suche (Feld Name, „Suchen“, Trefferzeilen); Detail mit Name, Rang, Status, Aufenthalt, Grund, Auswahl Sperre und Stumm | wie heute: Sperren, Stummschalten, Kicken, Sperre aufheben, Stumm aufheben, „Zurück zur Suche“. **NEU**: KONTO-AKTE ÖFFNEN im Detail; jede Aktion mit Bestätigung und Vorschau (3a.4) |
| Chat-Live (**NEU**) | Live-Feed aller Instanzen als Tabelle: Zeit, Instanz („Plaza 2“, „Bauplatz von X“, „Match: Raum“), Kanal, Kennzeichen + Name, Text. Filter: Instanz (Dropdown „Alle Instanzen“ oder einzelne), Spieler (Feld), Wörter (Feld, mehrere mit Komma, Treffer gold markiert), Chip „Nur Treffer“. Puffer 200 Zeilen. Flüstern und Party-Funk erscheinen nicht (Datenschutz, 20/O20); gemeldete Zeilen kommen über Meldungen. | je Zeile (Hover, Fokus, Gamepad-X): LÖSCHEN (die Zeile wird bei allen ersetzt durch „Nachricht von der Moderation entfernt.“) · STUMM (Sanktions-Dialog mit Art Stumm, Zeile als Beweis) · KONTO-AKTE. Kopf: PAUSE / WEITER; Scrollen nach oben pausiert, die Pille „n neue Zeilen“ springt ans Ende. |
| Replays | wie 3.9: Feld „Spieler oder Replay-ID“, „Suchen“; Zeilen „Map (Modus)“ mit Dauer und Alter | wie heute: Klick öffnet die Replay-Ansicht. Replay-IDs findet auch die Suche der TEAM-Seite. |
| Sanktions-Verlauf (**NEU**) | alle Sanktionen aller Konten: ZEIT / SPIELER / ART / DAUER / GRUND / VON / STATUS (aktiv, abgelaufen, aufgehoben); Filter-Chips Alle · Aktiv · Sperre · Stumm · Kick; Felder Staff und Zeitraum | Zeile → Konto-Akte › Sanktionen · AUFHEBEN an aktiven Sanktionen · „Zurück“ / „Weiter“ |

#### 3a.2.2 Spielerverwaltung: Konto-Akte (**NEU**)
Eine Akte je Konto, geöffnet über die Suche, /akte [name] oder KONTO-AKTE ÖFFNEN (3a.5). ADMIN und OWNER bearbeiten, MOD liest (Ausnahmen in 3a.3). Jede Änderung folgt den Sicherheitsregeln (3a.4).

**Konto-Kopf** (steht immer über den Reitern)

| Teil | Inhalt |
|---|---|
| Identität | Rang-Abzeichen (`rank_t*` + Zahl), Name, Kennzeichen (`UiNameBadges`), Rollen-Badges, Konto-ID (`mono`, Knopf Kopieren) |
| Status | Online-Punkt (`good.text`) und Ort („Plaza 2“, „Bauplatz von X“, „Match: Raum · Modus“) bzw. „offline · zuletzt vor n Tagen“ |
| Sanktionen | aktive Sanktionen als rote Etiketten, z. B. „GESPERRT BIS …“, „STUMM 2 STD.“; Klick → Reiter Sanktionen |
| Schnellaktionen | TELEPORTIEREN ZU · HOLEN · ZUSCHAUEN (nur wenn der Spieler im Match ist, öffnet den ReplayViewer live) · POST SENDEN (→ Reiter Sozial › Post). Offline sind die drei ersten ausgegraut mit Tooltip „Spieler ist offline.“ |

**Reiter** (Tabs; Tastatur 1–9 und 0, Gamepad LT/RT; der letzte Reiter wird je Sitzung gemerkt)

| Reiter | Inhalt | Aktionen |
|---|---|---|
| Übersicht | Erstellt am, letzte Anmeldung, Spielzeit gesamt; Geräte und Sitzungen (Tabelle GERÄT / SYSTEM / ZULETZT / SITZUNGEN 30 TAGE, IP nur gekürzt); Staff-Notizen mit Text, Autor (Name + Rollen-Badge) und Datum, neueste oben | NOTIZ HINZUFÜGEN (Feld, SPEICHERN). Notizen sind unveränderlich wie das Protokoll. |
| Währungen | 4 Karten Brix · Splitter · Kristalle · Münzen (`cur_*`, Betrag `num`); Verlauf ZEIT / WÄHRUNG / BETRAG / QUELLE / DETAIL / VON mit Filter-Chips Alle · Kauf · Match · Belohnung · Glücksbrett · Admin · Rückerstattung | je Karte HINZUFÜGEN · ABZIEHEN · SETZEN → Dialog mit Währungsfeld (Betrag), Grund (Pflicht) und Vorschau „alt → neu“; ein Guthaben wird nie negativ. RÜCKGÄNGIG an Einträgen der Quelle Admin (Gegenbuchung). |
| Inventar | gleiches Raster und gleiche Filter wie SPIND › Inventar (Alle, Waffen, Kleidung, Access., Verbrauch, Werkzeug, Gems; Abzeichen „AN“; Detail mit Laufzeit, „BONI“, „UPGRADES“); darunter Ausrüstung/Loadout wie SPIND › Loadout als reine Ansicht | ITEM GEBEN (Item-Auswahl: Katalog-Suche, Laufzeit 1 Tag / 7 Tage / 30 Tage / Dauerhaft, Anzahl, Sterne/Upgrades, Gems, optional mit Post-Notiz) · im Detail: ENTZIEHEN · LAUFZEIT ÄNDERN · AUFWERTEN / ABWERTEN · ZERLEGEN RÜCKGÄNGIG (zuletzt zerlegte Items; zieht die erhaltenen Splitter wieder ab) · unter dem Loadout: AUSRÜSTUNG ZURÜCKSETZEN |
| Fortschritt | Rang und XP (Balken wie im Profil); Waffen-Mastery je Waffe (WAFFE / STUFE / PUNKTE); Erfolge (Raster); Tagesmissionen (3 Zeilen); Serie der Täglichen Belohnung (Tag n von 7); Einführung (Schritt i/n); Glücksbrett (Münzen, Brett mit aufgedeckten Feldern) | RANG/XP SETZEN (ersetzt Verwaltung „XP setzen“: XP gesamt, Grund, Vorschau „Rang alt → neu“) · Mastery SETZEN je Zeile · Erfolge FREISCHALTEN / ZURÜCKSETZEN (Checkbox „Belohnung auszahlen“) · Tagesmissionen NEU WÜRFELN / ABSCHLIESSEN · Serie SETZEN · EINFÜHRUNG ZURÜCKSETZEN · Glücksbrett: Münzen SETZEN (dieselbe Buchung wie im Reiter Währungen), Felder AUFDECKEN / ZUDECKEN |
| Maps & Bauplatz | Map-Slots 1–6 (leer, belegt, gesperrt) wie ERSTELLEN › Meine Maps; eigene veröffentlichte Maps (Name, Version, Downloads, „AUSGEBLENDET“ / „GESPERRT“); Mitbauer je Slot | Slot FREISCHALTEN / SPERREN · Map ANSEHEN (Detail wie Map-Galerie) · BETRETEN (Instanzwechsel auf den Bauplatz; mit UNSICHTBAR, wenn aktiv) · AUSBLENDEN / SPERREN / FREIGEBEN (dieselben Aktionen wie „Map ausblenden“, „Map sperren“, „Map freigeben“ in Meldungen) · Mitbauer BAURECHT NEHMEN |
| Sozial | Freunde, Party (aktuell), Clan (Emblem, Rolle im Clan), Post (nur Team-Post an dieses Konto; private Nachrichten bleiben privat), Gesperrt-Liste | Clan: AUS CLAN ENTFERNEN · LEITUNG ÜBERTRAGEN (an ein Mitglied) · Post: NACHRICHT SENDEN / GESCHENK SENDEN als „Brixel-Team“ (Item-Auswahl bzw. Währungsfeld) |
| Sanktionen | aktive Sanktionen oben, Verlauf darunter: ART / DAUER / GRUND / BEWEIS / VON / ZEIT / STATUS | NEUE SANKTION (Chips Sperre / Stumm / Kick; Dauer wie heute „Auswahl Sperre und Stumm“; Grund; Beweis: Meldung oder Replay-ID über die Suche) · AUFHEBEN |
| Käufe | Kaufverlauf: ZEIT / ITEM / LAUFZEIT / PREIS / STATUS (aktiv, abgelaufen, erstattet) | RÜCKERSTATTEN (Vorschau: Währung + Betrag zurück, Item entfernt bzw. Laufzeit beendet) |
| Support | Tickets des Spielers: Kategorie, Betreff, Status, letzte Antwort; Ticket-Ansicht wie Hilfe und Support | Ticket öffnen · ANTWORTEN als „Support“ (20/O22) |
| Protokoll | jede Staff-Aktion an diesem Konto: ZEIT / WER (Name + Rollen-Badge) / AKTION / GRUND / VORHER → NACHHER / STATUS (ausgeführt, wartet auf Freigabe, abgelehnt, rückgängig) | RÜCKGÄNGIG, wo möglich: Gegenaktion mit eigenem Grund und eigenem Eintrag. Nicht möglich bei Kick, gesendeter Post und Teleport. |

#### 3a.2.3 Wirtschaft (**NEU**)

| Menü | Inhalt | Knöpfe |
|---|---|---|
| Laden-Verwaltung | Tabelle aller Katalog-Items: ITEM / KATEGORIE / 1 TAG / 7 TAGE / 30 TAGE / DAUERHAFT (Preis je Laufzeit als Zahlenfeld) / SICHTBAR (Schalter). Angebote und Rabatte: Items, „-n %“, Zeitfenster von–bis (Datum/Zeit). Empfohlen-Plätze: Reihenfolge der Karten in LADEN › Empfohlen (Item-Auswahl je Platz). | SPEICHERN (Diff aller geänderten Preise und Schalter; sofort oder zu einem Zeitpunkt) · ANGEBOT ANLEGEN · BEENDEN · Platz LEEREN |
| Glücksbrett-Saison | laufende Saison (Name, Ende, „n von m Feldern offen“); Gewinne je Stufe (Item, Stufe, Felder); Quoten-Vorschau wie der Dialog „Quoten“ (GEWINN / STUFE / FELDER / CHANCE); Vorschau des Bretts | GEWINN HINZUFÜGEN / ENTFERNEN · SPEICHERN · NEUES BRETT (neue Saison: Name, Ende, Felder; Tipp-Bestätigung mit dem Saison-Namen) |
| Massen-Geschenk | Empfänger: Chips Alle / Segment; Segment nach Rang von–bis, online jetzt, Clan, zuletzt aktiv (≤ n Tage). Inhalt: Währungsfeld und/oder Item-Auswahl. Post: Betreff, Text, Absender „Brixel-Team“. Zeitpunkt: sofort oder Datum/Zeit. Vorschau „n Konten erhalten …“ mit 5 Beispiel-Empfängern. | VORSCHAU AKTUALISIEREN · ZUR FREIGABE SENDEN (immer Vier-Augen-Freigabe, 3a.4) |
| Währungs-Statistik | Zeitraum-Chips 7 / 30 / 90 Tage; Umlauf je Währung (Linie); Quellen und Senken pro Tag (Balken; Quellen: Match, Belohnung, Glücksbrett, Admin, Rückerstattung; Senken: Kauf, Werkstatt, Map-Downloads, Gebühren); Admin-Anteil getrennt ausgewiesen | nur Ansicht; „Als Tabelle“ |

#### 3a.2.4 Live-Betrieb (**NEU**, Bühne wie heute)

| Menü | Inhalt | Knöpfe |
|---|---|---|
| Instanzen & Server | Tabelle INSTANZ / ART (Plaza, Bauplatz, Match, Asset-Karte) / SPIELER (n/max) / LAST (Balken + Tick-Zeit in ms) / LÄUFT SEIT; Filter-Chips nach Art | BEITRETEN (Instanzwechsel; Match nur als Zuschauer) · ZUSCHAUEN (Match → ReplayViewer live) · NACHRICHT AN INSTANZ (Text, Art Banner oder Chat-Systemzeile) · NEU STARTEN (60-s-Countdown für die Spieler; Tipp-Bestätigung mit dem Instanz-Namen) · SCHLIESSEN (Spieler wechseln zur Plaza; Tipp-Bestätigung) |
| Wartung planen | Zeitpunkt (Datum/Zeit), voraussichtliche Dauer, Meldung (Standard „Dein Fortschritt wird gespeichert.“), Vorschau des Wartungsbands; Liste geplanter Wartungen | WARTUNG PLANEN · VERSCHIEBEN · ABSAGEN. Steuert das Wartungsband (`LiveHud`, „Wartung in m:ss“ in den letzten 15 Min., Ebene 70) und danach den Wartungs-Kick (Fehlerkarte „Wartung“). |
| Feature-Schalter | Zeilen Tägliche Belohnung · Hilfe und Support · Fehler melden (die Schalter aus dem Inventar) · **NEU** Events · **NEU** Glücksbrett; je Zeile Beschreibung, betroffene Einträge, Zustand, zuletzt geändert von/um | Schalter umlegen → Bestätigung mit Vorschau „an → aus“ und Grund. Wirkt sofort bei allen Clients; der Eintrag verschwindet wie heute (3.14 „Schalter“). Events aus: Events in Neuigkeiten, Karussell-Folie „Event läuft“ und Event-Bonus-Chip ausgeblendet. Glücksbrett aus: LADEN › Glücksbrett ausgeblendet. |
| Bühne | wie 3.9 (/buehne): Bühne stummschalten/freigeben, Ankündigungen, Events (nur ADMIN, OWNER), Map der Woche, Event-Hosts, Auf die Bühne holen | wie heute; **NEU** „Start“ der Events als Datum/Zeit-Feld |

#### 3a.2.5 Entwicklung

| Menü | Inhalt | Knöpfe |
|---|---|---|
| Entwickler | wie 3.9: „Inhalte, Instanzen und Werkzeuge“ (Inhaltsversion, Waffen-Version, Overlay, Instanzen, Asset-Karte) | wie heute: „Asset-Karte betreten“, „Asset-Aufnahmen“, „Inhalte neu laden“ |
| Debug-Overlay (**NEU**) | Schalter für das eigene Spiel: Verlauf von Bildrate und Ping, UiState-Stapel (18.7), Canvas-Ebenen (Kapitel 9), Draw Calls und UI-Budget (18.12), Fokus-Gruppe des PadNavigator | nur lokal sichtbar, nie für andere; nicht im Foto (18.10) |
| Client-Logs anfordern (**NEU**) | Konto (Suche), Zeitraum (letzte Sitzung oder letzte 24 Std.), Grund; Liste der Anfragen mit Status (angefragt, hochgeladen, abgelaufen) | ANFORDERN · LINK KOPIEREN. Der Spieler sieht den Toast „Das Brixel-Team hat ein Fehlerprotokoll angefordert.“ (20/O21). |

#### 3a.2.6 Verwaltung

| Menü | Inhalt | Knöpfe |
|---|---|---|
| Rollen & Rechte | „Rolle setzen“ wie heute: Konto, Rolle player / moderator / developer / admin / owner, Grund, „Rolle setzen“ (admin und owner nur durch OWNER, 11.3). **NEU** Rechte-Matrix (3a.3) als Tabelle. | „Rolle setzen“ mit Tipp-Bestätigung. Matrix: OWNER ändert Zellen per Stepper ✓ / Lesen / – und SPEICHERN (Diff, Tipp-Bestätigung); ADMIN liest. „XP setzen“ liegt jetzt in Konto-Akte › Fortschritt (RANG/XP SETZEN); hier bleibt der Verweis „XP setzen“, der dorthin führt. |
| Staff-Liste (**NEU**) | alle Team-Mitglieder: NAME / ROLLE (Badge) / ZULETZT AKTIV / AKTIONEN (7 TAGE) | Zeile → Konto-Akte · Zahl der Aktionen → Audit-Log, gefiltert auf die Person |
| Audit-Log (**NEU**, global) | alle Staff-Aktionen: ZEIT / WER / AKTION / ZIEL / GRUND / VORHER → NACHHER / FREIGABE / STATUS; Filter Person, Aktion, Konto, Zeitraum | EXPORTIEREN (CSV, nur OWNER) · RÜCKGÄNGIG wie im Protokoll der Konto-Akte |
| Sicherheit (**NEU**) | Schwellen der Vier-Augen-Freigabe (Zahlenfelder je Währung, Schalter „Massen-Geschenk immer“ und „Rückerstattung immer“), Rate-Limits (3a.4), Ablauf offener Freigaben (Standard 48 Std.) | SPEICHERN (Diff, Tipp-Bestätigung) |
| Freigaben (**NEU**) | Warteschlange: Aktion, Ziel, Diff, Grund, Antragsteller mit Rollen-Badge, Zeit, „läuft ab in …“ | FREIGEBEN · ABLEHNEN (Grund Pflicht); Antragsteller: ZURÜCKZIEHEN. Zähler am TEAM-Schild, am Eintrag und im Staff-Kopf (nur OWNER); Antragsteller erfahren das Ergebnis über Glocke und Toast. |

#### 3a.2.7 Werkzeuge in der Welt (**NEU**)

| Werkzeug | Wo | Verhalten | Grenzen |
|---|---|---|---|
| UNSICHTBAR (Vanish, **NEU**) | Staff-Kopf (P); kleines Esc-Menü › TEAM-WERKZEUGE (B, A) | Schalter. Figur, Namensschild, Zeile in der Tab-Liste und der Ort für Freunde (dann „offline“) verschwinden für alle ohne Staff-Rolle; Staff sieht sich gegenseitig als Geist (`ghost`). Solange aktiv, steht oben links unter der Info-Leiste die HUD-Pille „UNSICHTBAR“ (`pill_staff_status`, Ebene 12). | nicht als aktiver Spieler im Match; eigener Sprachchat ist stumm |
| FREIE KAMERA (**NEU**) | Staff-Kopf (P); Esc-Menü › TEAM-WERKZEUGE (B, A) | Hub bzw. Menü schließt, die Kamera löst sich von der Figur; Steuerung wie im ReplayViewer (WASD, E/Q, Shift; Gamepad Sticks). HUD-Pille „FREIE KAMERA · Esc beendet“; Esc beendet zuerst die freie Kamera (3.12 #14). | im Match nur als Zuschauer oder Geist |
| TELEPORT ZU SPIELER (**NEU**) | Konto-Kopf TELEPORTIEREN ZU; Esc-Menü › TEAM-WERKZEUGE (Namensfeld mit Vorschlägen) | Sprung an die Position des Spielers; in einer anderen Instanz mit Instanzwechsel („Instanz wird gewechselt“) | Ziel im Match → nur als Zuschauer (wie ZUSCHAUEN) |
| SPIELER HOLEN (**NEU**) | Konto-Kopf HOLEN; Esc-Menü › TEAM-WERKZEUGE (Namensfeld) | holt den Spieler an die eigene Position, auch aus einer anderen Plaza, einem Bauplatz oder der Asset-Karte; der Spieler sieht den Toast „Du wurdest vom Brixel-Team geholt.“ | nie aus einem oder in ein laufendes Match |

Jede Nutzung erzeugt einen Protokoll-Eintrag (Unsichtbar an/aus, Freie Kamera an/aus, Teleport, Holen).

### 3a.3 Rechte-Matrix
✓ = sehen und ausführen · Lesen = sehen ohne Aktionen (Knöpfe ausgeblendet, Felder gesperrt, Etikett „NUR LESEN“) · – = erscheint nicht. Das ist die Standardbelegung; OWNER kann sie unter Verwaltung › Rollen & Rechte ändern. Fest bleiben: Spieler sehen nichts, und nur OWNER vergibt admin und owner.

| Funktion | Spieler | MOD | DEV | ADMIN | OWNER |
|---|---|---|---|---|---|
| **TEAM-Seite** | | | | | |
| TEAM-Seite, Suche, „zuletzt geöffnet“ | – | ✓ | ✓ | ✓ | ✓ |
| **Moderation** | | | | | |
| Meldungen (/meldungen) | – | ✓ | – | ✓ | ✓ |
| Spieler (/spieler): Sperren, Stummschalten, Kicken, Aufheben | – | ✓ | – | ✓ | ✓ |
| Chat-Live: mitlesen, filtern | – | ✓ | – | ✓ | ✓ |
| Chat-Live: LÖSCHEN, STUMM aus der Zeile | – | ✓ | – | ✓ | ✓ |
| Replays (/replays) | – | ✓ | – | ✓ | ✓ |
| Sanktions-Verlauf, AUFHEBEN | – | ✓ | – | ✓ | ✓ |
| **Spielerverwaltung: Konto-Akte** | | | | | |
| Konto-Akte öffnen, alle Reiter lesen (/akte) | – | Lesen | – | ✓ | ✓ |
| Staff-Notiz hinzufügen | – | ✓ | – | ✓ | ✓ |
| Sanktionen: NEUE SANKTION, AUFHEBEN | – | ✓ | – | ✓ | ✓ |
| Maps: AUSBLENDEN, SPERREN, FREIGEBEN | – | ✓ | – | ✓ | ✓ |
| Währungen: HINZUFÜGEN, ABZIEHEN, SETZEN, RÜCKGÄNGIG | – | Lesen | – | ✓ | ✓ |
| Inventar: ITEM GEBEN, ENTZIEHEN, LAUFZEIT ÄNDERN, AUFWERTEN / ABWERTEN, ZERLEGEN RÜCKGÄNGIG, AUSRÜSTUNG ZURÜCKSETZEN | – | Lesen | – | ✓ | ✓ |
| Fortschritt: Rang/XP, Mastery, Erfolge, Tagesmissionen, Serie, Einführung, Glücksbrett | – | Lesen | – | ✓ | ✓ |
| Maps & Bauplatz: Slots, BETRETEN, Mitbauer | – | Lesen | – | ✓ | ✓ |
| Sozial: Clan-Aktionen, Post als „Brixel-Team“ | – | Lesen | – | ✓ | ✓ |
| Käufe: RÜCKERSTATTEN | – | Lesen | – | ✓ | ✓ |
| Support: Tickets, ANTWORTEN | – | Lesen | – | ✓ | ✓ |
| Protokoll, RÜCKGÄNGIG | – | Lesen | – | ✓ | ✓ |
| **Wirtschaft** | | | | | |
| Laden-Verwaltung | – | – | – | ✓ | ✓ |
| Glücksbrett-Saison | – | – | – | ✓ | ✓ |
| Massen-Geschenk | – | – | – | ✓ | ✓ |
| Währungs-Statistik | – | – | – | ✓ | ✓ |
| **Live-Betrieb** | | | | | |
| Instanzen & Server | – | – | Lesen | ✓ | ✓ |
| Wartung planen | – | – | Lesen | ✓ | ✓ |
| Feature-Schalter | – | – | Lesen | ✓ | ✓ |
| Bühne (/buehne) ohne Events | – | ✓ | Lesen | ✓ | ✓ |
| Bühne › Events | – | – | Lesen | ✓ | ✓ |
| **Entwicklung** | | | | | |
| Entwickler (/entwickler, /asset-karte) | – | – | ✓ | ✓ | ✓ |
| Debug-Overlay, Client-Logs anfordern | – | – | ✓ | ✓ | ✓ |
| **Verwaltung** | | | | | |
| Rolle setzen: player, moderator, developer (/rolle) | – | – | – | ✓ | ✓ |
| Rolle setzen: admin, owner | – | – | – | – | ✓ |
| Rechte-Matrix | – | – | – | Lesen | ✓ |
| Staff-Liste | – | – | – | Lesen | ✓ |
| Audit-Log (global) | – | – | – | Lesen | ✓ |
| Audit-Log exportieren | – | – | – | – | ✓ |
| Sicherheit (Schwellen, Rate-Limits) | – | – | – | Lesen | ✓ |
| Freigaben erteilen | – | – | – | Lesen | ✓ |
| **Werkzeuge in der Welt** | | | | | |
| UNSICHTBAR | – | ✓ | – | ✓ | ✓ |
| FREIE KAMERA | – | ✓ | ✓ | ✓ | ✓ |
| TELEPORT ZU SPIELER, ZUSCHAUEN | – | ✓ | – | ✓ | ✓ |
| SPIELER HOLEN | – | – | – | ✓ | ✓ |

- ADMIN sieht unter Freigaben nur die eigenen Anträge.
- MOD liest die Konto-Akte, darf darin aber, was er heute schon darf: sanktionieren (wie im Menü Spieler) und Maps ausblenden, sperren und freigeben (wie in Meldungen). Dazu kommen Staff-Notizen (20/O18).
- Gegenüber dem Inventar: OWNER darf alles (11.3); MOD behält die Bühne ohne Events; DEV liest Live-Betrieb (**NEU**); „XP setzen“ zieht in die Konto-Akte um und bleibt ADMIN.
- Über allem stehen die Sicherheitsregeln (3a.4): nie am eigenen Konto, nie an gleicher oder höherer Rolle, Schwellen führen zur Freigabe.

### 3a.4 Sicherheitsregeln

| # | Regel | Umsetzung |
|---|---|---|
| 1 | Jede schreibende Aktion braucht einen Grund. | Feld „Grund“ im Bestätigungsdialog, Pflicht, mindestens 10 Zeichen; optional Bezug (Meldung, Ticket, Replay-ID). Bei Meldungen dient das Feld „Notiz“ als Grund. |
| 2 | Jede schreibende Aktion hat einen Bestätigungsdialog mit Vorschau. | Der Dialog „Bist du sicher?“ (JA, AUSFÜHREN / ABBRECHEN) zeigt die Diff-Ansicht „alt → neu“. Die Vorschau rechnet der Server. Hat sich der Wert bis zum Ausführen geändert, kommt „Der Wert hat sich geändert.“ mit neuer Vorschau. |
| 3 | Jede Aktion landet im Protokoll. | Eintrag mit wer, wann, Aktion, Ziel, Grund, vorher, nachher, Freigabe; sichtbar in Konto-Akte › Protokoll und Verwaltung › Audit-Log. Einträge werden nie gelöscht; RÜCKGÄNGIG ist ein neuer Eintrag. |
| 4 | Destruktive Aktionen brauchen eine Tipp-Bestätigung. | Man tippt den Kontonamen des Ziels (Groß/Klein egal, Einfügen gesperrt); ohne Konto den Namen des Objekts (Instanz, Saison). Gilt für ENTZIEHEN, AUSRÜSTUNG ZURÜCKSETZEN, Erfolge ZURÜCKSETZEN, Währung SETZEN auf 0, dauerhafte Sperre, Slot oder Map SPERREN, AUS CLAN ENTFERNEN, LEITUNG ÜBERTRAGEN, RÜCKERSTATTEN, „Rolle setzen“, NEU STARTEN, SCHLIESSEN, NEUES BRETT und SPEICHERN in Rechte-Matrix und Sicherheit. |
| 5 | Über Schwellen gilt die Vier-Augen-Freigabe. | Der Knopf im Dialog heißt dann ZUR FREIGABE SENDEN statt JA, AUSFÜHREN. OWNER entscheidet unter Verwaltung › Freigaben. Schwellen siehe unten. |
| 6 | Nie am eigenen Konto, nie an gleicher oder höherer Rolle. | Der Server lehnt ab; die Seite zeigt nur Lesen mit dem Hinweis „Eigenes Konto – nur Lesen.“ bzw. „Gleiche oder höhere Rolle – nur Lesen.“ (erweitert den heutigen Hinweis bei geschützten Staff-Konten; OWNER-Konten 20/O23). |
| 7 | Rate-Limits | Grenzen siehe unten. Beim Erreichen ist der Knopf deaktiviert, Tooltip „Limit erreicht – wieder frei in m:ss“; der Server lehnt mit demselben Text ab. |
| 8 | Niedrigere Rollen lesen nur. | Rechte-Matrix 3a.3; Etikett „NUR LESEN“. |
| 9 | Jede Aktion bestätigt sich mit einem Toast. | „Gespeichert · im Protokoll“ (`toast_plate` mit `icon_audit_log`, Klick → Protokoll-Eintrag); bei Freigabe „Zur Freigabe gesendet · im Protokoll“; bei Fehlern der Ablehnungs-Toast mit dem Grund vom Server. |

**Schwellen der Vier-Augen-Freigabe** (Standard, änderbar unter Verwaltung › Sicherheit)

| Auslöser | Schwelle |
|---|---|
| Währungsänderung je Aktion | > 10.000 Brix · > 500 Kristalle · > 5.000 Splitter (Vorschlag, 20/O24) · > 20 Münzen (Vorschlag, 20/O24) |
| Summe der Währungsänderungen je Ziel-Konto in 24 Std. | dieselben Werte (verhindert Stückeln) |
| Massen-Geschenk | immer |
| Rückerstattung | immer |

Offene Freigaben verfallen nach 48 Std. Aktionen eines OWNER über der Schwelle laufen ohne Freigabe und sind im Audit-Log markiert (20/O19).

**Rate-Limits** (Vorschlag, je Staff-Konto)

| Aktion | Grenze |
|---|---|
| Sanktionen | 30 je Std. |
| Chat-Zeile LÖSCHEN | 120 je Std. |
| Währungsänderungen | 20 je Std., davon höchstens 5 je Std. am selben Ziel-Konto |
| ITEM GEBEN, ENTZIEHEN | 30 je Std. |
| RÜCKERSTATTEN | 10 je Tag |
| Massen-Geschenk | 1 je Std. |
| NEU STARTEN, SCHLIESSEN | 1 je 5 Min. je Instanz |
| Client-Logs anfordern | 10 je Std. |
| Suche | 60 je Min. |

**Beispiel: ADMIN schreibt 15.000 Brix gut**
1. Konto-Akte › Währungen › Karte Brix › HINZUFÜGEN.
2. Dialog „Brix hinzufügen“: Betrag 15.000, Grund „Ersatz für Fehlkauf, Ticket 4711“.
3. Vorschau „12.400 → 27.400“ mit Etikett „Freigabe nötig (> 10.000 Brix)“; der Knopf heißt ZUR FREIGABE SENDEN.
4. Toast „Zur Freigabe gesendet · im Protokoll“; im Protokoll steht „wartet auf Freigabe“.
5. OWNER: Glocke „Freigabe angefragt“ → Verwaltung › Freigaben → FREIGEBEN. Der Server prüft den Stand erneut und bucht. Der OWNER sieht „Gespeichert · im Protokoll“, der ADMIN bekommt den Glocke-Eintrag „Freigegeben“.

### 3a.5 Einstiege

| Einstieg | Wo | Ziel | Neu |
|---|---|---|---|
| TEAM-Schild (rot) in der Top-Leiste | P | TEAM-Seite im Hub, zuletzt offenes Menü | wie 3.9 |
| TEAM im kleinen Esc-Menü | A, B | TEAM-Einzelseite `page.team` | auf B **NEU** (löst 20/O3) |
| TEAM-WERKZEUGE im kleinen Esc-Menü | B, A | Unterliste UNSICHTBAR · FREIE KAMERA · TELEPORT ZU SPIELER … · SPIELER HOLEN … | **NEU** |
| „•••“ → Spieler-Aktionen › Block „TEAM“ › KONTO-AKTE ÖFFNEN | alle Spielerlisten: Tab-Liste (Spielerliste und Punktestand), Warteraum, Ergebnis, Bauplatz-Fenster › Mitbauer, ReplayViewer-Spielerliste (Live) | Konto-Akte › Übersicht | **NEU** |
| KONTO-AKTE ÖFFNEN im Profil-Popup (fremdes Profil) | P, B, A, M | Konto-Akte | **NEU** |
| Sozial-Panel: Zeilen in Freunde, Party, Clan (Mitglieder), Post (Absender), Gesperrt; Kontext per Rechtsklick bzw. Gamepad-X | P, B, A | Konto-Akte | **NEU** |
| Meldungs-Detail, Spieler-Detail, Chat-Live-Zeile, Sanktions-Verlauf, Staff-Liste | TEAM-Seite | Konto-Akte | **NEU** |
| Chat-Befehle | überall | P: TEAM-Seite im Hub · B, A: Einzelseite · M: Baukasten-Modal (Ebene 50), jeweils direkt beim Menü | **NEU** /akte [name]; /meldungen, /spieler [name], /replays [name], /buehne, /entwickler, /asset-karte, /rolle wie heute |
| Glocke: „Freigabe angefragt“ (OWNER), „Freigegeben“ / „Abgelehnt“ (Antragsteller) | P | Verwaltung › Freigaben bzw. Protokoll-Eintrag | **NEU** |

- KONTO-AKTE ÖFFNEN sieht nur, wer die Konto-Akte mindestens lesen darf (MOD, ADMIN, OWNER). Der Block „TEAM“ steht in den Spieler-Aktionen über PROFIL / SCHLIESSEN, mit der roten Akzentlinie oben. An der eigenen Zeile fehlt er; die eigene Akte öffnet man nur über die Suche, und auch dann nur zum Lesen.
- Im Match öffnet KONTO-AKTE ÖFFNEN das Baukasten-Modal (Ebene 50) wie die Chat-Befehle. Die Spieler-Aktionen schließen, die angeheftete Tab-Liste wird gelöst; Esc führt zurück ins Spiel.
- TEAM-Schild und TEAM-Eintrag gibt es im Match weiter nicht (3.14).

### 3a.6 UI-Muster: neue Baukasten-Elemente, Look und Motion
Zu den 8 Element-Arten des Baukastens (Heading, Text, Info, Row, Button Normal/Primary/Danger/Muted, Field, Select-Stepper, Separator) kommen **NEU**:

| # | Element-Art | Aussehen | Verhalten | Assets |
|---|---|---|---|---|
| 1 | Tabs | wie die Unterreiter: `tab_inactive` / `tab_active` mit gleitendem `tab_underline`, optional Zähler; Kompakt nur Icons | 1–9 und 0 bzw. LT/RT; letzter Reiter wird gemerkt | `tab_*` |
| 2 | Tabelle (sortierbar, seitenweise) | `frame_data_table`: Kopfband mit Spaltenköpfen (`label`, `gold.light`), sortierbare Spalten mit `icon_sort`; Zeilen wie `list_row` dicht (44), Zahlen rechtsbündig in `num`, IDs in `mono`; im Kopf optional Filter-Chips und Suchfeld; Fuß „Seite x / y“ mit „Zurück“ / „Weiter“ | Klick auf einen Spaltenkopf sortiert auf → ab → aus; 50 Zeilen je Seite; Sortieren, Filtern und Blättern rechnet der Server; Zeilen sind klickbar wie Row; leer: „Keine Einträge.“ | `frame_data_table`, `list_row`, `icon_sort`, `chip_*` |
| 3 | Raster (Items mit Stufen-Rahmen) | Item-Kacheln wie SPIND › Inventar: `tile_slot` + `tier_frame_*` + `tier_sym_*` + Sterne + Etikett „AN“ | Auswahl öffnet das Detail rechts; Filter-Chips wie im Inventar | `tile_slot`, `tier_*`, `icon_star` |
| 4 | Zahlenfeld mit +/− | `input_text` mit `btn_minus` links und `btn_plus` rechts, Wert in `num` mittig | Tippen, Mausrad, Steuerkreuz links/rechts; Halten wiederholt (ab 400 ms 10/s, ab 1,5 s 30/s); Shift = ×10; Min/Max vom Server, außerhalb Fehler-Zustand | `input_text`, `btn_minus`, `btn_plus` |
| 5 | Währungsfeld mit Vorschau | Währungssymbol `cur_*` + Zahlenfeld + Segment HINZUFÜGEN / ABZIEHEN / SETZEN; darunter die Vorschau „alt → neu“ in `frame_diff_preview`; über der Schwelle Etikett „Freigabe nötig“ mit `icon_approval` | Vorschau vom Server; ein negativer Endstand wird nicht angenommen („Guthaben würde negativ.“) | `cur_*`, `frame_diff_preview`, `icon_approval` |
| 6 | Item-Auswahl (Katalog-Suche) | `input_search`, Trefferliste in `frame_dropdown_menu` mit kleiner Item-Kachel, Name, Typ, Stufe; danach Chips „LAUFZEIT“ (1 Tag, 7 Tage, 30 Tage, Dauerhaft), Anzahl (Zahlenfeld, nur bei stapelbaren Items), Sterne/Upgrades, Gems, Checkbox „Mit Post-Notiz“ + Text | Suche ab 2 Zeichen; Kategorie-Chips wie LADEN › Katalog | `input_search`, `frame_dropdown_menu`, `tile_slot`, `icon_item_give` |
| 7 | Datum/Zeit | `dropdown` mit `icon_calendar`: Monatsraster, Stunde und Minute als Stepper (15-Min.-Schritte), Schnellwahl-Chips „Jetzt“, „In 1 Std.“, „Heute 22:00“, „Morgen“; Anzeige in Serverzeit mit Zone | Vergangenheit gesperrt, wo nur die Zukunft Sinn hat (Wartung, Angebote, Events) | `dropdown`, `icon_calendar`, `stepper_*` |
| 8 | Diagramm (Linie, Balken) | `panel_inset`; Achsen in `caption`, `text.muted`; Hilfslinien `bg.raised`; Linie 2 px in der Währungsfarbe (`cur.*`); Balken: Quellen gold, Senken `danger`; Legende mit Symbol und Name | Hover bzw. Fokus zeigt den Wert als Tooltip; Knopf „Als Tabelle“ (Barrierefreiheit) | `panel_inset`, `tooltip_box`, `icon_economy_chart` |
| 9 | Bestätigung mit Tipp-Bestätigung | Dialog `frame_dialog` mit roter Akzentlinie oben, Diff-Ansicht, Satz „Tippe \<Kontoname\>, um zu bestätigen.“, Textfeld; JA, AUSFÜHREN als rote Platte | JA, AUSFÜHREN bleibt deaktiviert, bis die Eingabe stimmt; ABBRECHEN links | `frame_dialog`, `divider_staff`, `input_text`, `btn_red_m` |
| 10 | Diff-Ansicht (alt → neu) | `frame_diff_preview`, Zeilen „Feld · alt → neu“: alt durchgestrichen in `text.muted`, neu in `text.gold`; hinzugefügt mit „+“ in `good.text`, entfernt mit „−“ in `danger.text` (nie nur Farbe) | zeigt genau das, was der Server ausführen wird; bei Massen-Aktionen die Anzahl und Beispiele | `frame_diff_preview` |
| 11 | Schalter (ergänzt) | Schalter-Komponente aus 12.2 | Feature-Schalter, UNSICHTBAR, Debug-Overlay, Laden „SICHTBAR“ | `toggle_*` |
| 12 | Konto-Kopf (ergänzt) | `panel_inset` mit Rang-Abzeichen, Name, Kennzeichen, Rollen-Badges, Online-Punkt und Ort, Konto-ID in `mono` mit Kopieren, aktiven Sanktionen als rote Etiketten (`badge_tag`), Schnellaktionen als dunkle Platten S | Online-Status live | `panel_inset`, `rank_t*`, `role_*`, `badge_tag`, `btn_dark_m` |

**Look**
- Gleicher Stil wie der Hub (Kapitel 11 und 12): dunkle Panels mit Gold-Doppelrand, Gold-Platten für Aktionen, Fließtext nie gold.
- Staff-Kennung: Der Staff-Kopf `frame_staff_header` hat den Verlauf des ADMIN-Badges (`#AE4033` → `#7C100B`) mit Gold-Kontur; Text darauf `text.primary` (5,0 : 1 auf `#AE4033`) bzw. `text.gold`. Darunter liegt die dünne rote Akzentlinie `staff.line` (2 px, `#AE4033`, 3,4 : 1 auf `bg.panel`). Dieselbe Linie sitzt am linken Inhaltsrand, oben an jedem Staff-Dialog, am Baukasten-Modal im Match und am Block „TEAM“ der Spieler-Aktionen. So weiß Staff immer, dass es im Staff-Bereich ist.
- Rot markiert Bereich und Gefahr, Gold bleibt Aktion und Fokus. Gefahr-Aktionen (ENTZIEHEN, SPERREN, SCHLIESSEN …) sind rote Platten `btn_red_m`.
- Nur Lesen: Felder mit 50 % Deckkraft und `icon_lock`, keine Aktionsknöpfe, Etikett „NUR LESEN“ im Kopf der Seite.
- Toast „Gespeichert · im Protokoll“: `toast_plate` mit `icon_audit_log`; „Zur Freigabe gesendet · im Protokoll“ mit `icon_approval`.

**Motion** (Tokens aus 15.3–15.5; bei „Animationen reduzieren“ gilt 15.9)

| Fall | Eigenschaften | Dauer / Easing | Reduziert |
|---|---|---|---|
| TEAM-Seite öffnen | Staff-Kopf y −16 → 0 + Deckkraft; Akzentlinie zeichnet sich von links (Scale x 0 → 1, Pivot links); linke Liste Zeilen gestaffelt | Feder `snappy`; Linie 240 ms outCubic, 80 ms nach Start; 24 ms je Zeile, max. 8 | Fade 90 ms, Linie sofort |
| Menü wechseln, Tabs | Unterstrich gleitet; Inhalt Deckkraft 0 → 1, y 12 → 0 | `snappy`; 160 ms outCubic | Fade |
| Tabelle laden | Zeilen y 16 → 0 + Fade | 160 ms outCubic, 24 ms je Zeile, max. 8 | sofort |
| Tabelle sortieren | `icon_sort` dreht 180°; Zeilen überblenden | 160 ms outCubic; 120 ms | ohne Drehung |
| Tabelle blättern | alter Inhalt x 0 → −24 + Fade; neuer x +24 → 0 (Richtung = Blätterrichtung) | 120 ms inOutQuad; 240 ms outCubic | Fade |
| Chat-Live: neue Zeile | y 16 → 0 + Fade, gebündelt höchstens 10-mal/s; Wort-Treffer blitzt gold | 160 ms outCubic; 240 ms | sofort, ohne Blitz |
| Raster | wie Karten-Raster (15.5) | 32 ms je Diagonale | sofort |
| Zahlenfeld +/− | Press-Squash wie Platte S; Wert springt sofort; an Min/Max Shake x ±4 | 90 ms; 240 ms | ohne Shake |
| Vorschau alt → neu | „→“ gleitet 8 px ein, neuer Wert rollt; Etikett „Freigabe nötig“ ploppt | 160 ms outCubic; 600 ms; Feder `pop` | sofort |
| Item-Auswahl, Datum/Zeit | wie Dropdown (15.7) | 160 ms outCubic, Zeilen 16 ms | Fade |
| Diagramm | Linie zeichnet sich (Masken-Scale x 0 → 1); Balken Scale y 0 → 1 | 420 ms outCubic; 24 ms je Balken, max. 8 | sofort |
| Tipp-Bestätigung | Dialog-Pop; stimmt die Eingabe, wird der Knopf aktiv und glüht einmal rot; Enter bei falscher Eingabe → Shake | Feder `pop`; 240 ms; 240 ms | ohne Glühen und Shake |
| Freigabe erteilt | Zeile gleitet aus der Warteschlange (x 0 → +48 + Fade), der Rest rückt nach | 240 ms outCubic | sofort |
| HUD-Pille UNSICHTBAR / FREIE KAMERA | erscheint sofort (15.2); Glow-Puls 0,6 ↔ 1,0 | 1600-ms-Schleife inOutQuad | statisch |

Sounds wie gehabt (Kapitel 17): `ui_open`, `ui_tab`, `ui_select`, `ui_toggle_on/off`, `ui_toast`; Limit und falsche Tipp-Bestätigung `ui_error`. Es gibt keine neuen Sound-IDs.

### 3a.7 Unity- und Server-Umsetzung
- **Renderer:** `ServerMenuPanel` bleibt. Das Protokoll bekommt neue Element-Arten (`ServerMenuElementKind`): `Tabs`, `Table`, `Grid`, `NumberField`, `CurrencyField`, `ItemPicker`, `DateTime`, `Chart`, `TypedConfirm`, `Diff`, `Toggle`, `AccountHeader`. Jede Art ist ein Prefab mit Fabrik-Methode (z. B. `UiFactory.StaffTable(...)`) und liest Farben, Größen und Motion aus dem `UiTheme`. Der Server sendet eine Protokoll-Version; ein älterer Client zeigt eine unbekannte Art als Text „Dieses Element braucht eine neuere Version.“, statt abzustürzen.
- **Rahmen im Client, Inhalt vom Server:** Staff-Kopf, Akzentlinie, Suchfeld, „zuletzt geöffnet“ und die linke Liste baut der Client aus `staff.session`. Den Inhalt jedes Menüs baut der Server.
- **Tabellen:** Sortieren, Filtern und Blättern auf dem Server (50 Zeilen je Seite). Im Client eine virtualisierte Scroll-Ansicht mit Zeilen-Pool; nur sichtbare Zeilen sind aktiv. Chat-Live: Ringpuffer mit 200 Zeilen, Updates gebündelt höchstens 10-mal/s, keine GC-Allokation pro Zeile (18.12).
- **Diagramme:** ein `MaskableGraphic` je Serie (ein Mesh, ein Draw Call), höchstens 365 Punkte.
- **Vorschau und Ausführen in zwei Schritten:** Jede schreibende Aktion ruft zuerst mit `preview: true` auf. Der Server antwortet mit Diff, `confirmToken` (60 s gültig), `needsTypedConfirm`, `needsApproval` und ggf. einem Limit-Hinweis. Das Ausführen schickt Token, `reason`, ggf. `typedConfirm` und `evidence` (Meldung, Replay-ID, Ticket); der Server prüft alles erneut. Antwort: `auditId` und `status` (`done`, `pendingApproval`, `rejected` mit Grund).
- **Rechte nur auf dem Server:** Jeder Aufruf prüft das Recht aus der Rechte-Matrix (ein Schlüssel je Zeile, z. B. `account.currency.write`), die Rangfolge (Ziel ist nicht das eigene Konto, Ziel-Rolle liegt unter der eigenen), die Schwelle (→ Freigabe) und das Rate-Limit. Der Client blendet nur aus; jedes Element kann vom Server `readOnly` bekommen. Ändern sich Rolle oder Matrix, schickt der Server `staff.permissionsChanged`, und die TEAM-Seite baut sich neu auf.
- **Protokoll:** nur anhängen. Jede schreibende Aktion schreibt in derselben Transaktion genau einen Eintrag (wer, wann, Aktion, Ziel, Grund, vorher, nachher, Freigabe). RÜCKGÄNGIG ist eine neue Aktion mit Verweis `revertOf`.
- **Werkzeuge in der Welt:** Unsichtbar setzt der Server um. Er schickt die Figur des Staff-Kontos gar nicht erst an Clients ohne Staff-Rolle; ein Ausblenden im Client wäre für Cheats sichtbar. Freie Kamera läuft im Client (Kamera-Rig wie im ReplayViewer); der Server erlaubt sie nur außerhalb eines Matches oder als Zuschauer. Teleport und Holen sind Server-Aufrufe mit Instanzwechsel wie heute.
- **Ebenen und UiState:** TEAM-Seite 40 (`hub.team.*` in P, `page.team.*` in B und A), Dialoge 50, Baukasten-Modal im Match 50 (`servermenu`), Toasts 70. Kennungen: `.mod.reports` · `.mod.players` · `.mod.chat` · `.mod.replays` · `.mod.sanctions` · `.account.overview` / `.currency` / `.inventory` / `.progress` / `.maps` / `.social` / `.sanctions` / `.purchases` / `.support` / `.log` · `.economy.shop` / `.board` / `.gift` / `.stats` · `.live.instances` / `.maintenance` / `.flags` / `.stage` · `.dev.tools` / `.overlay` / `.logs` · `.admin.roles` / `.staff` / `.audit` / `.security` / `.approvals`.
- **Atlanten:** neue Icons in `ui_icons`; `frame_staff_header`, `divider_staff`, `frame_diff_preview`, `frame_data_table` und `btn_minus` in `ui_core`; `pill_staff_status` in `ui_hud`.

**Server-Aufrufe** (Namen als Vorschlag; jeder schreibende Aufruf mit `preview` und Ausführen wie oben)

| Bereich | Aufrufe |
|---|---|
| Sitzung, Suche | `staff.session` (Rolle, Rechte, Kategorien, Zähler) · `staff.search` · `staff.recent` · Push `staff.permissionsChanged` |
| Moderation | `mod.reports.list` / `.get` / `.resolve` · `mod.players.search` / `.sanction` · `mod.chat.subscribe` / `.unsubscribe` / `.delete` · `mod.replays.search` · `mod.sanctions.list` |
| Konto-Akte | `account.get` · `account.notes.add` · `account.currency.adjust` · `account.transactions.list` / `.revert` · `account.inventory.list` / `.give` / `.revoke` / `.setExpiry` / `.setUpgrade` / `.undoDisassemble` · `account.loadout.reset` · `account.progress.setXp` / `.setMastery` / `.setAchievement` / `.missions` / `.setLoginStreak` / `.resetTutorial` / `.setBoard` · `account.maps.setSlot` / `.moderate` / `.builders` · `account.social.get` / `.clanKick` / `.clanTransferLead` · `account.mail.sendAsTeam` · `account.sanctions.list` / `.create` / `.lift` · `account.purchases.list` / `.refund` · `account.tickets.list` / `.reply` · `account.audit.list` |
| Wirtschaft | `economy.shop.list` / `.update` / `.offer` / `.featured` · `economy.board.get` / `.update` / `.newSeason` · `economy.massGift.preview` / `.submit` · `economy.stats` |
| Live-Betrieb | `live.instances.list` / `.join` / `.spectate` / `.message` / `.restart` / `.close` · `live.maintenance.list` / `.schedule` / `.cancel` · `live.flags.list` / `.set` · Bühne über die heutigen Aufrufe von `StageMenu` |
| Entwicklung | heutige Aufrufe des Entwickler-Menüs · `dev.logs.request` / `.list` (das Debug-Overlay ist rein lokal) |
| Verwaltung | `admin.roles.set` · `admin.permissions.get` / `.set` · `admin.staff.list` · `audit.list` / `.export` · `admin.security.get` / `.set` · `approvals.list` / `.approve` / `.reject` / `.withdraw` |
| Werkzeuge | `staff.vanish` · `staff.freecam` · `staff.teleportTo` · `staff.summon` |

---
## 4. Kleines Esc-Menü & Bauplatz-Fenster
Auf Bauplatz (B), Asset-Karte (A) und im Match (M) öffnet Esc bzw. Gamepad-Start ein kompaktes Menü über dem leicht geblurrten Spiel (**NEU**). Es hat den gleichen Look wie der Hub und ersetzt das alte Esc-Menü (`MenuPanel`) außerhalb der Plaza. UiState-Kennung `menu` (wie heute).

### 4.1 Einträge je Modus

| Eintrag (alt → neu) | M | B | A | Ziel / Bedingung |
|---|---|---|---|---|
| „WEITER“ → ZURÜCK INS SPIEL (**NEU**-Text) | ● | ● | ● | Menü zu; Fokus beim Öffnen |
| „Bauplatz verwalten“ → BAUPLATZ VERWALTEN | – | ● | – | Bauplatz-Fenster (4.5); wie heute nur B |
| Rollen-Menüs (roter Marker) → TEAM (**NEU**-Text) | – | ● (**NEU**) | ● | TEAM-Seite (Einzelseite `page.team`); nur Staff (3a) |
| **NEU** TEAM-WERKZEUGE | – | ● | ● | Unterliste UNSICHTBAR (Schalter) · FREIE KAMERA · TELEPORT ZU SPIELER … · SPIELER HOLEN … (Namensfeld mit Vorschlägen); nur Staff, je nach Rolle (3a.2.7, 3a.3); Zeilen mit roter Akzentlinie |
| „Freunde und Gruppen · n online · n neu“ → SOZIAL · n online · n neu (**NEU**-Text) | – | ● | ● | Sozial-Panel (Ebene 42); im Match kein Sozial, wie heute |
| „Foto-Modus“ → FOTO-MODUS | – | ● | – | Foto-Modus (im Match nur über die Taste P als Geist/Zuschauer, wie heute) |
| EINSTELLUNGEN | ● | ● | ● | Einstellungen; SCHLIESSEN kehrt ins Menü zurück |
| „Hilfe und Support · neue Antwort“ → HILFE UND SUPPORT · neue Antwort | ● | ● | – | Schalter; öffnet Hilfe und Support als **eigenes Fenster** (Ebene 50), weil es außerhalb der Plaza keinen Hub gibt; der Punkt „neue Antwort“ steht am Eintrag und im Fenster am Ticket |
| „Fehler melden“ → FEHLER MELDEN | ● | ● | – | Schalter; dasselbe Fenster mit Kategorie „Fehler im Spiel“ |
| „ZUR PLAZA“ (im Match: Match verlassen) → MATCH VERLASSEN (**NEU**-Text, rot) | ● | – | – | **NEU** Bestätigung „Match verlassen?“ |
| ZUR PLAZA | – | ● | ● | Instanzwechsel zur Plaza (wie heute „außer Plaza“) |
| SPIEL BEENDEN (rot) | ● | ● | ● | **NEU** Bestätigung „Spiel beenden?“ |

● = sichtbar.
- Hilfe und Fehler melden fehlen auf A. Dort führen EINSTELLUNGEN › Allgemein › Hilfe (Support ÖFFNEN, Fehler melden MELDEN) zur selben Funktion.
- MEIN PROFIL entfällt im kleinen Menü (3.14 #3); das eigene Profil öffnet die eigene Zeile der Tab-Liste.
- „Zu Freunden wechseln“ liegt im Sozial-Panel › Plazas.

### 4.2 Kopfzeile je Modus

| Modus | Titel (`esc_header`, `display.m`) | Zeile darunter (`label`) |
|---|---|---|
| M | Map-Name (wie heute: Titel = Map-Name) | Modus · Runde/Zeit · Stand, z. B. „Entschärfung · RUNDE n/m · 1:23 · Blau 3 : 2 Rot“; Werte live wie im Match-Kopf; Phase „WARTERAUM“ / „BAUPHASE“ / „RUNDENENDE“ … |
| B | Map-Name | „SLOT n“ · „Bauplatz von X · n Spieler hier“ |
| A | Map-Name (Asset-Karte) | „n Spieler hier“ |

Die Spielerliste steht nicht im kleinen Menü; sie bleibt in der Tab-Liste (Kapitel 5).

### 4.3 Anatomie

```
 ┌───────────────────────────────┐   geblurrtes Spiel (Blur 6 px, Abdunkeln 35 %, bg_vignette)
 │ <MAP-NAME>                    │ ← esc_header (Höhe 88): Titel display.m, Zeile 2 label
 │ ENTSCHÄRFUNG · RUNDE 3/9 ·    │
 │ 1:23 · 3 : 2                  │
 ├───────────────────────────────┤
 │ ▶ ZURÜCK INS SPIEL            │ ← esc_row gold (Primär), Höhe 64, Fokus beim Öffnen
 │   EINSTELLUNGEN               │ ← esc_row
 │   HILFE UND SUPPORT        •  │ ← Punkt „neue Antwort“
 │   FEHLER MELDEN               │
 │ ───────────────────────────── │ ← divider_gold
 │   MATCH VERLASSEN             │ ← esc_row_danger
 │   SPIEL BEENDEN               │ ← esc_row_danger
 ├───────────────────────────────┤
 │ [Esc] Zurück   [Enter] OK     │ ← Tastenhinweise (key_plate; am Gamepad pad_b / pad_a)
 └───────────────────────────────┘
   Breite 480, links mit 96 Abstand vom Rand, vertikal zentriert (esc_panel)
```

| Teil | Regel |
|---|---|
| Position | links, vertikal zentriert; die rechte Bildhälfte bleibt frei, damit man das Spiel sieht. Bei schmaler Breite (10.3) zentriert. |
| Gruppen | Spiel-Aktionen oben, danach eine Trennlinie, dann die roten Einträge (Verlassen, Beenden) |
| Zeilen | Icon 32 links, Text button.m, Zähler rechts; Hover/Fokus: Gold-Tint, Lift 2 px, Pfeil ▶ |
| Blur | nur das Spielbild; das HUD darunter wird mit abgedunkelt. Im Match läuft das Spiel weiter (online), die eigene Figur nimmt keine Eingaben an, wie heute. |

### 4.4 Motion

| Vorgang | Eigenschaften | Dauer / Easing | Staffelung | Reduziert |
|---|---|---|---|---|
| Öffnen | Blur-Mischung 0 → 100 % (Blur 6 px, einmal berechnet), Abdunkeln 0 → 35 % | 240 ms outCubic | – | Abdunkeln ohne Blur-Animation, 90 ms |
| Öffnen: Panel | x −24 → 0 px, Deckkraft 0 → 1 | Feder „snappy“ (15.4) | – | nur Deckkraft, 90 ms |
| Öffnen: Zeilen | x −12 → 0, Deckkraft 0 → 1 | 160 ms outCubic | 24 ms je Zeile, max. 8 | keine |
| Hover/Fokus Zeile | Lift 2 px, Gold-Tint, ▶ gleitet 8 px ein | 90 ms outCubic | – | nur Tint |
| Schließen | alles rückwärts, ohne Staffelung | 160 ms inOutQuad | – | 90 ms Fade |
| Unterziel öffnen (z. B. EINSTELLUNGEN) | Menü bleibt im Stapel, Deckkraft → 0; Ziel öffnet mit eigener Animation | 160 ms | – | Fade |

### 4.5 Bauplatz-Fenster (B)
BAUPLATZ VERWALTEN öffnet das neu gestaltete Fenster `PlotPanel` (UiState `plot`, Ebene 40): Seitenleiste links (`sidebar_panel`), Inhalt rechts. Esc → kleines Menü.

| Seitenleiste | Inhalt (Inventar) | Knöpfe | Unterdialoge |
|---|---|---|---|
| Map-Slots | „MAP-SLOTS · n VON 6 FREIGESCHALTET“; Slot-Karten mit Vorschaubild | UMBENENNEN · ZURÜCKSETZEN · LADEN · ANLEGEN | „Slot n anlegen/zurücksetzen“: „VORLAGE“ (Flach 50 x 50, Flach 100 x 100, 50 x 50 mit 5 Lagen), „MATERIAL“ (Wiese, Wüste, Schnee, Stadt), ABBRECHEN / ANLEGEN bzw. ZURÜCKSETZEN · „Slot umbenennen“: Feld, ABBRECHEN / SPEICHERN |
| Himmel | „HIMMEL DIESER MAP“, 10 Karten: Klarer Tag, Morgenrot, Sommermittag, Bewölkt, Abendrot, Dämmerung, Sternennacht, Gewitterfront, Wüstenglut, Fremde Welt | Karte wählen | – |
| Mitbauer | „MITBAUER DIESER MAP · n VON 16 …“; Feld „Name eines Spielers (auch offline)“; Personenzeilen „Mitbauer · da/nicht da“, „Inhaber“, „Zu Besuch“ mit „•••“ (→ Spieler-Aktionen) | BAURECHT GEBEN · BAURECHT GEBEN/NEHMEN · RAUSWERFEN | – |
| Sprachchat | „SPRACHCHAT AUF DIESER MAP“, Chips „Nähe“ / „Map-weit“ | Chip wählen | – |
| Veröffentlichen (nur Inhaber) | `PublishPanel`: „NAME“, „BESCHREIBUNG“, Regler „PREIS FÜR DEN DOWNLOAD“ (Kostenlos … n Brix), Schalter „Als neue Version von „…““, „MODI · DIE MAP MUSS IHRE PFLICHT-ELEMENTE HABEN“ mit Chips je Modus „Bereit: …“ / „Fehlt: …“, Gebühren- und Rangzeile, Ergebnis-Box | VERÖFFENTLICHEN (das alte SCHLIESSEN ist Esc) | – |
| Bauvorlagen | öffnet das Bauvorlagen-Werkzeug (Taste X, **NEU**: rechts angedockt statt Fenster, weil ECKEN WÄHLEN die Welt braucht) und schließt das Fenster. Inhalt wie heute: „AUSWAHL“ (ECKEN WÄHLEN, KOPIEREN, LEEREN), „ZWISCHENABLAGE“ (EINFÜGEN, DREHEN n°, Chips Nicht gespiegelt / Spiegeln X / Spiegeln Z), „VERLAUF“ (RÜCKGÄNGIG (n), WIEDERHOLEN (n)), „SYMMETRIE“ (Chips Aus / X / Z / Vierfach), „ALS VORLAGE SPEICHERN“ (Name, Chip „In der Galerie teilen“, SPEICHERN), VORLAGEN-GALERIE, SCHLIESSEN | siehe Inhalt | – |
| Vorlagen-Galerie | `TemplatesPanel` wie 3.5, hier mit ÜBERNEHMEN | ÜBERNEHMEN · LÖSCHEN · TEILEN / NICHT TEILEN | – |

---

## 5. Tab-Liste
Eine Komponente für alle Modi (**NEU**; `tablist_frame`, Ebene 31). Sie fasst die alte Spielerliste (`PlayerListPanel`) und den Punktestand (`ScoreboardPanel`) zusammen. Rahmen, Kopfzeile, Zeilenstil, „•••“, Sprecher-Punkt und Anheften sind überall gleich; je Modus ändern sich nur Kopfzeile und Spalten.

### 5.1 Anatomie
```
 ┌──────────────────────────────────────────────────────────────┐
 │ PUNKTESTAND                         BLAU  3 : 2  ROT          │ ← Kopf: Titel + Score bzw. Untertitel
 │ Entschärfung · <Map> · Runde 5 / noch 1:23 · Ziel 7          │
 ├────────────────────────────┬─────────────────────────────────┤
 │ ZIEL PUNKTE K T A PING RANG │ ZIEL PUNKTE K T A PING RANG     │ ← Spaltenkopf (tablist_header_blue/red)
 │ ♛ [MOD] Name          •  ⋯ │ Name (aus)                   ⋯  │ ← tablist_row: Krone, Kennzeichen,
 │ ▌Du (eigene Zeile, gold)    │ …                               │   Name, Sprecher-Punkt, „•••“
 ├────────────────────────────┴─────────────────────────────────┤
 │ [Rechtsklick] Anheften · [Esc] Lösen                          │ ← Hinweiszeile
 └──────────────────────────────────────────────────────────────┘
```

### 5.2 Varianten je Modus

| Variante | Kopfzeile | Spalten | Besonderheiten |
|---|---|---|---|
| Plaza (P) | Titel = Map, Untertitel „n Spieler hier“ | Kennzeichen · Name „(du)“ · Rang · Party/Freund (Krone, Herz) · Sprecher · „•••“ | – |
| Asset-Karte (A) | wie Plaza | wie Plaza | Rollen-Abzeichen MOD/DEV/ADMIN/OWNER in den Kennzeichen |
| Bauplatz (B) | Titel = Map, Untertitel „Bauplatz von X · n Spieler hier“ | wie Plaza + Rolle „Inhaber“ / „Mitbauer“ / „Zu Besuch“ | „•••“ zeigt für den Inhaber den Block „BAUPLATZ“. |
| Match, Team-Modi | „Punktestand“, „Modus · Map · Runde/noch · Ziel“, Score „Team n : n Team“ | zwei Team-Spalten (Blau links, Rot rechts): ZIEL / PUNKTE / K / T / A / PING / RANG | Krone (Raumleiter), „(aus)“ für getrennte Spieler |
| Match, Jeder gegen jeden | „Punktestand“, Untertitel wie oben, dazu „Führung: X (n)“ | eine Rangliste: PLATZ / SPIELER / PUNKTE / K / T / A / PING / RANG | Platz 1–3 mit `medal_place_1–3` |
| Verteidigung / Zombie | „Punktestand“; Verteidigung mit „KERN n %“ und „WELLE n/m · n ÜBRIG“; Zombie mit Anzahl Infizierte/Überlebende | Team-Spalten wie Team-Modi; Zombie: Status je Zeile „INFIZIERT“ (roter Kopf) bzw. „ÜBERLEBT“ | Status-Symbol vor dem Namen, nie nur Farbe |
| Warteraum | – | – | Tab öffnet wie heute das Warteraum-Fenster (Kapitel 3.10). |

### 5.3 Gemeinsames Verhalten

| Verhalten | Regel |
|---|---|
| Anzeigen | Tab halten zeigt die Liste, Loslassen versteckt sie. Im Match wie heute; in P, B, A **NEU** statt Umschalten (Begründung 3.14 #6). Erscheint sofort, ohne Einblend-Verzögerung (15.2). |
| Anheften | Rechtsklick bei gehaltenem Tab heftet an (wie heute im Match; **NEU** auch in P, B, A). Gamepad: während des Haltens Gamepad-A. Angeheftet: Mauszeiger frei, Zeilen klickbar, UiState `tablist`. Esc oder Tab löst. |
| „•••“ | öffnet Spieler-Aktionen (Ebene 53). Im Match wie heute nur im angehefteten Zustand sichtbar; in P, B, A immer sichtbar und nach dem Anheften bedienbar (**NEU**, Folge von Halten statt Umschalten). |
| Zeile anklicken (angeheftet) | öffnet das Profil (wie heute in der Spielerliste; im Match **NEU**). Die eigene Zeile öffnet das eigene Profil im Eigen-Modus (Ersatz für MEIN PROFIL in B, A, M). |
| Sprecher-Punkt | grüner Punkt (`speaker_dot`) rechts am Namen, solange der Spieler spricht |
| Eigene Zeile | Gold-Tint und linker Goldbalken |
| Sortierung | Team-Modi nach PUNKTE, Jeder gegen jeden nach Platz, P/B/A alphabetisch mit Party oben |
| Werte | ändern sich sofort; eine geänderte Zelle blitzt 240 ms hell auf (Feedback ohne Verzögerung) |

---

## 6. Navigations-Flows
Wege in Schritten. P = Hub, sonst kleines Esc-Menü.

### 6.1 Match finden
**a) Schnellstart (P)**
1. Esc → Hub öffnet auf LOBBY.
2. Optional: Modus-Karte › WECHSELN → SPIELEN › Schnellspiel → Kanal-Segment und Modus-Kachel (oder „Alle Modi“) wählen → zurück in der LOBBY zeigt die Modus-Karte die Wahl.
3. SPIELEN drücken. Der Knopf zeigt Timer und ABBRECHEN, oben erscheint die Such-Pille. Als Party-Mitglied gilt die heutige Regel inkl. „Allein beitreten?“.
4. Hub schließen (Esc) ist erlaubt; die Such-Pille bleibt im HUD.
5. Treffer: „Server wird gestartet …“ → Instanzwechsel (Ladebildschirm „Instanz wird gewechselt“) → Warteraum bzw. Match.
6. Abbrechen: ABBRECHEN in der Such-Pille der Top-Leiste oder am SPIELEN-Knopf.

**b) Raum (P)**
1. Hub › SPIELEN › Server-Browser.
2. Kanal-Segment (Anfänger, Offen, Veteranen, Clan) und Modus-Auswahl setzen, AKTUALISIEREN.
3. Zeile wählen → BEITRETEN (bei „GESPERRT“ / „VOLL“ / „ENDET“ / „LÄUFT“ deaktiviert).
4. Schloss → Unterdialog „Passwort“ → BEITRETEN. In einer Party ggf. „Allein beitreten?“ → ALLEIN BEITRETEN.
5. Warten „Server wird gestartet …“ → Warteraum.
6. Alternativ RAUM ERSTELLEN → Ansicht „Raum erstellen“ („Raum“, „Spiel“, „MAP“) → RAUM ERSTELLEN → Warteraum als Master → MATCH STARTEN.

**c) Gewertet (P)**
1. Hub › SPIELEN › Gewertet.
2. Karte Team-Deathmatch oder Entschärfung → SUCHEN.
3. Die Such-Pille erscheint; SPIELEN und Gewertet tragen das Badge „Suche läuft“; die Karte zeigt SUCHE ABBRECHEN.
4. Hub darf zu sein; bei Treffer folgt der Instanzwechsel ins Match.

### 6.2 Replay ansehen als Spieler
Vier Einstiege, alle öffnen den ReplayViewer (Kapitel 19):
1. **KARRIERE › Replays & Highlights** (P): Chip Meine Replays / Highlights / Turnier-Replays → Karte → ABSPIELEN.
2. **KARRIERE › Match-Verlauf** (P): Zeile → REPLAY.
3. **Ergebnis › „Spielzug der Runde“** (M, nach dem Match): ANSEHEN (Clip); **NEU** „In Highlights“ speichert ihn unter KARRIERE › Replays & Highlights.
4. **SPIELEN › Turniere** (P): Segment „Beendet“ → Match → REPLAY (**NEU**).

Danach: Zeitleiste, ABSPIELEN/PAUSE, Tempo, NÄCHSTER KILL, Kamera-Modi; Esc schließt und kehrt zum Einstieg zurück. Live zuschauen geht über SPIELEN › Zuschauen, die Freundes-Zeile im Sozial-Panel (ZUSCHAUEN), Turniere (ZUSCHAUEN) und Clan-Kriege (ZUSCHAUEN).

### 6.3 Item kaufen & verschenken (Laden ↔ Post)
**Kaufen (P)**
1. Hub › LADEN › Empfohlen oder Katalog → Kategorie (z. B. Waffen) → Waffen-Filter → Karte.
2. Detail: Chip „LAUFZEIT“ (1 Tag, 7 Tage, 30 Tage, Dauerhaft) wählen.
3. KAUFEN · Preis → Unterdialog „KAUF BESTÄTIGEN“ (Guthaben, Ladekreisel) → JETZT KAUFEN.
4. Erfolg: Kauf-Animation (15.8), Abzeichen „BESITZ“, Guthaben-Pillen zählen herunter. Mit ABBRECHEN zurück zum Detail.

**Aus dem Laden verschenken**
1. Detail → VERSCHENKEN.
2. Sozial-Panel › Post (breite Seite) öffnet „Neue Nachricht“ mit dem Item unter GESCHENK.
3. AN, BETREFF, TEXT ausfüllen → SENDEN. Ablauf der Bezahlung wie heute.

**Aus der Post verschenken (P, B, A)**
1. Sozial-Panel › Post › NEUE NACHRICHT → AN, BETREFF, TEXT.
2. GESCHENK: AUS DEM INVENTAR (Overlay „Geschenk aus dem Inventar“, ZURÜCK) oder AUS DEM LADEN oder OHNE.
3. AUS DEM LADEN → Katalog im Geschenk-Modus mit Banner „Geschenk für X“ (nur in P; in B/A „Nur in der Plaza“ mit ZUR PLAZA, **NEU**).
4. Item wählen → VERSCHENKEN → zurück zur Nachricht mit dem Geschenk; ZURÜCK ZUR NACHRICHT oder Esc kehrt ohne Auswahl zurück.
5. SENDEN.

### 6.4 Map bauen & veröffentlichen
1. P: Hub › ERSTELLEN › Meine Maps → Slot-Karte → BETRETEN (Toast „Die Map wird vorbereitet.“) → Instanzwechsel auf den Bauplatz. Ein „Gesperrt“-Slot führt zu LADEN › Katalog › Map-Slots.
2. B: Bau-HUD (Kapitel 14). Brick 1–9 wählen, Q Palette, T Werkzeug, R drehen, X Bauvorlagen.
3. Neuer Slot: Esc → BAUPLATZ VERWALTEN → Map-Slots → ANLEGEN → „Slot n anlegen“ (VORLAGE, MATERIAL) → ANLEGEN.
4. Gestalten: Bauplatz-Fenster › Himmel (Karte wählen), Mitbauer (Name → BAURECHT GEBEN), Sprachchat („Nähe“ / „Map-weit“).
5. Vorschaubild: Esc → FOTO-MODUS → FOTO bzw. ALS VORSCHAUBILD (Inhaber).
6. Esc → BAUPLATZ VERWALTEN → Veröffentlichen (nur Inhaber): NAME, BESCHREIBUNG, PREIS FÜR DEN DOWNLOAD, ggf. „Als neue Version von „…““; die Modus-Chips müssen „Bereit: …“ zeigen → VERÖFFENTLICHEN → Ergebnis-Box.
7. Kontrolle in P: ERSTELLEN › Map-Galerie › Sortier-Chip „Eigene“.

### 6.5 Clan-Krieg herausfordern
1. P: Sozial-Knopf (oder F bzw. Gamepad-Y); B/A: Esc → SOZIAL.
2. Reiter Clan → breite Clan-Seite → CLAN-KRIEGE.
3. Block „HERAUSFORDERN“: Gegner-Kürzel, Start in Minuten, Teamgröße, Aufstellung, Chips „Spiel 1–3: Modus“ → HERAUSFORDERN. Wer herausfordern darf, entscheidet wie heute der Server.
4. Der Gegner sieht den Krieg in „KRIEGE“ → ANNEHMEN / ABLEHNEN; eigene Seite: ABSAGEN.
5. Zum Start: BEITRETEN; andere Mitglieder: ZUSCHAUEN (live im ReplayViewer; in B/A „Nur in der Plaza“).

### 6.6 Spieler melden
Alle Wege enden im Dialog „X melden“ (Ebene 52): „WAS MELDEST DU?“ (Spieler / Chat / Sprachchat), „GRUND“ (Schummeln, Belästigung, Anstößiger Name, Spam, Sprachchat-Missbrauch, Sonstiges), „DETAILS (FREIWILLIG)“ (bei Chat mit den letzten Zeilen vorbefüllt), MELDEN / ABBRECHEN.
1. Tab-Liste (alle Modi): Tab halten → Rechtsklick (anheften) → „•••“ → Spieler-Aktionen › „MELDEN“: SPIELER, CHAT oder SPRACHCHAT → Dialog mit vorgewählter Art.
2. Warteraum, Ergebnis-Tabelle, Bauplatz-Fenster › Mitbauer, ReplayViewer-Spielerliste (nur Live): „•••“ → wie 1.
3. In der Welt: „[E]   Profil von X“ → Profil-Popup → MELDEN.
4. Sozial-Panel: Freundes-Zeile → Profil → MELDEN.
5. Ohne Namen in Reichweite: Hilfe und Support → NEUES TICKET → Kategorie „Spieler melden“ (Ticket an den Support).

---

## 7. Welt: was entfällt
Plaza-Gebäude, Stationen und Portale gehören **nicht** zur UI. Sie sind Deko der Welt und bekommen keine UI-Spec: keinen Interaktionshinweis, kein Fenster, keinen Teleport. `StationView` (Stationsschild und -ring) hat in der Migration den Status `entfällt`. Alles, was früher nur über eine Station ging, läuft über den Hub (3.14 #1).

**Texte, die entfallen**

| Text (Inventar) | Wo heute |
|---|---|
| „Stationen direkt benutzen“ | Kopf des Esc-Menüs |
| „alle Stationen der Instanz (unfertige mit „(bald)“; Plaza-Portal ausgenommen)“ | linke Liste des Esc-Menüs |
| „[E]   \<Station\> - \<Hinweis\>“ | HUD-Hinweis unten Mitte |
| „Diese Station wird bald freigeschaltet.“ | Stations-Toast |
| Farbbalken, Titel, Hinweis bzw. „(bald)“; „leuchtet während der Einführung“ | `StationView` |
| „die Ziel-Station leuchtet“ | Einführung-Karte |
| „schließt auch mit E“ | Waffenständer |

**Welt-UI, die bleibt** (neuer Look, World-Space, nicht von der UI-Größe skaliert)

| Element | Klasse | Inhalt (Inventar) |
|---|---|---|
| Namensschild | NameTag | Name, Rollen-Abzeichen, Kennzeichen-Reihe (`UiNameBadges`), Sprech-Symbol; abschaltbar in den Einstellungen |
| Bühnen-Leinwand (P) | StageScreen | Folien alle ~8 s: Ankündigung, Saison, News, „Event läuft“ / „Event“, Map der Woche, Clan des Monats, die besten drei; Punkte-Reihe (dieselben Folien im LOBBY-Karussell) |
| Ziele im Match (M) | ModeWorldView | Flagge, Platten mit Buchstaben, Bombe, Stern über dem Gesuchten, Bauzonen-Rahmen, liegende Waffen |
| Schießstand-Ziele, Monster, Asset-Karte, Geister | RangeTargetsView · MonsterView · AssetMapView · GhostView | Zahl über dem Ziel „-n Zone“ (schwebende Schadenszahlen nur am Schießstand); Lebensleiste über angeschlagenen Monstern; Schilder und Überschriften der Asset-Karte; Geister hellblau |

**Texte, die bleiben oder umgeschrieben werden**

| Text | Neu |
|---|---|
| „[E]   Tür öffnen/schließen“, „[E]   Profil von X“, alle Match-Hinweise („Geschütz verlassen“, „\<Waffe\> aufheben“ …) | bleiben (`hud_interact_plate`) |
| „Die Map wird vorbereitet.“ | bleibt als Toast nach BETRETEN (ERSTELLEN › Meine Maps) |
| „Der Support hat auf dein Ticket … geantwortet. Esc → Hilfe und Support.“ | Karte „Der Support hat auf dein Ticket … geantwortet.“ mit ÖFFNEN (**NEU**). Die Chat-Systemzeile nennt den Weg je Ort: P „… Esc → ⚙ → Hilfe und Support.“ · B/M „… Esc → Hilfe und Support.“ · A „… Esc → Einstellungen → Allgemein.“ |
| Schritt-Texte der Einführung, die eine Station nennen | nennen den Hub-Weg, z. B. „Öffne Esc → SPIND → Aussehen“; der Ziel-Reiter bekommt einen Coachmark (**NEU**). Reine Welt-Schritte behalten „(noch x m)“. |
| „(bald)“ | Schloss + Etikett „BALD“ an Reiter oder Karte |
| „WEITER“ (Esc-Menü) | ZURÜCK INS SPIEL |
| „SCHLIESSEN führt zurück ins Menü“ (Einstellungen) | SCHLIESSEN führt dorthin zurück, woher man kam |
| „Zu Freunden wechseln“ | Sozial-Panel › Plazas (WECHSELN) |

---
## 8. Migration (67 Einträge)
Kurzfassung je Inventar-Eintrag. Die Zuordnung jedes einzelnen Knopf-Texts (`ui-label`), Unterdialogs, Zugangs, Modus und jeder Bedingung steht in **`data/ui_migration.csv`**; `python3 tools/check_ui_migration.py` prüft 67/67 Einträge und alle Knopf-Texte.
Status: `bleibt` (Ort gleich, neuer Look) · `verschoben` (neuer Ort) · `zusammengelegt` (mit anderem Eintrag vereint) · `aufgeteilt` (auf mehrere Orte verteilt) · `NEU-Teil` (bekommt einen neuen Teil) · `entfällt` (kein UI mehr).

| # | Bereich | Eintrag | Klasse | → neuer Ort | Status |
|---|---|---|---|---|---|
| 1 | Einstieg & System | Ladebildschirm, Anmeldung, Fehler | LoadingScreen | System-Screen (100), Fehlerkarte; ERNEUT VERSUCHEN-Regel bleibt | bleibt |
| 2 | Einstieg & System | Hinweise zu Sanktionen, Wartung, Support | kein eigenes Fenster | Toast + Chat-Systemzeile (70), Fehlerkarte im System-Screen, **NEU** Eintrag in der Glocke, Support-Antwort als Karte mit ÖFFNEN | NEU-Teil |
| 3 | Einstieg & System | Was ist neu | WhatsNewPanel | Popup-Warteschlange (58); **NEU** wieder aufrufbar in LOBBY › Neuigkeiten | NEU-Teil |
| 4 | Einstieg & System | Tägliche Belohnung | LoginRewardPanel | Popup-Warteschlange (P, Schalter) + Truhe in der LOBBY | aufgeteilt |
| 5 | Einstieg & System | Einführung | TutorialHud | HUD-Karte bleibt (13); Dialog in der Popup-Warteschlange (58) und über die LOBBY-Karte; **NEU** Coachmarks auf Hub-Reitern (41) | aufgeteilt |
| 6 | Einstieg & System | Wartungsstreifen | LiveHud | Wartungsband, **NEU** über allen Menüs (70) | NEU-Teil |
| 7 | Einstieg & System | Bühnen-Banner | StageHud | Benachrichtigungskarte (70); wartet weiter während einer Match-Runde | verschoben |
| 8 | Ingame-HUD | Basis-HUD | HudController | HUD (10); Toast → Toast-Ebene (70); Brick-Leiste → **NEU** Bau-HUD mit Werkzeugleiste (Kapitel 14); MissionsWidget nicht klickbar | NEU-Teil |
| 9 | Ingame-HUD | Kampf-HUD | CombatHud | Kampf-HUD (Kapitel 13); Zielfernrohr 9, Blendung 20 | bleibt |
| 10 | Ingame-HUD | Match-Kopf | MatchHud | HUD oben Mitte (12) | bleibt |
| 11 | Ingame-HUD | Ziele | ObjectiveHud | HUD-Marker (10) | bleibt |
| 12 | Ingame-HUD | Radar | RadarHud | HUD oben links (10) | bleibt |
| 13 | Ingame-HUD | Überleben | SurvivalHud | HUD (11), Kern-/Boss-Leiste im Stil von 13.6 | bleibt |
| 14 | Ingame-HUD | Party | PartyHud | Liste bleibt HUD (12); Einladungs- und Folgen-Karte → Benachrichtigungskarten (70); Party zusätzlich als Figuren in der LOBBY | aufgeteilt |
| 15 | Ingame-HUD | Foto-Modus | PhotoMode | Overlay (60); Zugang P-Taste, System-Dropdown (P), FOTO-MODUS im kleinen Menü (B) | bleibt |
| 16 | Menü & Navigation | Esc-Menü | MenuPanel | P: **NEU** Hub (Reiter, Top-, Fußleiste, System-Dropdown, Sozial-Knopf); B, A, M: **NEU** kleines Esc-Menü (WEITER → ZURÜCK INS SPIEL, ZUR PLAZA im Match → MATCH VERLASSEN) | aufgeteilt |
| 17 | Menü & Navigation | Spielerliste | PlayerListPanel | Tab-Liste, Varianten Plaza/Asset-Karte/Bauplatz (31) | zusammengelegt |
| 18 | Menü & Navigation | Funkrad | RadioMenu | Radial (33), Taste Z, M | bleibt |
| 19 | Menü & Navigation | Gamepad-Navigation | PadNavigator | Fokus-Ring auf allen Screens; **NEU** sichtbarer Fokus mit Fokus-Glühen, Belegung 3.13 | bleibt |
| 20 | Plaza-Stationen & Fenster | Laden | ShopPanel | LADEN › Katalog inkl. KAUF BESTÄTIGEN; VERSCHENKEN → Sozial › Post; Geschenk-Modus mit **NEU** Banner „Geschenk für X“; in B/A zeigt „AUS DEM LADEN“ „Nur in der Plaza“ (**NEU**) | verschoben |
| 21 | Plaza-Stationen & Fenster | Garderobe | WardrobePanel | SPIND › Loadout (**NEU**-Name für „Ausrüstung“) · Aussehen · Inventar · Werkstatt inkl. „\<Slot\> belegen“, Ergebnis, „ITEM ZERLEGEN“ | verschoben |
| 22 | Plaza-Stationen & Fenster | Arena / Räume | RoomBrowserPanel | SPIELEN › Server-Browser (Liste, Raum erstellen, Passwort, Warten, „Allein beitreten?“); SCHNELLSTART → LOBBY SPIELEN + Schnellspiel; GEWERTET/TURNIERE → Unterreiter | aufgeteilt |
| 23 | Plaza-Stationen & Fenster | Map-Galerie | MapGalleryPanel | ERSTELLEN › Map-Galerie; RAUM AUF DIESER MAP ERSTELLEN → „Raum erstellen“ mit vorgewählter Map | verschoben |
| 24 | Plaza-Stationen & Fenster | Waffenständer (Schießstand) | RangePanel | SPIND › Testgelände (**NEU**-Name, ohne Teleport); „schließt auch mit E“ entfällt | verschoben |
| 25 | Plaza-Stationen & Fenster | Glücksbrett | BoardPanel | LADEN › Glücksbrett | verschoben |
| 26 | Plaza-Stationen & Fenster | Bestenlisten | LeaderboardPanel | KARRIERE › Bestenlisten; Querverweise aus Profil, Gewertet, Clan bleiben (in B/A „Nur in der Plaza“, im Match ausgeblendet, **NEU**) | verschoben |
| 27 | Plaza-Stationen & Fenster | Gewertete Matches | RankedPanel | SPIELEN › Gewertet; Suche zusätzlich als **NEU** Such-Pille statt blockierendem Warten | verschoben |
| 28 | Plaza-Stationen & Fenster | Turniere | TournamentPanel | SPIELEN › Turniere; ZUSCHAUEN → SPIELEN › Zuschauen; **NEU** REPLAY an beendeten Matches | verschoben |
| 29 | Plaza-Stationen & Fenster | Clan: Kasse und Kriege | ClanWarPanel | Sozial-Panel › breite Clan-Seite (**NEU**: Seite statt eigenem Fenster) › Kasse und Stufe / Clan-Kriege (42); ZUSCHAUEN → SPIELEN › Zuschauen wie bei Turniere (in B/A „Nur in der Plaza“) | zusammengelegt |
| 30 | Plaza-Stationen & Fenster | Bühne | StagePanel | LOBBY (**NEU** Karussell, Event-Bonus-Chip) + Unterseite Neuigkeiten | zusammengelegt |
| 31 | Plaza-Stationen & Fenster | Hilfe und Support | SupportPanel | System-Dropdown (P), HILFE UND SUPPORT im kleinen Menü (B, M), Einstellungen › Allgemein; Ebene 50; im Match als eigenes Fenster; **NEU** „Screenshot anhängen“ nimmt das letzte Spielbild ohne Menü | verschoben |
| 32 | Bauen | Bau-Portal | MapPickerPanel | ERSTELLEN › Meine Maps / Mitbauen (P) | verschoben |
| 33 | Bauen | Bauplatz verwalten | PlotPanel | Bauplatz-Fenster über BAUPLATZ VERWALTEN (B) mit Map-Slots, Himmel, Mitbauer, Sprachchat, Veröffentlichen, Bauvorlagen, Vorlagen-Galerie | bleibt |
| 34 | Bauen | Map veröffentlichen | PublishPanel | Seite „Veröffentlichen“ im Bauplatz-Fenster (nur Inhaber) | zusammengelegt |
| 35 | Bauen | Bauvorlagen | BlueprintPanel | **NEU** rechts angedocktes Werkzeug (Taste X, 34) statt Fenster; Eintrag im Bauplatz-Fenster; Platz in der Werkzeugleiste | bleibt |
| 36 | Bauen | Vorlagen-Galerie | TemplatesPanel | Bauplatz-Fenster › Vorlagen-Galerie (B); **NEU** ERSTELLEN › Vorlagen (P, ohne ÜBERNEHMEN) | NEU-Teil |
| 37 | Bauen | Palette | BrickPalettePanel | Overlay (34), Taste Q, B; Platz in der Werkzeugleiste | bleibt |
| 38 | Match | Warteraum | WaitingRoomPanel | Vollbild (30), Tab-Variante „Warteraum“ | bleibt |
| 39 | Match | Punktestand | ScoreboardPanel | Tab-Liste, Varianten Team / Jeder gegen jeden / Verteidigung-Zombie (31) | zusammengelegt |
| 40 | Match | Ergebnis-Sequenz | ResultsSequence | Vollbild-Sequenz (45, über Ergebnis), Timeline 15.8 | bleibt |
| 41 | Match | Ergebnis | ResultsPanel | Vollbild (43, über dem kleinen Esc-Menü); **NEU** „In Highlights“ | NEU-Teil |
| 42 | Match | Zuschauen | SpectatePanel | SPIELEN › Zuschauen; **NEU** ZUSCHAUEN in der Freundes-Zeile (in B/A wie Clan-Kriege „Nur in der Plaza“) | verschoben |
| 43 | Match | Replay- und Zuschauer-Ansicht | ReplayViewer | Vollbild (46), **NEU** für alle Spieler (Kapitel 19); „•••“-Liste nur Live wie heute; Staff unverändert über TEAM › Replays und Baukasten-Effekt „Replay ansehen“ | NEU-Teil |
| 44 | Soziales & Profil | Freunde und Gruppen | SocialPanel | **NEU** Sozial-Panel (42) mit 6 Reitern, breiter Clan- und Post-Seite und allen Overlays; Querverweise in den Hub in B/A „Nur in der Plaza“ | verschoben |
| 45 | Soziales & Profil | Profil | ProfilePanel | eigenes: KARRIERE › Profil (P) bzw. Popup im Eigen-Modus (B, A, M); fremdes: Popup (51) mit allen Aktionsknöpfen, im Match POST/BESTENLISTEN aus (**NEU**) | aufgeteilt |
| 46 | Einstellungen | Grafik | Seite grafik | Einstellungen › Grafik; Abschnitt Barrierefreiheit → neuer Reiter Barrierefreiheit | aufgeteilt |
| 47 | Einstellungen | Sound | Seite sound | Einstellungen › Sound | bleibt |
| 48 | Einstellungen | Steuerung | Seite steuerung | Einstellungen › Steuerung (Tastenbelegung-Tabelle bleibt) | bleibt |
| 49 | Einstellungen | Controller | Seite controller | Einstellungen › Controller | bleibt |
| 50 | Einstellungen | Sprachchat | Seite sprachchat | Einstellungen › Sprachchat | bleibt |
| 51 | Einstellungen | Allgemein | Seite allgemein | Einstellungen › Allgemein; **NEU** UI-Größe | NEU-Teil |
| 52 | Rollen-Menüs | Baukasten | ServerMenuPanel | Renderer der TEAM-Seite mit neuen Skins für alle 8 Element-Arten; „Bist du sicher?“ (50); Chat-Befehle öffnen in B/A die TEAM-Seite, im Match den Baukasten als eigenes Modal (50), jeweils mit `[name]`; **NEU** Kategorien, Staff-Kopf, Suche, 12 Element-Arten, Sicherheitsregeln (3a) | NEU-Teil |
| 53 | Rollen-Menüs | Moderation | StaffMenus · /meldungen | TEAM-Seite › Moderation › Meldungen; **NEU** KONTO-AKTE ÖFFNEN, NEUE SANKTION; daneben **NEU** Chat-Live und Sanktions-Verlauf | NEU-Teil |
| 54 | Rollen-Menüs | Entwickler | StaffMenus · /entwickler, /asset-karte | TEAM-Seite › Entwicklung › Entwickler; daneben **NEU** Debug-Overlay und Client-Logs anfordern | NEU-Teil |
| 55 | Rollen-Menüs | Verwaltung | StaffMenus · /rolle | TEAM-Seite › Verwaltung › Rollen & Rechte (OWNER, ADMIN eingeschränkt); „XP setzen“ → Konto-Akte › Fortschritt; **NEU** Rechte-Matrix, Staff-Liste, Audit-Log, Sicherheit, Freigaben | NEU-Teil |
| 56 | Rollen-Menüs | Bühne | StageMenu · /buehne | TEAM-Seite › Live-Betrieb › Bühne (MOD wie heute); **NEU** Datum/Zeit für „Start“, DEV liest | NEU-Teil |
| 57 | Rollen-Menüs | Spieler | PlayersMenu · /spieler [name] | TEAM-Seite › Moderation › Spieler; **NEU** KONTO-AKTE ÖFFNEN (Konto-Akte, /akte [name]) | NEU-Teil |
| 58 | Rollen-Menüs | Replays | ReplaysMenu · /replays [name] | TEAM-Seite › Moderation › Replays | verschoben |
| 59 | Welt-UI | Namensschild | NameTag | Welt-UI im neuen Look (`hud_nametag_plate`, Rollen-Badges) | bleibt |
| 60 | Welt-UI | Stationsschild und -ring | StationView | – (Deko, kein UI) | entfällt |
| 61 | Welt-UI | Bühnen-Leinwand | StageScreen | Welt-UI im neuen Look; dieselben Folien im LOBBY-Karussell | bleibt |
| 62 | Welt-UI | Ziele im Match | ModeWorldView | Welt-UI im neuen Look | bleibt |
| 63 | Welt-UI | Schießstand-Ziele, Monster, Asset-Karte, Geister | RangeTargetsView · MonsterView · AssetMapView · GhostView | Welt-UI im neuen Look; Monster-Lebensleiste wie 13.6 | bleibt |
| 64 | Sonstiges & Overlays | Spieler-Aktionen | PlayerActionsPanel | Kontext-Popup (53); alle 6 Aufrufer bleiben (Tab-Liste, Punktestand, Warteraum, Ergebnis, Bauplatz-Mitbauer, Replay-Liste); **NEU** Block „TEAM“ mit KONTO-AKTE ÖFFNEN (nur Staff) | NEU-Teil |
| 65 | Sonstiges & Overlays | Melden | ReportPanel | Popup (52) | bleibt |
| 66 | Sonstiges & Overlays | Weitere Texte ohne eigenes Fenster | Toasts, Ablehnungen, Hilfsklassen | Toast-Komponente (70); Bau-Ablehnungen mit rotem Rand + Shake und Rot-Puls am Werkzeug; Stations-Toasts entfallen (Kapitel 7); Hilfsklassen bleiben | verschoben |
| 67 | Bausteine | UiFactory, EconomyUi, UiControls | Game/UI/UiFactory*.cs, EconomyUi.cs, UiControls.cs | Skin-Schicht mit Tokens (Kapitel 11, 12, 18); **NEU** Auto-Skalierung, Tween-Helfer, UI-Partikel | NEU-Teil |

Summe: 7 + 8 + 4 + 12 + 6 + 6 + 2 + 6 + 7 + 5 + 3 + 1 = **67**.

---

## 9. Canvas-Ebenen
Alle Canvases aus der Inventar-Tabelle „Canvas-Ebenen“ mit ihrer neuen Ebene, abgestimmt mit der Spalte `ebene_neu` in `data/ui_migration.csv`. In Unity gilt `sortingOrder = Ebene` (Kapitel 18).

### 9.1 Bänder

| Ebene | Inhalt |
|---|---|
| 9–13 | HUD: 9 Zielfernrohr · 10 Basis-HUD, Ziele, Radar, Bau-HUD · 11 Kampf-HUD, Überleben · 12 Match-Kopf, Party-Liste, Such-Pille (HUD), **NEU** Staff-Pille „UNSICHTBAR“ / „FREIE KAMERA“ · 13 Einführung-Karte |
| 20 | HUD-Effekte (Blendung) |
| 30–34 | Spiel-Overlays: 30 Warteraum · 31 Tab-Liste · 33 Funkrad · 34 Bau-Werkzeuge (Palette, Bauvorlagen-Werkzeug) |
| 40 | Hub (P), kleines Esc-Menü, Bauplatz-Fenster, TEAM-Einzelseite (B, A), System-Dropdown, Glocke-Verlauf |
| 41 | Coachmarks der Einführung (über dem Hub) |
| 42 | Sozial-Panel (Drawer) mit breiten Seiten |
| 43 | Ergebnis (über dem kleinen Esc-Menü, wie heute 42 > 40) |
| 44 | Einstellungen |
| 45 | Ergebnis-Sequenz (über Ergebnis, wie heute 44 > 42) |
| 46 | ReplayViewer (über Hub, Ergebnis und Ergebnis-Sequenz, wie heute 49) |
| 50–53 | 50 Dialoge, Hilfe und Support, Baukasten-Modal im Match · 51 Profil · 52 Melden · 53 Spieler-Aktionen |
| 58 | Popups / Belohnung (**NEU**: über den Einstellungen) |
| 60 | Foto-Modus (blendet Ebene 70 aus, außer den eigenen Toasts) |
| 70 | Benachrichtigungen, Toasts, Wartungsband (**NEU**: über den Menüs) |
| 100 | System-Screen |

### 9.2 Alt → neu (alle Canvases)

| Ord alt | Canvas / Klasse (Inventar) | Ebene neu | Anmerkung |
|---|---|---|---|
| 9 | Zielfernrohr (CombatHud) | 9 | |
| 10 | Hud (HudController mit VoiceHud, MissionsWidget) | 10 | Toast → 70; Brick-Leiste → Bau-HUD (10) |
| 10 | ObjectiveHud | 10 | |
| 10 | RadarHud | 10 | |
| 11 | CombatHud | 11 | teilt sich unten den Platz mit dem Bau-HUD (sofortiger Tausch, 14.6) |
| 11 | SurvivalHud | 11 | |
| 12 | MatchHud | 12 | |
| 12 | PartyHud | 12 | Karten siehe PartyHudTop |
| 13 | TutorialHud | 13 | Begrüßung → 58, Coachmarks → 41, LOBBY-Karte → 40 |
| 30 | Wardrobe | 40 | Hub › SPIND |
| 35 | WaitingRoom | 30 | |
| 35 | Blendung | 20 | |
| 36 | Palette | 34 | |
| 36 | Waffenständer | 40 | Hub › SPIND › Testgelände |
| 37 | Plot | 40 | Bauplatz-Fenster |
| 37 | MapPicker | 40 | Hub › ERSTELLEN |
| 38 | Scoreboard | 31 | Tab-Liste |
| 38 | Publish | 40 | Bauplatz-Fenster › Veröffentlichen |
| 38 | Blueprints | 34 | angedocktes Werkzeug |
| 39 | Templates | 40 | Bauplatz-Fenster bzw. Hub › ERSTELLEN › Vorlagen |
| 39 | LiveHud | 70 | **NEU** über den Menüs |
| 40 | Menu | 40 | Hub (P) bzw. kleines Esc-Menü |
| 40 | PlayerList | 31 | Tab-Liste |
| 40 | RadioMenu | 33 | |
| 40 | Spectate | 40 | Hub › SPIELEN › Zuschauen |
| 41 | ClanWar | 42 | Sozial-Panel › Clan-Seite |
| 41 | StageHud | 70 | Benachrichtigungskarte |
| 41 | PartyHudTop | 70 | Benachrichtigungskarte |
| 42 | Results | 43 | über dem kleinen Esc-Menü |
| 44 | Gallery | 40 | Hub › ERSTELLEN › Map-Galerie |
| 44 | Social | 42 | Sozial-Panel |
| 44 | ResultsSequence | 45 | über Ergebnis |
| 45 | Shop | 40 | Hub › LADEN |
| 45 | Board | 40 | Hub › LADEN › Glücksbrett |
| 45 | Leaderboard | 40 | Hub › KARRIERE › Bestenlisten |
| 45 | Rooms | 40 | Hub › SPIELEN |
| 45 | Ranked | 40 | Hub › SPIELEN › Gewertet |
| 45 | Tournaments | 40 | Hub › SPIELEN › Turniere |
| 45 | StagePanel | 40 | Hub › LOBBY › Neuigkeiten; Clan-Seite des Clans des Monats → 50 |
| 47 | ServerMenu | 40 / 50 | TEAM-Seite bzw. Einzelseite (40); im Match eigenes Modal (50); „Bist du sicher?“ → 50 |
| 47 | LoginReward | 58 | Popup-Warteschlange (**NEU** über den Einstellungen) |
| 47 | WhatsNew | 58 | Popup-Warteschlange (**NEU** über den Einstellungen) |
| 48 | Support | 50 | **NEU** über den Einstellungen; im Match eigenes Fenster |
| 49 | ReplayViewer | 46 | |
| 50 | Settings | 44 | |
| 51 | Profile | 51 | |
| 52 | Report | 52 | |
| 53 | PlayerActions | 53 | |
| 60 | PhotoMode | 60 | |
| 100 | LoadingScreen | 100 | |
| Welt | NameTag, StageScreen, ModeWorldView, RangeTargetsView, MonsterView, AssetMapView | Welt | World-Space, nicht von der UI-Größe skaliert |
| Welt | StationView | – | entfällt |
| – | **NEU** Bau-HUD · Such-Pille (HUD) · Coachmarks · Sozial-Panel · Popup-Warteschlange · Toast-Ebene | 10 · 12 · 41 · 42 · 58 · 70 | |

### 9.3 Reihenfolgen, die erhalten bleiben
- Zielfernrohr (9) < HUD (10–13) < Blendung (20) < alle Menüs (≥ 30)
- ReplayViewer (46) < Profil (51) < Melden (52) < Spieler-Aktionen (53)
- Einstellungen (44) < Profil (51)
- kleines Esc-Menü (40) < Ergebnis (43) < Ergebnis-Sequenz (45) < ReplayViewer (46)
- Warteraum (30) < Tab-Liste (31) (alt Warteraum 35 < Punktestand 38)
- Hub (40) < Sozial (42) < Einstellungen (44); Profil (51) < Foto-Modus (60) < System (100)

### 9.4 Bewusst geändert

| Änderung | Regel, damit sich das sichtbare Verhalten nicht ändert |
|---|---|
| Ergebnis-Sequenz (45) und ReplayViewer (46) liegen über den Einstellungen (44); alt lagen beide darunter (44 bzw. 49 < 50). | Endet ein Match, während die Einstellungen offen sind, wartet die Ergebnis-Sequenz, bis sie geschlossen sind. Aus dem ReplayViewer lassen sich die Einstellungen nicht öffnen. |
| Tab-Liste (31) liegt unter den Bau-Werkzeugen (34); alt lag die Spielerliste (40) über Palette (36) und Bauvorlagen (38). | Die Palette ist modal, Tab wirkt dort nicht. Solange die Tab-Liste gehalten wird, ist das angedockte Bauvorlagen-Werkzeug sofort ausgeblendet. |
| Wartungsband, Bühnen-Banner, Party-Karten, Toasts → 70 über allen Menüs (**NEU**) | gewollt: Hinweise bleiben sichtbar. Im Foto-Modus ist Ebene 70 aus, außer den eigenen Toasts („Foto gespeichert.“, „Das Bild ist zu groß für ein Vorschaubild.“). |
| Hilfe und Support (alt 48 < Einstellungen 50) → 50 über Einstellungen 44 (**NEU**) | Support öffnet aus den Einstellungen, ohne sie zu schließen. |
| Popups (alt 47 < Einstellungen 50 < Profil 51) → 58 (**NEU**) | Die Popup-Warteschlange wartet, solange Einstellungen, Dialoge, Profil, Melden oder Spieler-Aktionen offen sind. |
| Sozial (alt 44 > Ergebnis 42) → 42 < Ergebnis 43 | Sozial gibt es nicht im Match, Ergebnis nur im Match. |
| ServerMenu (alt 47 > Sozial 44) → TEAM-Seite 40 < Sozial 42 | Das Sozial-Panel ist ein Drawer über jeder Hub-Seite, also auch über der TEAM-Seite. |
| Toasts liegen über dem Foto-Modus (60). | FOTO rendert das Bild ohne UI-Canvases, Toasts landen nie im Foto. |

---

## 10. Skalierung & UI-Größe

### 10.1 Formel
- **Nur Desktop (PC)**, keine Handy-Ansicht. Unterstützt werden 1280×720 bis 4K in 16:9, 16:10, 21:9 und 32:9; kleinere Fenster werden nur verkleinert, nicht umgebaut.
- Referenz **1920×1080**.
- Auto-Faktor: `f_auto = clamp( sqrt( (W / 1920) · (H / 1080) ), 0.6, 2.0 )`. Das ist das geometrische Mittel aus Breiten- und Höhenfaktor, also genau das, was Unitys `CanvasScaler` (Scale With Screen Size, Match 0.5) rechnet, nur mit Begrenzung.
- Nutzer-Faktor `g` = UI-Größe: Klein **0.85** · Mittel **1.0** (Standard) · Groß **1.2**.
- Gesamt: `f = f_auto · g`. Logische Größe der Fläche: `W / f` × `H / f`.

| Auflösung | Seitenverh. | f_auto | Klein (f · logisch) | Mittel | Groß |
|---|---|---|---|---|---|
| 800×600 | 4:3 | 0.600 (begrenzt) | 0.510 · 1569×1176 | 0.600 · 1333×1000 | 0.720 · 1111×833 |
| 1024×768 | 4:3 | 0.616 | 0.523 · 1956×1467 | 0.616 · 1663×1247 | 0.739 · 1386×1039 |
| 1280×720 | 16:9 | 0.667 | 0.567 · 2259×1271 | 0.667 · 1920×1080 | 0.800 · 1600×900 |
| 1280×800 | 16:10 | 0.703 | 0.597 · 2143×1339 | 0.703 · 1821×1138 | 0.843 · 1518×949 |
| 1366×768 | 16:9 | 0.711 | 0.605 · 2259×1270 | 0.711 · 1920×1080 | 0.854 · 1600×900 |
| 1920×1080 | 16:9 | 1.000 | 0.850 · 2259×1271 | 1.000 · 1920×1080 | 1.200 · 1600×900 |
| 1920×1200 | 16:10 | 1.054 | 0.896 · 2143×1339 | 1.054 · 1821×1138 | 1.265 · 1518×949 |
| 2560×1080 | 21:9 | 1.155 | 0.981 · 2608×1100 | 1.155 · 2217×935 | 1.386 · 1848×779 |
| 2560×1440 | 16:9 | 1.333 | 1.133 · 2259×1271 | 1.333 · 1920×1080 | 1.600 · 1600×900 |
| 3440×1440 | 21:9 | 1.546 | 1.314 · 2618×1096 | 1.546 · 2226×932 | 1.855 · 1855×776 |
| 3840×2160 | 16:9 | 2.000 | 1.700 · 2259×1271 | 2.000 · 1920×1080 | 2.400 · 1600×900 |
| 5120×1440 | 32:9 | 1.886 | 1.603 · 3194×898 | 1.886 · 2715×764 | 2.263 · 2263×636 |

### 10.2 Safe Area
- `Screen.safeArea` begrenzt die Wurzel aller Screen-Space-Canvases (Steam Deck, Fernseher mit Overscan, Notch).
- Zusätzlich gibt es einen Innenrand: Hub und Menüs 48 logische px, HUD 24 logische px.
- Ultrabreit: Das HUD bleibt in einer 21:9-Spalte (logische Breite höchstens 2520 bei 1080 Höhe), damit Gesundheit und Munition im Blickfeld bleiben. Der Hub-Inhalt bleibt in einer Spalte von höchstens 2200 logischen px; Hintergründe, Blur und Leisten laufen über die volle Breite.

### 10.3 Breakpoints und Layout-Anpassungen
Gemessen wird an der logischen Größe nach UI-Größe; „Groß“ führt also bei 16:9 automatisch zu „Kompakt“.

| Stufe | Bedingung (logisch) | Anpassungen |
|---|---|---|
| Normal | Breite ≥ 1760 und Höhe ≥ 900 | Layout wie beschrieben |
| Kompakt | Breite 1440–1759 oder Höhe < 900 | Hub-Reiter werden zu Icons (`icon_tab_*`), ein Label nur am aktiven Reiter. Seitenleisten klappen zu Icon-Leisten (72 px) ein: SPIND-Vorschau, Bauplatz-Fenster, TEAM-Liste. Das Beschreibungs-Panel der Einstellungen erscheint als Zeile unter der fokussierten Einstellung. Raster 4 → 3 Spalten. Top-Leiste 64, Fußleiste 48. |
| Schmal | Breite < 1440 | dazu: Währungen werden zu einer Pille (Brix; Klick klappt alle auf). Das Sozial-Panel überdeckt den Inhalt in voller Höhe statt daneben, die breite Clan-/Post-Seite nimmt die volle Breite. Raster 2 Spalten. Das kleine Esc-Menü sitzt zentriert. Fußleiste zeigt nur Zurück und Auswählen. |
| Ultrabreit | Seitenverhältnis > 2.1 | Inhalts-Spalte und HUD-Spalte wie in 10.2 |

`UiFitBox` bleibt für Fenster und Dialoge: Passt ein Fenster nicht in die logische Fläche minus Ränder, wird es gleichmäßig verkleinert (höchstens bis 0.8). Reicht das nicht, scrollt der Inhalt; die Fußzeile mit der Primäraktion bleibt stehen.

### 10.4 UI-Größe als Einstellung
| Punkt | Regel |
|---|---|
| Ort | Einstellungen › Allgemein (Abschnitt „Anzeigen im Spiel“) und Einstellungen › Barrierefreiheit; beide Zeilen steuern denselben Wert |
| Werte | Klein (85 %) · Mittel (100 %, Standard) · Groß (120 %); Stufen-Slider mit 3 Knoten |
| Wirkung | multipliziert die Auto-Skalierung; gilt für alle Screen-Space-Canvases (Hub, Menüs, HUD, Tab-Liste, Bau-HUD, Toasts), nicht für World-Space-UI (Namensschild, Bühnen-Leinwand) |
| Übergang | **sofort**, ohne Übergangsanimation (ÄNDERUNG 4, 15.2). Die Einstellungs-Zeile bestätigt mit einem kurzen Gold-Puls am Wert. |
| Vorschau | Das Beschreibungs-Panel zeigt Hub und HUD als Miniatur in der gewählten Größe. |
| Unabhängig | Die Chat-Schriftgröße (pt) bleibt eine eigene Einstellung. |

### 10.5 Unity-Umsetzung
- **CanvasScaler:** Als Grundlage dient Scale With Screen Size, Referenz 1920×1080, Match 0.5. Weil `CanvasScaler` weder begrenzt noch einen Nutzer-Faktor kennt, setzt `UiScaler` (vorhanden, wird erweitert) auf allen Screen-Space-Canvases `uiScaleMode = ConstantPixelSize` und `scaleFactor = f` aus 10.1. Innerhalb von 0.6–2.0 und mit `g = 1` ist das Ergebnis pixelgleich zu Match 0.5. `UiScaler` hört auf Auflösungswechsel, Safe-Area-Änderung und die Einstellung UI-Größe und setzt den Wert im selben Frame.
- **Breakpoints:** `UiScaler` meldet die Stufe (Normal/Kompakt/Schmal/Ultrabreit) als Ereignis; Seiten schalten Varianten um (eigene Prefab-Varianten, keine Layout-Neuberechnung je Frame).
- **UiFitBox:** misst gegen logische Fläche minus Safe Area minus Innenrand.
- **Sprites:** alle UI-Sprites mit doppelter Auflösung (2×) erstellt, `Pixels Per Unit` 100, am `Image` `pixelsPerUnitMultiplier = 2`. So sind 9-Slice-Ränder bei f = 1 halb so groß wie die Textur und bleiben bis f = 2 scharf. Mipmaps aus, bilinear, Kompression BC7 (PC).
- **9-Slice-Regeln:** Rand ≥ Fase + Kontur + Lippe + 2 px (Werte je Asset in `data/ui_assets.csv`, Spalte `slice`). Die Mitte wird gestreckt (Fill Center); Verläufe nie kacheln. Die Panel-Textur `bg_panel_tile` liegt als eigenes gekacheltes Bild darunter. Kleinste Größe = linker + rechter Rand. Wird ein Teil kleiner gebraucht, nimmt man die kleinere Variante (`btn_gold_s` statt `btn_gold_m`), statt zu stauchen.
- **Glyphen und Text:** TextMeshPro mit SDF-Fonts (scharf in jeder Größe); Icons als 2×-Sprites, Mindestgröße 16 logische px.

---
## 11. Design-Tokens
Alle Werte gelten in logischen Pixeln bei 1920×1080 (Kapitel 10). Gemessene Farben stammen aus `ref/ui-asset-sheet.webp` (2000×1131 px).

### 11.1 Farben aus dem Sheet (gemessen)

| Token | Hex | Herkunft im Sheet | Einsatz |
|---|---|---|---|
| `bg.base` | `#00040A` | Hintergrund des Sheets | Grund hinter allem, Scrim |
| `bg.panel` | `#0B0B0D` | Fenster mit Chat-Feld, Karte | Fenster, Panels, Sozial-Panel |
| `bg.track` | `#0B0D0F` | Slider-Spur, inaktive Reiter, Balken-Spur | Spuren, Eingabefelder, inaktive Reiter |
| `gold.outline` | `#3A1400` | 2-px-Außenkontur der Platten | Kontur aller Gold-Teile |
| `gold.light` | `#FFD148` | Oberlicht der Platten | obere Lichtkante, Fokus-Ring |
| `gold.body` | `#FBB21D` → `#F9A50E` | Plattenkörper oben → unten | Verlauf aller Gold-Platten |
| `gold.inner` | `#C27200` | Innenlinie | Innenlinie der Platten |
| `gold.lip` | `#A85200` | Unterkante (3D-Lippe, ca. 5 px im Sheet) | Lippe |
| `state.normal` | `#FCAE0F` | Zustands-Spalte 1 | Knopf normal |
| `state.hover` | `#FFC21F` | Zustands-Spalte 2 | Hover / Fokus |
| `state.pressed` | `#C26D02` | Zustands-Spalte 3 | gedrückt |
| `state.disabled` | `#A76919` | Zustands-Spalte 4 | deaktiviert |
| `glyph` | `#562C00` | Glyphen der Icon-Knöpfe | Text und Icons auf Gold |
| `frame` / `frame.light` | `#AE5F00` / `#D4B55C` | Rahmen von Fenster, Karte, Prunkrahmen | Panel-Rahmen mit Lichtkante |
| `toggle.on` | `#192F01` | Toggle an (Spur) | Schalter an, Erfolg-Flächen |
| `danger` | `#7C1F17` | rote Quadrate | Gefahr-Knöpfe, Fehler-Flächen |
| `accent.heart` | `#D93233` | Herz | Freund-Herz, Gesundheit niedrig |
| `accent.potion` | `#1D7DBD` | Trank | Verbrauchsitems, Party |
| `accent.gem` | `#C71E15` | Kronen-Edelstein | Krone, Rang-Legende |

Eigene Nachmessung: Kontur `#341000`, Oberlicht `#FFD248`, Innenlinie `#BE7100`–`#C27100`, Lippe `#A84F00`–`#AF5D00`, gedrückt `#C26F02`, deaktiviert `#A7681B`. Die Abweichungen liegen in der Bildkompression; die Tokens oben gelten.

### 11.2 Abgeleitete Farben (Text, Zustände)
Kontrast berechnet nach WCAG 2.x gegen `bg.panel` `#0B0B0D`, sofern nicht anders angegeben.

| Token | Hex | Kontrast | Einsatz |
|---|---|---|---|
| `text.primary` | `#F4EBD9` (abgeleitet) | 16,6 : 1 | Fließtext, Titel auf Dunkel |
| `text.muted` | `#A8987A` (abgeleitet) | 7,0 : 1 | Untertitel, Beschreibungen |
| `text.disabled` | `#8C826F` (abgeleitet) | 5,2 : 1 | deaktivierte Zeilen |
| `text.gold` | `#FFD148` | 13,6 : 1 | Zahlen, Überschriften-Akzente (nie Fließtext) |
| `text.onGold` | `#562C00` | 6,4 : 1 auf normal · 7,4 : 1 auf hover · 3,1 : 1 auf gedrückt | Knopf-Text |
| `text.onGoldDisabled` | `#3A1F00` (abgeleitet) | 3,4 : 1 auf `state.disabled` | Knopf-Text deaktiviert |
| `danger.text` | `#E5533F` (abgeleitet) | 5,3 : 1 | Fehlertexte, „VOLL“, Gesundheit niedrig |
| `text.onDanger` | `#F4EBD9` auf `#7C1F17` | 8,6 : 1 | Text auf roten Knöpfen |
| `good.text` | `#8DBF3A` (abgeleitet) | 9,0 : 1 | „erledigt“, „Bereit: …“, Heilung |
| `text.onGood` | `#F4EBD9` auf `#192F01` | 12,2 : 1 | Text auf Erfolg-Flächen |
| `bg.raised` | `#16161A` (abgeleitet) | – | Hover-Zeilen, gehobene Flächen |
| `scrim` | `#00040A` mit 60 % | – | hinter Dialogen |
| `focus` | `#FFD148` + Glow `#FFC21F` 40 % | 13,6 : 1 | Fokus-Ring |
| `staff.line` (**NEU**) | `#AE4033` (ADMIN-Badge) | 3,4 : 1 (Grafik) | rote Akzentlinie aller Staff-Flächen (3a.6) |
| `staff.header` (**NEU**) | `#AE4033` → `#7C100B` (ADMIN-Badge) | `text.primary` darauf 5,0 : 1 (oben) bzw. 9,2 : 1 (unten) | Staff-Kopf der TEAM-Seite (3a.1) |

### 11.3 Rollen-Badges (unterste Reihe im Sheet)

| Badge | Farbe | Glyphe | Rolle | Asset |
|---|---|---|---|---|
| Krone | Bronze `#9C4D01` | goldene Krone | **OWNER (Inhaber)**, höchster Rang (**NEU**) | `role_owner` |
| Schild | Rot `#AE4033` → `#7C100B` | goldener Schild-Umriss | ADMIN | `role_admin` |
| `</>` | Lila `#7543A4` → `#3B116A` | helles `</>` | DEV | `role_dev` |
| Schild mit Haken | Grün `#66842E` → `#1E3A01` | goldener Schild mit Haken | MOD | `role_mod` |
| Person | Blau `#5C83A8` → `#15406C` | helle Büste | Spieler | `role_player` |

Das TEAM-Schild der Top-Leiste nutzt die rote ADMIN-Platte für alle Staff-Rollen. Der Staff-Kopf der TEAM-Seite (**NEU**, 3a.1) zeigt dagegen das eigene Rollen-Badge, damit jeder sieht, mit welcher Rolle er gerade arbeitet.

**OWNER (Inhaber, NEU):** höchster Rang über ADMIN. Sieht alle TEAM-Menüs und ist als einzige Rolle berechtigt, ADMIN oder OWNER zu vergeben (Verwaltung › „Rolle setzen“). ADMIN vergibt nur noch player, moderator und developer. Party-Leiter, Raum-Master, Clan-Leitung und Bauplatz-Inhaber bekommen kein Rollen-Badge, sondern die kleine Krone `icon_crown` vor dem Namen. So bleibt die Kronen-Platte eindeutig dem OWNER vorbehalten.

### 11.4 Stufen
Namen aus dem Glücksbrett. Eine Stufe erscheint nie nur als Farbe, sondern immer mit Name **und** Symbol (passt zur Farbseh-Einstellung).

| Stufe | Rahmen (Verlauf) | Textfarbe | Kontrast | Symbol | Assets |
|---|---|---|---|---|---|
| Gewöhnlich | Stahlgrau `#8E969F` → `#3E444B` (abgeleitet) | `#B4BAC2` | 10,1 : 1 | Kreis | `tier_frame_common`, `tier_sym_common` |
| Ungewöhnlich | Grün `#66842E` → `#1E3A01` | `#9CCB4A` (abgeleitet) | 10,4 : 1 | Raute | `tier_frame_uncommon`, `tier_sym_uncommon` |
| Selten | Blau `#5C83A8` → `#15406C` | `#7FB2E5` (abgeleitet) | 8,8 : 1 | Dreieck | `tier_frame_rare`, `tier_sym_rare` |
| Episch | Lila `#7543A4` → `#3B116A` | `#B58AE6` (abgeleitet) | 7,3 : 1 | Sechseck | `tier_frame_epic`, `tier_sym_epic` |
| Hauptgewinn | Gold `#FFD148` → `#FBB21D` | `#FFD148` | 13,6 : 1 | Krone | `tier_frame_jackpot`, `tier_sym_jackpot` |

### 11.5 Team-, Spiel-, Rang- und Währungsfarben
Deckt auch alle übrigen alten Farben ab (`RankColor`, Währungsfarben, Party-/Freund-/Leiter-Farben, Funkfarbe, Geister, Teamfarben); Zuordnung alt → neu in 18.2.

| Token | Fläche | HUD-Licht (aufgehellt, abgeleitet) | Kontrast HUD-Licht | Einsatz |
|---|---|---|---|---|
| `team.blue` | `#5C83A8` → `#15406C` | `#6FB0FF` | 8,7 : 1 | Teamscores, Tab-Liste Kopf Blau, Funk, Marker |
| `team.red` | `#AE4033` → `#7C100B` | `#FF7A6B` | 7,7 : 1 | Teamscores, Kopf Rot, Zombie „INFIZIERT“ |
| `ghost` | – | `#9FD8FF` (abgeleitet, „hellblau“ wie heute) | – | Geister, Status-Icon Geist |
| `hp` | `#D93233` → `#7C1F17` | – | – | Gesundheitsbalken (aus Herz und Gefahr) |
| `armor` | `#5C83A8` → `#15406C` | `#7FB2E5` | 8,8 : 1 | Rüstungsbalken |
| `heal` | `#8DBF3A` | – | 9,0 : 1 | Heil-Glanz |
| `chat.whisper` / `chat.party` / `chat.system` | – | `#B58AE6` / `#7FB2E5` / `#A8987A` | 7,3 / 8,8 / 7,0 : 1 | Chat-Zeilen; „[Funk] X: …“ in der Team-Licht-Farbe |
| `party` / `friend` / `leader` | `accent.potion` `#1D7DBD` / `accent.heart` `#D93233` / `gold.light` `#FFD148` | `#7FB2E5` / – / – | 8,8 : 1 | Party-Symbol und Party-Zeilen / Freund-Herz / Leiter-Krone (alte Party-, Freund-, Leiter-Farben) |
| `radio` | – | Team-Licht der eigenen Seite (`#6FB0FF` / `#FF7A6B`) | 8,7 / 7,7 : 1 | Funkfarbe („[Funk] X: …“, Funkrad, Funk-Sprecher) |
| `rank.t1` … `rank.t6` | Bronze `#9C4D01` · Silber `#B4BAC2` (abgeleitet) · Gold `#FCAE0F` · Medaille Gold + Band `#C71E15` · Stern `#FFD148` · Legende Gold + Edelstein `#C71E15` | – | – | Rang-Abzeichen `rank_t1`–`rank_t6` (alte `RankColor`) |
| `cur.brix` | `#FBB21D` | – | 10,5 : 1 | Brix (`cur_brix`) |
| `cur.splitter` | `#E8742A` (abgeleitet) | – | 6,5 : 1 | Splitter (`cur_splitter`) |
| `cur.kristalle` | `#6CC6F0` (abgeleitet) | – | 10,3 : 1 | Kristalle (`cur_kristalle`) |
| `cur.muenze` | `#FFD148` | – | 13,6 : 1 | Münze (`cur_muenze`) |

### 11.6 Typografie

| Token | Schrift | Größe / Zeile | Gewicht | Stil | Einsatz |
|---|---|---|---|---|---|
| `display.xl` | Barlow Condensed | 96 / 96 | 700 | GROSS, Laufweite +2 % | Ergebnis-Titelkarte, Countdown-Zahl |
| `display.l` | Barlow Condensed | 56 / 60 | 700 | GROSS | „RANG n!“, SPIELEN-Knopf, „AUSGESCHALTET“ |
| `display.m` | Barlow Condensed | 40 / 44 | 700 | GROSS | Seitentitel, Kopf des kleinen Menüs |
| `title` | Barlow Condensed | 28 / 32 | 700 | GROSS | Abschnitte, Kartentitel |
| `tab` | Barlow Condensed | 24 / 28 | 700 | GROSS, +4 % | Hub-Reiter |
| `button.l` / `.m` / `.s` | Barlow Condensed | 26 / 22 / 18 | 700 | GROSS, +3 % | Knöpfe L / M / S |
| `label` | Barlow Condensed | 16 / 20 | 600 | GROSS, +6 % | Spaltenköpfe, Etiketten, Tastenhinweise |
| `body.l` | Barlow | 20 / 28 | 500 | – | Beschreibungen, Dialogtext |
| `body` | Barlow | 18 / 26 | 400 | – | Listen, Fließtext |
| `body.s` | Barlow | 16 / 22 | 400 | – | Sekundärtext |
| `caption` | Barlow | 14 / 18 | 500 | – | Zeitstempel, Badges (Minimum) |
| `num.hud` | Barlow Condensed | 48 (Magazin, Gesundheit) / 28 (Reserve) | 700 | gleich breite Ziffern, 2 px Kontur `#00040A` | HUD-Zahlen |
| `num` | Barlow Condensed | wie Kontext | 600 | gleich breite Ziffern | Zähler, Preise, Tabellen |
| `mono` | JetBrains Mono | 14 / 18 | 400 | – | Replay-ID, Ticket-Nummer, „Version x   Protokoll y“ |

Mindestgröße 14 px (bei Klein 85 % entsprechend ≈ 12 Bildschirm-px bei 1080p). Gleich breite Ziffern in TextMeshPro über `<mspace=0.56em>` bzw. eine Font-Variante mit Tabellenziffern. Die Chat-Schriftgröße bleibt eine eigene Einstellung.

### 11.7 Abstände & Raster

| Token | Wert | Einsatz |
|---|---|---|
| `space.1` … `space.8` | 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 | alle Abstände sind Vielfache von 4 |
| Raster Hub | 12 Spalten, Abstand 24, Rand 48 | Seiten |
| Top-Leiste / Unterreiter / Fußleiste | 72 / 52 / 56 (Kompakt 64 / 48 / 48) | Hub |
| Knopf-Höhen | L 64 · M 48 · S 36 · Hero 112 | Platten |
| Icon-Knopf | 56 (klein 40) | Top-Leiste, Werkzeuge |
| Listenzeile | 56 (dicht 44) | Listen, Tab-Liste 40 |
| Karte | min. 240 × 300, Abstand 24 | Raster |
| Chip | Höhe 32, Innenabstand 12 | Filter |
| Klickfläche | mindestens 40 × 40 | alles Bedienbare |

### 11.8 Formsprache
Gemessen am Sheet (Sheet-Pixel):

| Element | Größe | Fase | Kontur | Oberlicht | Innenlinie (Abstand vom Rand) | Lippe |
|---|---|---|---|---|---|---|
| Platte groß (links, 2×3) | 212×118 | 12–13 | 2 px dunkel | 2 px | ≈ 10 | ≈ 5 |
| Platte Zustands-Raster (Mitte, 3×4) | 141×90 | 11 | 2 px | 2 px | ≈ 8 | ≈ 4–5 |
| Icon-Knopf | 110×108 | 13 | 2 px | 2 px | ≈ 10 | ≈ 4 |
| Rollen-Badge | 107×102 | 11 | 2 px | 1 px | farbige Innenfläche | ≈ 4 |
| rotes Quadrat | 73×78 | 9 | 2 px | 2 px | ≈ 9 | ≈ 3 |
| Karte mit Plakette | 174×266 | 10 | 2 px | – | Goldrahmen ≈ 6 | ≈ 4 |
| Fenster mit Chat-Feld | 518×348 | 9 | 2 px | Rahmen-Licht | Goldrahmen ≈ 6 | ≈ 4 |

Nieten: zwei kleine Punkte links und rechts auf Höhe der oberen Innenlinie (große und mittlere Platten).

Zur Laufzeit gilt: Fase ≈ 12 % der Höhe, Lippe ≈ 5 %, Innenlinie ≈ 9 %.

| Komponente | Höhe | Fase | Kontur | Innenlinie | Lippe | Nieten |
|---|---|---|---|---|---|---|
| Hero (SPIELEN) | 112 | 12 | 2 | 1 px, Abstand 8 | 5 | 2 |
| Platte L | 64 | 8 | 2 | 1 px, Abstand 6 | 4 | 2 |
| Platte M | 48 | 6 | 2 | 1 px, Abstand 5 | 3 | 2 |
| Platte S | 36 | 4 | 2 | – | 2 | – |
| Icon-Knopf | 56 / 40 | 7 / 5 | 2 | 1 px, Abstand 5 | 3 / 2 | – |
| Fenster, Panel, Sozial-Panel | – | 10 | 2 + Rahmen 4 (`frame`, Licht `frame.light`) | 1 px, Abstand 6 | – | 4 Ecken (nur Fenster) |
| Karte | – | 8 | 2 + Rahmen 3 | – | 3 | – |
| Chip, Etikett | 32 / 24 | 4 / 3 | 1–2 | – | – | – |
| Zähler-Badge | 20 | 3 | 1 | – | – | – |

### 11.9 Ebenen-Tiefe (Elevation)

| Stufe | Einsatz | Schatten (x / y / Weichheit, Deckkraft) | Hintergrund |
|---|---|---|---|
| e0 | Spuren, Innenflächen | – | – |
| e1 | Knöpfe, Platten | Lippe + 0 / 2 / 0, 25 % | – |
| e2 | Karten, Panels, HUD-Platten | 0 / 6 / 16, 45 % | – |
| e3 | Dialoge, Dropdowns, Sozial-Panel, kleines Esc-Menü | 0 / 12 / 32, 55 % | Scrim 60 % bzw. Blur |
| e4 | Popups, Belohnungen | 0 / 16 / 48, 60 % | Vignette + Strahlenkranz |

Schatten sind weiche 9-Slice-Sprites, nicht die Unity-Komponente `Shadow` (die verdoppelt die Vertices).

### 11.10 Fokus-Ring
- `frame_focus`: 2 px `gold.light` außen, 1 px `gold.outline` innen, Glow 8 px `#FFC21F` 40 %, 3 px Abstand, folgt der Fase.
- Sichtbar bei Gamepad- und Tastatur-Bedienung; bei Maus zeigt das Element nur Hover.
- Puls: Glow-Deckkraft 0,7 ↔ 1,0 in 1600 ms (inOutQuad), nur am fokussierten Element. Ohne Puls bei „Animationen reduzieren“.
- Fokus-Wechsel: Der Ring gleitet zum neuen Ziel (Position und Größe, 160 ms, Feder „snappy“), statt zu springen.

---

## 12. Komponenten-Katalog
Zustände: **N** normal · **H** hover · **G** gedrückt · **D** deaktiviert · **F** fokussiert · **A** ausgewählt. Asset-IDs aus `data/ui_assets.csv`.

### 12.1 Sheet → Komponente

| Sheet-Element | Komponente(n) | Assets |
|---|---|---|
| 6 große Platten (links, 2×3) | Platte L, SPIELEN-Hero, Karten-Grund | `btn_gold_l`, `btn_play_hero` |
| Platten-Raster Mitte: 3 Reihen × 4 Zustands-Spalten (normal, hover, gedrückt, deaktiviert) | Platten in **3 Größen** (L 64 · M 48 · S 36, 11.8) × **4 Zuständen**; Hero als vierte, größte Stufe. Dunkle und rote Varianten per eigener Datei, Zustände per Tint | `btn_gold_m`, `btn_gold_s`, `btn_dark_m`, `btn_red_m` |
| 15 Icon-Knöpfe: ▶ Abspielen · ❚❚ Pause · Zahnrad · Haus · ✕ · Wagen · Person · Brief · Pokal · Geschenk · ← · → · ↻ · i · ? | Icon-Knopf: ABSPIELEN/SPIELEN · PAUSE · System · ZUR PLAZA · Schließen · LADEN · Profil/Sozial · Post · KARRIERE/Bestenlisten · Geschenk/Tägliche Belohnung · ZURÜCK/Blättern · WEITER/Blättern · AKTUALISIEREN · Info/Beschreibung · Hilfe und Support | `btn_icon_square` + `icon_play`, `icon_pause`, `icon_settings`, `icon_close`, `icon_mail`, `icon_gift`, `icon_back`, `icon_forward`, `icon_refresh`, `icon_info`, `icon_help`, `icon_tab_*` |
| 2 Toggles (an: grüne Spur, Knopf rechts; aus: dunkle Spur, Knopf links) | Schalter | `toggle_track_on`, `toggle_track_off`, `toggle_knob` |
| Checkbox an / aus | Checkbox, Radio | `checkbox_on/off`, `radio_on/off` |
| Slider (Spur, Füllung, Knopf) | Slider | `slider_track`, `slider_fill`, `slider_knob` |
| Stufen-Slider (5 Knoten, großer Knopf) | Stufen-Slider (Qualitätsstufe, UI-Größe, Teamgröße) | `slider_node` |
| Schild-, Medaillen-, Stern-Abzeichen | Rang-Abzeichen, Erfolge | `rank_t1` … `rank_t6` |
| 4 rote Quadrate | Gefahr-Knopf, Limit-/Fehler-Zustand, Ablehnung | `btn_red_m`, Rot-Tint |
| Fenster mit Chat-Feld und Senden-Knopf | Fenster, Chat (HUD), Textfeld mit SENDEN | `frame_window`, `input_text` |
| Karte mit goldener Titel-Plakette | Karte, Modus-Karte, Fenstertitel | `card_item`, `plaque_title`, `frame_mode_card` |
| Prunkrahmen mit Rauten-Ornament | Hauptgewinn, Rang-Aufstieg, Werkstatt-Erfolg, Clan des Monats | `frame_ornate`, `frame_ornate_crest` |
| Reiter (1 aktiv gold, 2 inaktiv dunkel, Grundlinie) | Hub-Reiter, Unterreiter, Einstellungen-Kategorien, Sozial-Reiter | `tab_active`, `tab_inactive`, `tab_underline` |
| Fortschrittsbalken | Balken | `bar_track`, `bar_fill_*` |
| Knoten-Pfad (4 Knoten) | Fortschritts-Pfad: Einführung i/n, 7 Tage Belohnung, Turnierbaum | `path_node_*`, `path_link` |
| Ressourcen-Leisten mit Symbol und „+“ (Krone, Diamant, Blitz) | Währungs-Pille (Symbol je Währung), „+“ | `pill_resource`, `btn_plus`, `cur_*` |
| Banner schlicht · Band · Wimpel | Titel-Plakette, Ergebnis-/Geschenk-Banner, Platzierung | `plaque_title`, `reward_banner`, `reward_pennant` |
| Krone (roter Stein) · Diamant · Stern · Herz · Trank | Leiter-Krone · Kristalle · Sterne (Upgrade, Erfolge) · Freund-Herz · Verbrauch/Hotbar | `icon_crown`, `cur_kristalle`, `icon_star`, `icon_heart`, `icon_health` |
| 5 Rollen-Badges | Rollen-Badge, TEAM-Schild | `role_*` |

### 12.2 Komponenten

| Komponente | Anatomie | Zustände | Ersetzt (alt) |
|---|---|---|---|
| Fenster | `frame_window` + Titel-Plakette + Inhalt + Fußzeile (Statuszeile links, Aktionen rechts) | – | `UiFactory.Window` (Schatten + `UiFitBox`), `TopLabel`, Statuszeile |
| Panel / Innenfläche | `panel_inset`, gefast statt abgerundet | – | `UiFactory.Panel` (abgerundet), `Rect` |
| Dialog | `frame_dialog`, Titel, Text, 1–3 Knöpfe (Primär rechts, ABBRECHEN links), Scrim | – | `EconomyUi.Overlay`, Bestätigungsdialoge, „Bist du sicher?“, „Anzeige beibehalten?“ |
| Platte-Knopf L / M / S | Kontur, Oberlicht, Körper-Verlauf, Innenlinie, Lippe, Nieten (L, M), Text `button.*`, optional Icon links | N H G D F | `UiFactory.Button` (primär = gold) |
| Platte dunkel | `btn_dark_m`: `bg.track`, Rahmen `frame`, Text `text.primary` | N H G D F | `UiFactory.Button` (sekundär) |
| Platte rot | `btn_red_m`: `danger`, Text `text.onDanger` | N H G D F | Gefahr-Knöpfe (SPIEL BEENDEN, ENDGÜLTIG ZERLEGEN, CLAN AUFLÖSEN, SPERREN) |
| SPIELEN-Hero | `btn_play_hero`, Titel `display.l`, Unterzeile (Modus); im Suchzustand Timer + ABBRECHEN | N H G D F + Suche | SCHNELLSTART-Knopf |
| Icon-Knopf | `btn_icon_square` 56 mit Glyphe `glyph`, optional Badge oben rechts | N H G D F A | `UiFactory.Icon` (klickbar), `Chevron` |
| Rundknopf | `btn_round` | N H G D F | ABSPIELEN/PAUSE, FOTO |
| Schließen / Zurück | `btn_close`, `btn_back` 40 | N H G D F | SCHLIESSEN-Knöpfe in Ecken |
| Reiter | `tab_inactive` / `tab_active` + gleitender `tab_underline`, optional Icon (Kompakt) und Zähler | N H G D F A | `UiTab`, `UiFactory.Segment` (Kopfreiter) |
| Seitenleisten-Eintrag | vertikaler Reiter mit Icon + Text, aktiver Eintrag mit Goldbalken links | N H G D F A | `SidebarTab` |
| Chip / Segment | `chip_on` / `chip_off`, Text `label`, optional Zähler | N H G D F A | `EconomyUi.Chip`, `UiFactory.Segment` |
| Etikett | `badge_tag` (NEU, BALD + Schloss, BESITZ, AKTIV, „-n %“, HALL OF FAME, OFFIZIELL) | – | `UiFactory.Badge`, Symbol `Lock` |
| Zähler-Badge | `badge_counter` rot, Zahl bis „99+“, oder Punkt (8 px) | – | Zähler des Esc-Menüs und der Sozial-Chips |
| Textfeld / Suchfeld | `input_text` / `input_search`: Spur, Rahmen, Platzhalter `text.muted`, Lupe | N H D F + Fehler | `UiFactory.InputField` |
| Dropdown | `dropdown`: Wert + Pfeil, Liste als `frame_dropdown_menu` | N H G D F | Listen-Auswahl in Einstellungen |
| Stepper | `stepper_left` · Wert · `stepper_right` („< Wert >“) | N H G D F | `UiFactory.Stepper`, `UiStepper`, Baukasten-Select |
| Schalter | Spur `toggle_track_on/off`, Knopf `toggle_knob` | N H D F + an/aus | `UiFactory.Switch`, `UiSwitch` |
| Checkbox / Radio | 28 px, Haken in `glyph` | N H D F + an/aus | Mehrfach-/Einzelauswahl (Melden, Vorlage/Material) |
| Slider | Spur `bg.track`, Füllung Gold, Knopf 28×36, Wert rechts `num` | N H G D F | `UiFactory.Slider`, `UiSlider` |
| Stufen-Slider | Knoten `slider_node`, rastet ein | N H G D F | Qualitätsstufe, UI-Größe, Teamgröße |
| Einstellungs-Zeile | Titel links, Bedienelement rechts, Beschreibung im Panel rechts | N H D F | `SettingRow`, `InfoValue` |
| Tastenbelegungs-Knopf | `key_plate` mit Taste, Zustand „Taste drücken …“ | N H G F + wartet | `KeybindButton`, `UiKeybindButton` |
| Abschnittskopf / Trennlinie | `label` in `gold.light` + `divider_gold` | – | `SectionHeader`, `HorizontalLine` |
| Scroll-Ansicht | Maske + `scrollbar_thumb`, weiches Scrollen, Stick-Scroll | N H G | `ScrollView` |
| Balken | `bar_track` + `bar_fill_gold/xp/hp/armor`, optional Wert, Shimmer | – | `UiFactory.ProgressBar`, `EconomyUi.Bar/SetFill` |
| Stufen-Balken / Sterne | `bar_segment` bzw. `icon_star` | voll / leer | `EconomyUi.Steps`, Sterne, `StarRow` |
| Fortschritts-Pfad | Knoten + Verbindungen, erreicht = gold | leer / erreicht / aktuell | – (**NEU**) |
| Ring | `ring_track` + `ring_fill` (radial) | – | – (**NEU**: Timer, XP-Ring, Abklingzeit) |
| Ladekreisel | `spinner`, dreht linear | – | `UiFactory.Spinner` |
| Karte | `card_item` + `plaque_title`, Vorschau, Etiketten, Preis | N H G D F A | `EconomyUi.Card` |
| Item-Kachel | `tile_slot` + Item-Symbol + Stufen-Rahmen + Sterne + Etikett „AN“ | N H G D F A | `EconomyUi.ItemTile`, `ItemIcon` |
| Stufen-Anzeige | `tier_frame_*` + `tier_sym_*` + Name | – | `TierColor`, `TierName` |
| Laufzeit | Chip „LAUFZEIT“ bzw. Text „noch n Tage“, abgelaufen in `text.disabled` | – | `Lifetime`, Farbe `Expired` |
| Währungs-Pille | `pill_resource` + `cur_*` + Zahl (rollt), optional `btn_plus` | N H | `BalancePill`, Währungssymbole und -farben |
| Rang-Abzeichen | `rank_t1` … `rank_t6` + Zahl | – | `RankBadge`, `RankColor` |
| Profil-Chip | Rang-Abzeichen, Name, XP-Ring | N H G F | – (**NEU**) |
| Namens-Kennzeichen | Rollen-Badge (MOD/DEV/ADMIN/OWNER), Rang, „[TAG]“ mit Emblem, Party, Freund-Herz | – | `UiNameBadges` |
| Listenzeile | `list_row`: Avatar/Icon, Text, Werte, Zeilen-Knöpfe (S), „•••“ mit Sprecher-Punkt | N H G D F A | `PlayerActionsPanel.AddRowButton` |
| Vorschaubild-Fläche | gefaste Maske mit Rahmen, Ladeschimmer | lädt / da | `MapThumbnailCache.PlotPicture` |
| Emblem-Editor | 16×16-Raster, Palette, Werkzeuge Stift / Füllen / Spiegeln, LEEREN | – | `UiEmblemEditor` |
| Tooltip | `tooltip_box`, max. 320 breit | – | – (**NEU**) |
| Toast | `toast_plate`, Icon + Text, Ablehnung mit Rot-Tint + Shake | – | Toast im `HudController` |
| Benachrichtigungskarte | `notif_card`: Titel, Text, 1–2 Knöpfe, Timer-Ring | N H F | Party-Einladung, Folgen-Karte, Bühnen-Banner |
| Such-Pille | `pill_search`: Spinner, Modus, Timer mm:ss, ABBRECHEN | N H | – (**NEU**) |
| Tastenhinweis | `key_plate` bzw. `pad_a/b/x/y/lb/rb` + `label` | N H (klickbar) | – (**NEU**) |
| Fokus-Ring | `frame_focus` | – | `PadNavigator` (bisher unsichtbar) |
| Top-Leiste / Fußleiste | `bar_top_hub` / `bar_footer_hub` | – | Kopf und rechte Knöpfe des Esc-Menüs |
| System-Dropdown, Glocke-Verlauf | `frame_dropdown_menu`, Zeilen mit Icon | N H G F | – (**NEU**) |
| Kleines Esc-Menü | `esc_panel`, `esc_header`, `esc_row`, `esc_row_danger` | Zeile: N H G D F | `MenuPanel` außerhalb P |
| Sozial-Panel | `frame_social_panel`, Reiter-Chips, Listen, breite Seite | – | `SocialPanel` |
| Tab-Liste | `tablist_frame`, `tablist_row`, `tablist_header_blue/red`, `medal_place_*`, `speaker_dot` | Zeile: N H F + eigene | `PlayerListPanel`, `ScoreboardPanel` |
| Modus-Karte | `frame_mode_card` + `mode_*` + WECHSELN | N H F | – (**NEU**) |
| Party-Platz | `frame_party_slot`: Figur bzw. „+“, Krone, Name, Bereit-Haken | leer / belegt / bereit | – (**NEU**) |
| Modus-Kachel | `card_item` + `mode_*` | N H G D F A | Modus-Auswahl im Raumbrowser |
| Karussell | Folien 16:9 + Punkte-Reihe | – | Folien der Bühnen-Leinwand |
| Truhe | `reward_chest_closed/open` (2D) + Badge | zu / abholbar / offen | – (**NEU** in der LOBBY) |
| TEAM-Bausteine (**NEU**) | Staff-Kopf `frame_staff_header`, Akzentlinie `divider_staff`, Tabelle `frame_data_table`, Diff-Ansicht `frame_diff_preview`, Zahlenfeld mit `btn_minus`/`btn_plus`, HUD-Pille `pill_staff_status`; alle 12 neuen Baukasten-Elemente in 3a.6 | wie die Grund-Komponenten | `ServerMenuPanel`-Elemente |
| Coachmark | `frame_focus` um das Ziel + Pfeil `hud_offscreen_arrow` + Text-Plakette | – | Leuchten der Ziel-Station |
| Kampf-HUD-Teile | Gesundheit/Rüstung-Block, Status-Icon, Munitions-Panel, Waffen-Slot, Hotbar-Platz, Warn-Etikett, Schadensbogen, Trefferkreuz, Killfeed-Zeile, Lebensleiste, Ansage-Banner, Todesbildschirm | Kapitel 13 | CombatHud, MatchHud, SurvivalHud, ObjectiveHud, Symbole aus `.Combat`/`.Modes` |
| Bau-HUD-Teile | Brick-Platz, Werkzeug-Platz, Tasten-Etikett, Limit-Zähler, Statuszeile, Bauplatz-Info, Symmetrie-Anzeige, Abklingzeit-Ring | Kapitel 14 | Brick-Leiste im HudController |

### 12.3 Zustands-Matrix

| Zustand | Gold-Platte | Dunkle Platte / Zeile | Reiter / Chip | Karte / Kachel | Ton |
|---|---|---|---|---|---|
| N | `state.normal`, Lippe voll | `bg.track`, Rahmen `frame` | inaktiv dunkel, Text `text.muted` | Rahmen `frame` | – |
| H | `state.hover`, Lift −2 px, Glanz-Sweep | `bg.raised`, Rahmen `frame.light` | Text `text.primary`, Unterstrich-Vorschau 30 % | Lift −4 px, Rahmen `frame.light`, Glanz | `ui_hover` |
| G | `state.pressed`, Lippe 0, y + Lippenhöhe, Squash x 1,02 / y 0,94 (15.6) | `bg.base` | Scale 0,96 | Scale 0,98 | `ui_click` |
| D | `state.disabled`, Text `text.onGoldDisabled`, kein Hover; Klick → Shake | 50 % Deckkraft | 40 % Deckkraft, Schloss bei „BALD“ | Graufilter 60 %, Schloss | `ui_error` beim Klick |
| F | wie H + Fokus-Ring | wie H + Fokus-Ring | wie H + Fokus-Ring | wie H + Fokus-Ring | `ui_hover` |
| A | – (Knöpfe haben keinen Auswahlzustand) | Goldbalken links, Gold-Tint 12 % | `tab_active` gold bzw. `chip_on`, Text `glyph` | Goldrahmen 2 px + Haken | `ui_tab` bzw. `ui_select` |

### 12.4 Alle alten Bausteine → neu
Jeder Baustein aus dem Inventar-Anhang „Bausteine“ hat einen Platz:

| Alt | Neu |
|---|---|
| `CreateCanvas`, `Stretch/Place`, `Label`, `EconomyUi.Text`, `PixelImage` | bleiben als Hilfen; `CreateCanvas` setzt Ebene und `UiScaler`, `Label`/`Text` nutzen die TMP-Stile aus 11.6 |
| Farben `Accent`, `Surface`, `SurfaceLight`, `SurfaceSoft`, `TextPrimary`, `TextMuted`, `Danger`, `Good`, `Selected`, `TileColor`, `Expired`, `TierColor` | Tokens (Tabelle 18.2) |
| `.Match`: `Window`, `TopLabel`, `HorizontalLine`, `Segment`, `Badge`, `Icon`, `Spinner`, `ProgressBar`, Symbole `Lock`, `Crown` | Fenster, Titel-Plakette, Trennlinie, Chip/Reiter, Etikett, Icon-Knopf/Icon, Ladekreisel, Balken, `icon_lock`, `icon_crown` |
| `.Controls`: `SectionHeader`, `SettingRow`, `ScrollView`, `Slider`, `Switch`, `Stepper`, `InfoValue`, `KeybindButton`, `SidebarTab`, `Chevron` | Abschnittskopf, Einstellungs-Zeile, Scroll-Ansicht, Slider, Schalter, Stepper, Einstellungs-Zeile (Wert), Tastenbelegungs-Knopf, Seitenleisten-Eintrag, `icon_forward` |
| `.Economy`: `ItemIcon`, `RankBadge`, `RankColor`, Währungssymbole und -farben (Brix, Splitter, Kristalle, Münze), Sterne, `StarRow`, `PixelImage`, `BalancePill` | Item-Kachel, Rang-Abzeichen (`rank_t*`), `cur_*` + `cur.*`, `icon_star`, Stufen-Balken, Währungs-Pille |
| `.Combat` / `.Modes`: Waffen-, Kopftreffer-, Zielfernrohr-, Schadensbogen-, Schild-, Gesundheitssymbole; Flagge, Bombe, Kern, Ziel, Gesucht, Pfeil, Warnung, Ring, Zone, Totenkopf | `icon_headshot`, `hud_scope_mask`, `hud_damage_arc`, `icon_shield`, `icon_health`, `icon_flag`, `icon_bomb`, `icon_core`, `icon_target`, `icon_wanted`, `hud_offscreen_arrow`, `icon_warning`, `fx_ring`, Bauzonen-Rahmen, `icon_skull`; Waffensymbole aus dem Asset-Katalog |
| `.Social` / `.Voice`: Party/Freund/Leiter-Farben, Herz, Gruppe, Umschlag; Funkfarbe, Lautsprecher, Mikrofon, `LevelMeter` | `accent.potion` / `accent.heart` / `gold.light`, `icon_heart`, `icon_party`, `icon_mail`; Team-Licht, `icon_speaker`, `icon_mic`, Pegel-Balken (Balken mit 12 Segmenten) |
| `EconomyUi`: `Card`, `Chip`, `ItemTile`, `Overlay`, `Bar/SetFill`, `Steps`, `TierColor/TierName`, `Lifetime`, Farben `Selected` / `TileColor` / `Expired` | Karte, Chip, Item-Kachel, Dialog, Balken, Stufen-Balken, Stufen-Anzeige, Laufzeit, Tokens |
| `UiScaler`, `UiFitBox` | Kapitel 10 |
| `UiButtonSound` | Sound-Hooks (Kapitel 17) |
| `UiSwitch`, `UiSlider`, `UiStepper`, `UiTab`, `UiKeybindButton` | Schalter, Slider, Stepper, Reiter, Tastenbelegungs-Knopf (Verhalten bleibt, Skin neu) |
| `UiNameBadges`, `UiEmblemEditor` | Namens-Kennzeichen, Emblem-Editor |
| `PlayerActionsPanel.AddRowButton`, `MapThumbnailCache.PlotPicture`, `PadNavigator` | „•••“ mit Sprecher-Punkt, Vorschaubild-Fläche, Fokus-Ring |

---
## 13. Kampf-HUD
Gilt im Match (M) und am Schießstand der Plaza. Grundregel: **Spielzustände schalten sofort** (Werte, Waffe, Slot, Status). Effekte laufen danach und verzögern nie die Anzeige (15.2).

### 13.1 Layout (1920×1080, logisch)
```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│ ┌────────┐ <Map> | n Spieler | <Name>  ✉ 3          ┌────────────┐          Killfeed (≤ 5) │
│ │ RADAR  │ 144 FPS   23 ms Ping           BLAU  3   │ 1:23       │   2 ROT  X ⌖ ✱ Y        │
│ │  N  ·  │                                          │ RUNDE 3/9  │          A ⌖   B        │
│ └────────┘ 🎤 Team-Funk · Nähe                       └────────────┘                         │
│                                       WELLE 3/5 · 12 ÜBRIG  /  KERN 74 % ▬▬▬▬▬▬            │
│                                       BOSS: NAME 61 % ▬▬▬▬▬▬▬▬▬▬▬                ┌────────┐ │
│                                                                                  │Karten  │ │
│        ◄ Ziel-Marker am Rand                ▲ Platz A · 34 m                     │(≤ 2)   │ │
│                                                                                  └────────┘ │
│ ◜ Schadensbogen                         ─┼─  Fadenkreuz                     Schadensbogen ◝ │
│                                          ✕   Trefferkreuz                                  │
│                                 KOPFTREFFER  Name +100                                     │
│                                     NACHLADEN                                              │
│                                halten: Bombe legen · Platz A                               │
│ Chat (9 Zeilen)                                                                            │
│ …                                                                                          │
│ ┌ Status ⏱ ⏱ ⏱ ─────────────┐                                ┌ M4A1 · Sturmgewehr ─────┐ │
│ │ ⛨ 50 (25 %)  ▬▬▬▬▬▬░░░░░░ │                                │  30 / 120     Zoom: 2 St. │ │
│ │ ✚ 100        ▬▬▬▬▬▬▬▬▬▬▬▬ │                                │ [1][2][3][4]  [5][6][7][8]│ │
│ └───────────────────────────┘                                └──────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

| Zone | Inhalt (Inventar) | Komponente / Asset |
|---|---|---|
| oben links | Radar (M): Ringe, „N“, Reichweite „n m“, Pfeil für die eigene Figur, Punkte. Daneben Info-Leiste „\<Map\> \| n Spieler \| \<Name\>“ mit Post-Zähler, darunter FPS/Ping „n FPS   n ms Ping“ (je nach Einstellung), darunter VoiceHud-Pille | `hud_minimap_ring`, Basis-HUD |
| oben Mitte | Match-Kopf: Uhr, Teamscores links/rechts in Teamfarbe, Phase „WARTERAUM“ / „GLEICH GEHT'S LOS“ / „ERGEBNIS“ / „GLEICH“ / „BAUPHASE“ / „RUNDENENDE“ / „RUNDE n/m“; „Führung: X (n)“; Warte-Hinweis „Start in n s“ / „Warteraum“. Darunter Überleben (Kern-/Wellen-/Boss-Leiste) | `hud_score_plate`, 13.6 |
| obere Mitte | Countdown-Banner (große Zahl, „Das Match beginnt“, „LOS!“ mit Teamname oder „Viel Glück“), Ansage-Banner (auch „SEITENWECHSEL“), „DU BIST INFIZIERT“ / „Stecke die Überlebenden mit deinen Klauen an.“ | `hud_banner` |
| oben rechts | Killfeed: Schütze, Waffensymbol, Kopftreffer-Symbol, Opfer; höchstens 5 Zeilen, eigene Beteiligung mit Goldrand | `hud_killfeed_plate` |
| rechts unter dem Killfeed | Benachrichtigungskarten im Match (höchstens 2, ab y = 360), damit der Killfeed frei bleibt | `notif_card` (Ebene 70) |
| Mitte | dynamisches Fadenkreuz (Streuung; in der 3. Person am Treffpunkt), Trefferkreuz, Meldung „KOPFTREFFER“ / „AUSGESCHALTET“ / „ASSIST“ mit „Opfer +Punkte“, Nachladen-Hinweis, Aktionsbalken „Bombe wird gelegt · Platz X“ / „Bombe wird entschärft“, Hinweis unten Mitte („Geschütz verlassen“, „\<Waffe\> aufheben“, „MG-Geschütz bedienen“, „Kanone bedienen“, „halten: Bombe legen · Platz X“, „halten: Bombe entschärfen“, „Das Geschütz ist besetzt“), Träger-Hinweis „Du trägst die Flagge! …“, „FIEBER · …“ | `hud_crosshair_*`, `hud_hitmarker`, `hud_interact_plate` |
| Rand | Ziel-Marker in der Welt bzw. am Rand mit Pfeil (Flagge / „Flagge liegt“ / Träger, „Abgabe X“, „Platz X“, „Bombe“ / „Entschärfen …“, „Kern Blau/Rot n %“, „Gesucht: X“, mit Entfernung und Timer), Schadensbögen, Granatwarnung, Spawn-Schutz-Rahmen, Vignetten | `hud_objective_marker`, `hud_offscreen_arrow`, `hud_damage_arc`, `bg_vignette` |
| unten links | Chat (rückt über den Gesundheits-Block), Status-Leiste, Rüstung, Gesundheit | 13.2, 13.3 |
| unten rechts | Waffe, Magazin/Reserve, 4 Waffen-Slots, Hotbar 5–8 | `hud_ammo_panel`, `tile_slot` |
| eigene Canvases | Zielfernrohr (Ebene 9): Maske, roter Punkt, „Zoom n · xfach“; Blendung (Ebene 20): weißes Vollbild | `hud_scope_mask` |

### 13.2 Gesundheit & Rüstung (unten links)
Rüstung steht über der Gesundheit. Beide Zeilen haben Symbol, Zahl und Balken.

| Teil | Inhalt | Regel |
|---|---|---|
| Rüstung | Schild-Symbol `icon_shield`, „n (x %)“, Balken `bar_fill_armor` | Ohne Rüstung: Zeile grau mit „0“, Balken leer |
| Gesundheit | Kreuz-Symbol `icon_health`, große Zahl (`num.hud` 48), Balken `bar_fill_hp` für 100 HP | Zahl und Balken schalten sofort. |
| Schadens-Rest (**NEU**) | heller Balkenteil (`text.primary`, 70 %) zwischen altem und neuem Wert | steht 300 ms, schrumpft dann in 240 ms (outCubic) auf den neuen Wert; ein weiterer Treffer in der Haltezeit startet die 300 ms neu |
| Heilen (**NEU**) | grüner Glanz (`fx_shine_sweep` in `heal`) über den gewonnenen Bereich von links nach rechts | Wert sofort; Glanz 420 ms, inOutQuad |
| Rüstung bricht (→ 0) (**NEU**) | Splitter-Partikel (`fx_shard` in `armor`) ab dem Schild-Symbol, Schild-Icon blinkt 3× | Balken sofort leer; Blinken 3 × 90 ms an/aus; Sound `hud_armor_break` |
| Wenig Leben ≤ 25 % (**NEU**) | Balken pulsiert rot, rote Rand-Vignette pulsiert, Herzschlag | Puls 860 ms (≈ 70 Schläge/min), Füllung `hp` ↔ `danger.text`, Vignette (`bg_vignette` in `danger`) Deckkraft 0,15 ↔ 0,35 im selben Takt; Sound-Hook `hud_heartbeat` als Schleife, solange ≤ 25 % |
| Tod (0) | Todesbildschirm (13.7) | – |

### 13.3 Status-Leiste (über Gesundheit/Rüstung) (**NEU** als Leiste)
Buffs und Debuffs als kleine Icons (36 px) mit Restzeit-Ring (`ring_fill`, läuft linear ab). Ein neues Icon ist sofort voll sichtbar; als Feedback springt es von 1,15 auf 1,0 (Feder „pop“). In den letzten 3 s blinkt der Ring (2 Hz). Der Name steht 1,5 s unter einem neuen Icon und blendet dann aus.

| Status | Icon (Asset) | Quelle (Inventar) | Restzeit-Ring | Zusatz am Bildschirm |
|---|---|---|---|---|
| Tempo „SCHNELLER“ | `icon_speed` | Tempo-Item | ja | Text „SCHNELLER“ |
| Spawn-Schutz | `icon_shield` (gold) | Spawn-Schutz-Rahmen | ja | Rahmen am Bildschirmrand (13.5) |
| Überhitzt | `icon_heat` | „ÜBERHITZT“ | Abkühlung | Warnung am Magazin |
| Infiziert (Zombie) | `icon_skull` (grün) | „DU BIST INFIZIERT“ | – | grüne Vignette |
| Flagge tragen | `icon_flag` | „Du trägst die Flagge! …“ | – | Träger-Hinweis |
| Fieber (Freier Fall) | `icon_clock` | „FIEBER · …“ | ja | Hinweistext |
| Geist | `icon_eye` (`ghost`) | „Du bist ein Geist – nur andere Geister sehen und hören dich.“ | – | – |

Reihenfolge von links: Geist, Infiziert, Flagge, Spawn-Schutz, Fieber, Überhitzt, Tempo.

### 13.4 Waffe, Munition, Slots (unten rechts)

| Teil | Inhalt (Inventar) | Regel |
|---|---|---|
| Waffe | Name, Info, „Alternativfeuer: …“ / „Zoom: n Stufen“; ohne Waffe „KEINE WAFFE“ | Wechsel sofort; Feedback: der Name gleitet 8 px von rechts (90 ms), der Wert steht schon |
| Magazin / Reserve | Magazin groß (`num.hud` 48), Reserve klein (28); bei Wurfwaffen „Stück“, bei Hitzewaffen „Hitze“-Balken | Zahlen sofort; jeder Schuss lässt die Magazinzahl kurz auf 1,06 skalieren (60 ms) |
| Warnungen | „NACHLADEN“ / „KEINE MUNITION“ / „ÜBERHITZT“ | Etikett über dem Magazin (`badge_tag`, Rot-Tint bei KEINE MUNITION/ÜBERHITZT, Gold bei NACHLADEN), die Magazinzahl färbt sich mit; zusätzlich wie heute klein unter dem Fadenkreuz. Erscheinen sofort, pulsieren 2 Hz. |
| 4 Waffen-Slots | Taste 1–4, Anzahl | aktiver Slot gold und 6 px angehoben, sofort; Feedback-Bounce (Feder „pop“) |
| Hotbar 5–8 | 4 Verbrauchsitems mit Abklingzeit (`build_cooldown_ring`) und Anzahl | nur in Modi mit Gefahr („Hotbar – wirkt in Modi mit Gefahr“) |

### 13.5 Rand-Feedback

| Element | Darstellung | Timing |
|---|---|---|
| Trefferrichtung | rote Bögen (`hud_damage_arc`, `danger.text`) in Richtung des Schützen; Deckkraft nach Schaden 0,4–1,0 | erscheint sofort, steht 600 ms, verblasst in 400 ms |
| Treffer-/Kill-Marker | `hud_hitmarker`: weiß = Treffer, golden `#FFD148` = Kopftreffer, rot `#E5533F` = Kill | sofort voll sichtbar, Scale 1,3 → 1,0 in 90 ms, steht 160 ms, verblasst in 160 ms |
| Meldung | „KOPFTREFFER“ / „AUSGESCHALTET“ / „ASSIST“ mit „Opfer +Punkte“ | sofort; Slam 1,2 → 1,0 (120 ms outBack); steht 1,2 s; verblasst in 240 ms |
| Granatwarnung | Symbol `icon_grenade` + Pfeil am Rand in Richtung der Granate | solange in Reichweite; Puls 2 Hz |
| Spawn-Schutz-Rahmen | gold-weißer Rahmen 6 px am Bildschirmrand, Deckkraft 0,5 | solange der Schutz läuft; die letzten 2 s blinkt er |
| Zombie-Vignette | grüne Vignette | solange infiziert |

### 13.6 Weitere Lebensleisten (gleicher Stil wie Gesundheit, mit Schadens-Rest)

| Leiste | Ort | Inhalt (Inventar) |
|---|---|---|
| Kern | oben Mitte unter dem Match-Kopf (Verteidigung) | „KERN n %“; dazu „WELLE n/m · n ÜBRIG“ bzw. „WELLE n IN n s“; ≤ 25 % roter Puls |
| Boss | oben Mitte, 640 breit | „BOSS: NAME n %“ |
| Kern Blau/Rot | Ziel-Marker (ObjectiveHud) | „Kern Blau/Rot n %“ als Ring am Marker |
| Monster | Welt-UI über angeschlagenen Monstern (`MonsterView`), 96×10 | Lebensleiste |

### 13.7 Todesbildschirm
| Teil | Inhalt (Inventar) |
|---|---|
| Titel | „AUSGESCHALTET“ (`display.l`) |
| Detail | „von X · Waffe · Kopftreffer“ (Name, Waffensymbol, Kopftreffer-Symbol) / „Selbst erwischt“ / „Du bist ein Geist – nur andere Geister sehen und hören dich.“ |
| Countdown | „Wiedereinstieg in n“ / „Als Geist bis zum Ende der Runde“ / „Du schaust zu: X …“ / „Gleich geht es weiter“ |
| HUD | Waffenbereich und Gesundheit ausgeblendet; Status-Leiste zeigt ggf. Geist; Killfeed, Match-Kopf und Chat bleiben |

Der Screen erscheint sofort. Feedback: Bild abdunkeln auf 40 % (240 ms), Titel-Slam 1,15 → 1,0 (160 ms outBack), die Countdown-Zahl tickt mit kurzem Puls.

### 13.8 Schießstand, Bauphase, Bauplatz

| Situation | Sichtbar | Nicht sichtbar |
|---|---|---|
| Match, Kampf | alles aus 13.1–13.7 | Brick-Leiste, Werkzeugleiste |
| Match, Bauphase | Gesundheit, Rüstung und Status unten links; Brick-Leiste unten Mitte; Werkzeugleiste unten rechts **statt** Waffenbereich und Hotbar (sofortiger Tausch, kein Überblenden) | Waffenbereich, Hotbar, Waffen-Warnungen |
| Schießstand (P) | Fadenkreuz, Trefferkreuz, Waffenbereich, Schießstand-Karte rechts: „SCHIESSSTAND“, letzter Treffer (Zone, Schaden, m, Ziel, Waffe), Zonenzähler Kopfmitte / Kopf / Körper / Arm/Bein, „Spieler nehmen hier keinen Schaden.“; über den Zielen „-n Zone“ (Welt-UI) | Gesundheit, Rüstung, Hotbar (**NEU**, falls heute sichtbar: dort gibt es keinen Schaden, gleiche Regel wie Bauplatz) |
| Bauplatz (B) | Bau-HUD (Kapitel 14) | Gesundheit und Rüstung (keine Gefahr), Waffenbereich |

### 13.9 Zustände & Animationen (Kampf-HUD)

| Ereignis | Anzeige (sofort) | Feedback danach | Dauer / Easing | Reduziert | Sound |
|---|---|---|---|---|---|
| Schaden | Zahl + Balken neu | Schadens-Rest, Schadensbogen | 300 ms halten + 240 ms outCubic | Rest springt ohne Schrumpfen nach 300 ms | – (Treffer-Sound im Spiel) |
| Heilung | Zahl + Balken neu | grüner Glanz | 420 ms inOutQuad | aus | `hud_heal` |
| Rüstung bricht | Balken leer | `fx_shard` + Icon blinkt 3× | 270 ms | ohne Partikel und Blinken | `hud_armor_break` |
| Gesundheit ≤ 25 % | Balken rot | Balken- und Vignetten-Puls | 860 ms Schleife inOutQuad | statisch rot, Vignette 0,25 | `hud_heartbeat` (Schleife) |
| Status beginnt / endet | Icon da / weg | Pop 1,15 → 1,0 / – | Feder „pop“ | ohne Pop | `hud_status_on` |
| Waffenwechsel | neue Waffe, Slot gold | Slot-Bounce, Namen gleitet | Feder „pop“ / 90 ms | ohne | `hud_slot_switch` |
| Schuss | Magazin −1 | Zahl 1,06 | 60 ms | ohne | – |
| Magazin knapp / leer / überhitzt | Etikett + Farbe | Puls 2 Hz | Schleife | statisch | `hud_low_ammo` / `hud_no_ammo` / `hud_overheat` (einmalig) |
| Treffer / Kopftreffer / Kill | Trefferkreuz | Scale 1,3 → 1,0 | 90 ms + 160 + 160 | ohne Scale | `hud_hitmarker` / `hud_headshot` / `hud_kill` |
| Killfeed-Zeile | Zeile oben | ältere Zeilen rutschen nach unten | 160 ms outCubic | springen | – |
| Granate in Reichweite | Symbol + Pfeil | Puls 2 Hz | Schleife | statisch | `hud_grenade_warn` |
| Countdown / „LOS!“ | Zahl / Text | Slam 1,4 → 1,0 | 240 ms outBack | ohne Slam | `ui_countdown` / `ui_go` |
| Tod | Todesbildschirm | Abdunkeln, Titel-Slam | 240 / 160 ms | nur Abdunkeln | – |

---

## 14. Baumodus-HUD
Auf dem Bauplatz (B) und in der Bauphase im Match (M). Ersetzt die Brick-Leiste des Basis-HUD und bekommt eine eigene Werkzeugleiste (**NEU**).

### 14.1 Layout (1920×1080, logisch)
```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│ ┌ Bauplatz-Info (nur B) ─────────────┐                                                    │
│ │ <Map> · SLOT 2                     │                                                    │
│ │ Mitbauer da: 2 · Sprachchat: Nähe  │                                                    │
│ │ Symmetrie [X]   Auswahl 12×4×8     │  ← Auswahl-Info nur bei aktiven Bauvorlagen        │
│ └────────────────────────────────────┘                                                    │
│                                                                                            │
│                                         ·   (einfaches Fadenkreuz)                         │
│                                                                                            │
│ Chat (rückt über die Leisten)                                                              │
│          ┌──────── Rotstein · Linie · Norden · 37/200 ────────┐                            │
│          │[1][2][3][4][5][6][7][8][9]                          │  ┌ Werkzeuge ───────────────┐ │
│          │ 37/200 …   aktiv: gold, 8 px angehoben             │  │[T][R][◉][F][Q][X][Z|Y][+]│ │
│          └─────────────────────────────────────────────────────┘  └──────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────────────────┘
   In der Bauphase im Match: links unten zusätzlich Status/Rüstung/Gesundheit (13.8),
   oben der Match-Kopf mit „BAUPHASE“, keine Bauplatz-Info.
```

### 14.2 Brick-Leiste (unten Mitte)
| Teil | Inhalt (Inventar) | Regel |
|---|---|---|
| 9 Plätze | `build_slot` 64×64 mit Brick-Symbol, Ziffer 1–9 (`build_key_label`); Limit-Zähler „n/Limit“ (`build_limit_badge`) nur bei begrenzten Bricks | Wahl mit 1–9 oder Mausrad; der aktive Platz ist goldgerahmt und 8 px angehoben (72×72) |
| Statuszeile | nur der Brick-Name „\<Brick\>“, bei begrenzten Bricks „\<Brick\> · n/Limit“, auf `build_status_plate`. Werkzeug-Modus und Richtung zeigt die Werkzeugleiste (**NEU**: früher „\<Brick\> · Einzeln/Linie/Ersetzen · Norden/Osten/Süden/Westen · n/Limit“) | schaltet sofort mit jeder Änderung |
| Belegen | Palette (Q), Reihe „LEISTE“ mit 9 Plätzen (Ziffern 1–9 belegen) | wie heute |

**Palette** (`BrickPalettePanel`, Taste Q, nur B, Ebene 34): Suchfeld „Suchen …“; Seitenleiste Allgemein · Farbbox · Deko · Funktion · Zuletzt; Raster mit Limit-Abzeichen; Info-Karte (Name, Gruppe, „Drehbar …“, „Zerstörbar …“); Reihe „LEISTE“ mit 9 Plätzen (Ziffern 1–9 belegen); SCHLIESSEN (auch Esc bzw. Gamepad-B).

### 14.3 Werkzeugleiste (unten rechts) (**NEU**)
Eigene, etwas größere Leiste im gleichen Stil (`build_tool_slot` 72×72). Jede Taste zeigt die aktuelle Belegung aus Einstellungen › Steuerung, nicht fest.

| Platz | Taste (Standard) | Icon | Anzeige | Verfügbar |
|---|---|---|---|---|
| Werkzeug-Modus | T | `icon_tool_single` / `icon_tool_line` / `icon_tool_replace` | Symbol wechselt Einzeln / Linie / Ersetzen | B, M-Bauphase |
| Drehen | R | `icon_compass` | Kompass-Pfeil zeigt N / O / S / W | B, M-Bauphase |
| Brick aufnehmen | Mittelklick | `icon_pick` | kurzer Puls bei Aufnahme | B, M-Bauphase |
| Fliegen | F | `icon_fly` | an (gold gefüllt) / aus; nur mit Flug-Item aus dem Loadout | wie heute verfügbar |
| Palette | Q | `icon_palette` | aktiv, solange die Palette offen ist | B |
| Bauvorlagen | X | `icon_blueprint` | aktiv, solange das angedockte Werkzeug (**NEU**: rechts angedockt) offen ist | B |
| Rückgängig / Wiederholen | Z / Y | `icon_undo` / `icon_redo` | Zähler „n“ (wie „RÜCKGÄNGIG (n)“ / „WIEDERHOLEN (n)“); bei 0 deaktiviert | wie heute verfügbar |
| Bau-Werkzeuge | wie belegt | Item-Symbol | aus SPIND › Loadout „Werkzeug und Flug – wirkt auf dem Bauplatz“, mit Abklingzeit-Ring bzw. Anzahl | B |

Brick setzen (Linksklick) und entfernen (Rechtsklick) bzw. am Controller rechter/linker Trigger stehen als Hinweis in der Statuszeile, nicht als Platz.

### 14.4 Bauplatz-Info (oben links, nur B)
| Zeile | Inhalt |
|---|---|
| 1 | Map-Name · „SLOT n“ |
| 2 | Mitbauer da (Anzahl) · Sprachchat „Nähe“ / „Map-weit“ |
| 3 | Symmetrie-Anzeige `icon_sym_off` / `icon_sym_x` / `icon_sym_z` / `icon_sym_quad` (Aus / X / Z / Vierfach) |
| 4 | Auswahl-Info, nur wenn Bauvorlagen aktiv: Auswahl-Größe, Zwischenablage, „DREHEN n°“, Spiegeln (Nicht gespiegelt / Spiegeln X / Spiegeln Z) |

### 14.5 Zustände & Animationen (Bau-HUD)

| Ereignis | Anzeige (sofort) | Feedback | Dauer / Easing | Reduziert | Sound |
|---|---|---|---|---|---|
| Platz-Wechsel (1–9, Mausrad) | neuer Platz gold + angehoben, Statuszeile neu | kleiner Bounce 1,0 → 1,08 → 1,0 | Feder „pop“ | ohne Bounce | `hud_slot_switch` |
| Werkzeug-Modus (T) | Symbol neu, Statuszeile neu | Glanz über den Platz | 240 ms | ohne Glanz | `ui_toggle_on` |
| Drehen (R) | Kompass-Pfeil auf neuer Richtung | Puls am Platz | 160 ms | ohne Puls | `ui_select` |
| Fliegen an/aus (F) | Platz gold gefüllt / normal | `fx_glow_dot`-Puff | 300 ms | ohne Puff | `ui_toggle_on` / `ui_toggle_off` |
| Brick aufgenommen | Brick im aktiven Platz | 4 `fx_sparkle` | 300 ms | aus | `ui_select` |
| Rückgängig / Wiederholen | Zähler neu | Icon-Puls | 160 ms | ohne Puls | `ui_click` |
| Ablehnung (Bau-Ablehnungen, rund 20 Texte, z. B. „Dort ist schon ein Brick.“) | Toast mit rotem Rand | roter Puls am betroffenen Werkzeug (Rot-Tint 0 → 60 % → 0) + Toast-Shake ±4 px | 240 ms | Rot-Tint ohne Puls, Toast ohne Shake | `hud_build_reject` |
| Limit erreicht | Platz rot, Zähler „n/Limit“ rot | beim Setzversuch Shake ±4 px | 240 ms | ohne Shake | `hud_limit` |
| Bauphase beginnt / endet (M) | Kampf-HUD ↔ Bau-HUD **sofort** getauscht | – | 0 ms | – | Phase im Match-Kopf |

### 14.6 Kampf-HUD und Bau-HUD teilen sich unten den Platz
- Unten links bleiben im Match Gesundheit, Rüstung und Status in jeder Phase stehen.
- Unten Mitte ist im Kampf frei; in der Bauphase steht dort die Brick-Leiste.
- Unten rechts wechselt der Waffenbereich (inkl. Hotbar) beim Phasenwechsel **im selben Frame** mit der Werkzeugleiste. Es gibt kein Überblenden (ÄNDERUNG 4).
- Der Chat rückt über die jeweils höchste Leiste.

---
## 15. Motion-Spec
Ziel: ultra smooth und clean. Menüs bewegen sich weich und federnd, das HUD bleibt sofort und ruhig.

### 15.1 Leistungsregeln
| Regel | Umsetzung in Unity (uGUI) |
|---|---|
| Nur `transform`, `opacity`, `filter` animieren | `RectTransform.anchoredPosition` (als Offset), `localScale`, `localRotation`; `CanvasGroup.alpha` bzw. Vertex-Alpha; „filter“ = Material-Eigenschaften (Tint, Glanz, Glow, Graufilter, Blur-Mischung) an einem eigenen Material. Nie `sizeDelta`, Anker, Schriftgröße oder Layout-Werte animieren. |
| Keine Layout-Sprünge | Kein `LayoutGroup`/`ContentSizeFitter` auf animierten Elementen oder ihren Eltern während der Animation. Das Layout wird einmal gerechnet; die Animation verschiebt nur Offsets. Platz für erscheinende Elemente ist vorher reserviert. |
| Rebuilds klein halten | Bewegte Teile liegen auf einem eigenen Unter-Canvas („Motion-Canvas“) je Seite, statische Teile auf einem anderen; Zähler-Texte aktualisieren höchstens 30-mal/s. |
| 60 fps | Frame 16,7 ms. UI-Budget: CPU ≤ 2,0 ms (Canvas-Rebuild + Tweens + Partikel), GPU ≤ 1,5 ms inkl. Blur. Keine GC-Allokation pro Frame. |
| Blur günstig | Der Hintergrund wird beim Öffnen einmal in 1/4 Auflösung mit 2 Kawase-Durchgängen geblurrt; animiert wird nur die Überblendung scharf ↔ geblurrt, nicht der Radius. |
| Unabhängig von der Spielzeit | Menü-Animationen laufen mit `unscaledDeltaTime`. |
| Eingabe nie blockieren | Jede Animation ist unterbrechbar. Neue Eingabe springt die laufende Animation ans Ende (Endzustand), außer bei Belohnungs-Reveals, die mindestens 300 ms stehen. |
| Gleichzeitigkeit | höchstens 1 große Sequenz (Ergebnis, Belohnung) und 3 kleine Effekte zugleich; weitere warten |

### 15.2 Sofort-Regel für das HUD (ÄNDERUNG 4)
- **Spielzustände im HUD schalten sofort, im selben Frame:** Waffe, Werkzeug, Platzwechsel, HUD-Modus (Kampf ↔ Bau), Gesundheit/Rüstung, Munition, Status-Icons, Tab-Liste, Werte in Tabellen und die **UI-Größe**.
- Kleine Bestätigungs-Effekte (Bounce am aktiven Platz, Funken, Schadens-Rest, Glanz, Puls) sind erlaubt. Sie starten am sichtbaren Endzustand und **verzögern nie die Anzeige**: kein Einblenden aus 0 % Deckkraft, kein Hineinfahren, kein Überblenden zwischen HUD-Zuständen.
- Menüs (Hub, kleines Esc-Menü, Dialoge, Panels, Popups) behalten ihre Animationen.

### 15.3 Dauer-Tokens
| Token | Dauer | Einsatz |
|---|---|---|
| `motion.0` | 0 ms | HUD-Zustände (15.2) |
| `motion.xs` | 90 ms | Hover, Press, Farbwechsel, Trefferkreuz |
| `motion.s` | 160 ms | Schalter, Unterstrich, Zeilen, Schließen, Fokus-Ring |
| `motion.m` | 240 ms | Seiteninhalt, Dialog, Blur, Esc-Menü |
| `motion.l` | 420 ms | Hub öffnen, Sozial-Panel, Glanz-Sweep, große Reveals |
| `motion.xl` | 900 ms | Belohnungs-Sequenzen, Rang-Balken, Rang-Aufstieg |

### 15.4 Easings und Federn
| Easing | cubic-bezier | Einsatz |
|---|---|---|
| outCubic | `cubic-bezier(0.33, 1, 0.68, 1)` | Standard für Einblenden und Bewegen |
| outBack(1.4) | `cubic-bezier(0.34, 1.46, 0.64, 1)` (angenähert, Überschwinger ≈ 7 % wie die Formel mit s = 1,4) | Pops, Slams, Badges |
| inOutQuad | `cubic-bezier(0.45, 0, 0.55, 1)` | Schleifen (Puls, Fokus-Glühen), Schließen |
| linear | – | Spinner, Timer-Ringe, Strahlen-Drehung |

Federn (gedämpfte Feder, Masse 1; im CSS-Prototyp per JS-Feder oder `linear()`-Kurve nachgebildet):

| Feder | Steifigkeit | Dämpfung | Dämpfungsgrad | Überschwinger | Einschwingzeit (2 %) | Einsatz |
|---|---|---|---|---|---|---|
| `snappy` | 520 | 32 | 0,70 | 4,5 % | 250 ms | Panels, kleines Esc-Menü, Reiter-Unterstrich, Fokus-Ring |
| `pop` | 600 | 26 | 0,53 | 14 % | 308 ms | Badges, Dialog-Pop, Zähler-Puls, Slot-Bounce |
| `bouncy` | 380 | 18 | 0,46 | 19,5 % | 444 ms | Release-Bounce, Truhe, Belohnungen |
| `press` | 900 | 40 | 0,67 | 6 % | 200 ms | Rückfedern kleiner Wege (Schalter-Knopf, Chips) |
| `gentle` | 170 | 24 | 0,92 | 0,1 % | 333 ms | Sozial-Panel, breite Seiten, Karussell |

### 15.5 Staffelung
| Was | Versatz | Grenze |
|---|---|---|
| Listen-Zeilen | 24 ms je Zeile | höchstens 8 Zeilen (≤ 168 ms), der Rest gleichzeitig |
| Karten-Raster | 32 ms je Diagonale (Zeile + Spalte) | ≤ 240 ms |
| Hub-Reiter beim Öffnen | 20 ms je Reiter | 6 Reiter |
| Top-Leiste rechts | 16 ms je Element, von rechts | – |
| Kleines Esc-Menü | 24 ms je Zeile | 8 Zeilen |
| Party-Figuren | 80 ms je Platz | – |
| Ergebnis-Zähler | 120 ms je Zeile | – |
| Popup-Warteschlange | 300 ms Pause zwischen zwei Popups | – |

Gestaffelt wird nur beim ersten Erscheinen einer Ansicht, nicht beim Zurückkehren und nie bei „Animationen reduzieren“.

### 15.6 Button-Effekt-Stapel
Gilt für Gold-Platten (L, M, Hero); dunkle und rote Platten nutzen dieselben Phasen ohne Glanz-Sweep und ohne Funken.

| Phase | Auslöser | Eigenschaften und Werte | Dauer / Easing | Reduziert |
|---|---|---|---|---|
| Hover-Lift | Maus rein, Fokus | y −2 px (Karten −4 px), Schatten wächst | 90 ms outCubic | aus |
| Aufhellen | Hover | Tint `#FCAE0F` → `#FFC21F` | 90 ms outCubic | bleibt (Farbwechsel ohne Dauer) |
| Glanz-Sweep | Hover-Beginn, höchstens 1× je 1,2 s | `fx_shine_sweep`, 25° geneigt, additiv 35 %, x −120 % → +120 % der Breite, maskiert auf die Platte | 420 ms inOutQuad | aus |
| Press-Squash | Taste/Maus runter, Gamepad-A runter | Scale x 1,02 / y 0,94, y + Lippenhöhe, Lippe 100 % → 0 %, Tint `#C26D02` | 90 ms outCubic | nur Tint |
| Release-Bounce | Loslassen auf dem Knopf | zurück auf 1,0 mit Feder `bouncy` (schwingt kurz auf ≈ x 0,99 / y 1,03), Lippe zurück | ≈ 300 ms | sofort 1,0 |
| Fokus-Glühen | Gamepad-/Tastatur-Fokus | Ring gleitet zum Ziel (Feder `snappy`), Glow 0,7 ↔ 1,0 | 160 ms + 1600-ms-Schleife inOutQuad | statischer Ring |
| Klick-Funken | gültiger Klick auf Gold-Platte | 6–8 `fx_sparkle` ab Klickpunkt + kleiner `fx_ring` 0,6 → 1,4 | 320 ms | aus |
| Deaktiviert-Klick | Klick auf deaktiviert | Shake x ±4 px, 3 Schwingungen; Tooltip mit Grund | 240 ms | kein Shake, nur Ton + Tooltip |

### 15.7 Animationen je Fall

| Fall | Auslöser | Eigenschaften | von → nach | Dauer | Easing | Versatz | Reduziert |
|---|---|---|---|---|---|---|---|
| Hub öffnen | Esc/Start in P | Blur-Mischung (Blur 8 px, einmal berechnet), Abdunkeln | 0 → 100 %, 0 → 45 % | 240 ms | outCubic | – | Abdunkeln 90 ms |
| | | Top-Leiste y, Fußleiste y | −72 → 0, +56 → 0 | Feder `snappy` | – | 0 / 40 ms | Fade 90 ms |
| | | Reiter, Top-Leiste rechts | Deckkraft 0 → 1, y −8 → 0 | 160 ms | outCubic | 20 / 16 ms | – |
| | | Seiteninhalt | Deckkraft 0 → 1, y 24 → 0 | 240 ms | outCubic | 80 ms nach Start | Fade |
| Hub schließen | Esc/Gamepad-B oben | alles rückwärts, ohne Versatz | – | 160 ms | inOutQuad | – | 90 ms Fade |
| Reiterwechsel | Q/E, LB/RB, Klick | Unterstrich x und Breite; alter Inhalt; neuer Inhalt | gleitet; Deckkraft 1 → 0 und x 0 → −24; Deckkraft 0 → 1 und x +24 → 0 (Richtung folgt dem Reiter) | Feder `snappy`; 120 ms; 240 ms | – ; inOutQuad; outCubic | neuer Inhalt 60 ms später | harter Schnitt + Fade 90 ms |
| Unterreiter | 1–9, LT/RT | Unterstrich; Inhalt | gleitet; Deckkraft 0 → 1, y 12 → 0 | `snappy`; 160 ms | outCubic | – | Fade |
| Listen / Raster erscheinen | erstes Öffnen | Deckkraft, y | 0 → 1, 16 → 0 | 160 ms | outCubic | 15.5 | sofort |
| Dialog (Unterdialog) | Öffnen | Scrim; Box Scale, Deckkraft | 0 → 60 %; 0,92 → 1, 0 → 1 | 160 ms; Feder `pop` | outCubic | – | Fade 90 ms |
| Dialog schließen | Esc, Knopf | Box Scale, Deckkraft | 1 → 0,96, 1 → 0 | 120 ms | inOutQuad | – | Fade |
| Sozial-Panel | Öffnen / Schließen | x | +560 → 0 / 0 → +560 | Feder `gentle` / 240 ms | – / inOutQuad | Zeilen 24 ms | Fade |
| Breite Seite (Clan, Post) | Öffnen | Breite über Scale x der Maske + Inhalt | 560 → 1280 | 420 ms | outCubic | – | Schnitt |
| Dropdown (System, Glocke) | Klick | Scale y, Deckkraft | 0,9 → 1, 0 → 1 (Pivot oben) | 160 ms | outCubic | Zeilen 16 ms | Fade |
| Kleines Esc-Menü | Esc in B/A/M | siehe 4.4 | | | | | |
| Coachmark | Einführungs-Schritt | Ring, Pfeil | Scale 1,3 → 1, Pfeil wippt 8 px | Feder `pop`; 1200-ms-Schleife | inOutQuad | – | statisch |
| Tooltip | Hover 400 ms bzw. Fokus | Deckkraft, y | 0 → 1, 4 → 0 | 120 ms | outCubic | – | Fade |
| Fokus-Ring | Fokuswechsel | Position, Größe | gleitet | Feder `snappy` | – | – | springt |
| Schalter | Klick | Knopf x; Spur-Farbe | links ↔ rechts mit Überschwinger; `bg.track` ↔ `toggle.on` | Feder `pop`; 160 ms | – ; outCubic | – | springt |
| Slider | Ziehen / Fokus | Knopf Glow; Wert | Glow 0 → 1 beim Greifen; Füllung folgt direkt | 90 ms | outCubic | – | ohne Glow |
| Stufen-Slider | Einrasten | Knopf Scale | 1,15 → 1 | Feder `pop` | – | – | ohne |
| Checkbox-Haken | an | Haken zeichnet sich (Strich-Maske 0 → 100 %), Kasten Scale | 0 → 100 %, 0,9 → 1 | 160 ms; Feder `pop` | outCubic | – | sofort |
| Zahl rollt | Wertänderung in Menüs | Ziffern zählen hoch/runter | alter → neuer Wert | 600 ms (≤ 50 Schritte) | outCubic | – | sofort |
| Balken füllen | Wertänderung in Menüs | Füllung Scale x; Shimmer | alt → neu; `fx_shine_sweep` läuft einmal | 420 ms; 600 ms | outCubic; inOutQuad | – | sofort, ohne Shimmer |
| Zähler-Puls | Badge-Wert steigt | Scale | 1 → 1,25 → 1 + kleiner `fx_ring` | Feder `pop` | – | – | ohne |
| Toast | erscheint / geht | y, Deckkraft | +24 → 0, 0 → 1 / −8, 1 → 0 | Feder `snappy` / 160 ms | – / inOutQuad | – | Fade |
| Ablehnungs-Toast | erscheint | zusätzlich Shake x ±4 | – | 240 ms | – | – | ohne Shake |
| Benachrichtigungskarte | erscheint | x, Deckkraft; Timer-Ring | +48 → 0, 0 → 1; 100 % → 0 % | Feder `snappy`; Restzeit | – ; linear | – | Fade; Ring bleibt |
| Such-Pille | Suche läuft | Puls Glow; Spinner | 0,6 ↔ 1,0; Drehung | 1600-ms-Schleife; 1000 ms je Umdrehung | inOutQuad; linear | – | statischer Glow, Spinner bleibt |
| Treffer gefunden | Match gefunden | Pille Scale + Gold-Blitz | 1 → 1,15 → 1 | Feder `pop` | – | – | ohne |
| SPIELEN → Suche | Klick | Knopf-Text wechselt; Timer erscheint | Text-Flip (Scale y 1 → 0 → 1) | 160 ms | inOutQuad | – | Schnitt |
| Modus-Karte wechselt | neue Auswahl | Karte flippt | Scale x 1 → 0 → 1 | 240 ms | inOutQuad | – | Schnitt |
| Party-Figur kommt / geht | Beitritt / Austritt | Figur y, Deckkraft; Podest-Glow | −40 → 0 mit Feder `bouncy`; Ring-Puls | 444 ms | – | 80 ms je Platz | Fade |
| Karussell | alle 8 s, Klick | Folie x | 100 % → 0 | 420 ms | outCubic | – | Schnitt |
| Lade-Kreisel | Warten | Rotation | 360° | 1000 ms je Umdrehung | linear | – | bleibt |
| Ladebalken (System-Screen) | Fortschritt | Füllung | folgt dem Wert | 240 ms | outCubic | – | sofort |
| Einstellungen öffnen | Klick | Deckkraft, Scale | 0 → 1, 0,98 → 1 | 240 ms | outCubic | Zeilen 24 ms | Fade |
| UI-Größe | Einstellung | – | sofort (15.2) | 0 ms | – | – | – |
| Tab-Liste | Tab halten | – | sofort voll sichtbar; geänderte Zelle blitzt | 0 ms / 240 ms | – | – | ohne Blitz |
| Kampf-HUD ↔ Bau-HUD | Bauphase beginnt/endet (M) | Waffenbereich ↔ Werkzeugleiste | Tausch im selben Frame | 0 ms | – | – | – |
| Schadens-Rest | Schaden | heller Balkenteil Scale x | alter → neuer Wert (Wert selbst sofort) | 300 ms stehen + 240 ms | outCubic | – | springt nach 300 ms |
| Wenig Leben | Gesundheit ≤ 25 % | Balken-Tint, Vignette-Deckkraft | `hp` ↔ `danger.text`, 0,15 ↔ 0,35 | 860-ms-Schleife | inOutQuad | – | statisch |
| Brick-/Waffen-Platz wechseln | 1–9, Mausrad, 1–4 | Platz Scale (Platz ist sofort aktiv) | 1,0 → 1,08 → 1,0 | Feder `pop` | – | – | ohne |
| Bau-Ablehnung | abgelehnte Aktion | Rot-Tint am Werkzeug; Toast-Shake | 0 → 60 % → 0; x ±4 | 240 ms | inOutQuad | – | Tint ohne Puls |
| Limit erreicht | Setzversuch bei „n/Limit“ | Platz x | Shake ±4 | 240 ms | – | – | ohne |
| Killfeed, Trefferkreuz, HUD-Warnungen, Banner, Status-Icons | Kapitel 13.9 | | | | | | |
| weitere Bau-HUD-Zustände | Kapitel 14.5 | | | | | | |

### 15.8 Sequenzen
Alle Sequenzen sind mit Klick, Leertaste oder Esc überspringbar (wie heute), dazu **NEU** mit Enter und Gamepad-A/B; Überspringen springt in den Endzustand (Zahlen final, Partikel aus).

**Ergebnis-Sequenz** (`ResultsSequence`, Ebene 45)
| Zeit | Ereignis | Details |
|---|---|---|
| 0 ms | Hintergrund | Abdunkeln 0 → 60 %, 240 ms outCubic |
| 120 ms | Titelkarte (SIEG / NIEDERLAGE / UNENTSCHIEDEN / „n. PLATZ“ / INFIZIERT / ÜBERLEBT / VERTEIDIGUNG) | Slam: Scale 1,6 → 1,0, Deckkraft 0 → 1, 240 ms outBack(1.4); Banner `reward_banner` rollt aus (Scale x 0 → 1, 240 ms) |
| 360 ms | Aufprall | UI-Erschütterung 4 px (120 ms), `fx_ring`, bei SIEG `fx_confetti`; Ton `ui_slam` |
| 700 ms | Zähler „+n XP“, „+n Brix“, Bonuszeilen | je Zeile 120 ms versetzt: y 16 → 0 + Fade 160 ms; Zahl rollt 600 ms (`ui_coin`-Ticks, höchstens 12/s) |
| 1500 ms | Rangbalken „RANG n“ | füllt von alt auf neu in 900 ms outCubic; `fx_ember`-Funken an der Füllspitze (30/s) |
| bei Überlauf | Rang-Aufstieg | Balken voll → Blitz → Rang-Aufstieg (unten) → Balken beginnt bei 0 und füllt weiter |
| ≈ 2600 ms | „Klicken für die Tabelle“ | Fade 240 ms, dann Puls 1600 ms |

**Rang-Aufstieg** (Ergebnis-Sequenz oder Popup, 900 ms Kern)
1. 0 ms: `reward_rays` blenden ein (0 → 0,6, 240 ms) und drehen 20°/s.
2. 0 ms: Emblem `reward_rankup_emblem` Scale 0,4 → 1,0 mit Feder `bouncy`.
3. 120 ms: Schockwelle `fx_ring` Scale 0,2 → 2,2, Deckkraft 1 → 0, 600 ms outCubic; 40 `fx_ember` + 60 `fx_confetti`.
4. 200 ms: „RANG n!“ Slam 1,4 → 1,0, 240 ms outBack(1.4); Ton `ui_rankup`.
5. Profil-Chip (Top-Leiste) zeigt den neuen Rang beim nächsten Öffnen mit Zähler-Puls.

**Tägliche Belohnung ABHOLEN**
1. Tages-Kachel pulsiert (Feder `pop`).
2. Truhe wackelt 3× (Rotation ±6°, 240 ms gesamt), wechselt auf `reward_chest_open` mit Scale 1,15 → 1,0 (`bouncy`); dahinter `reward_rays`. Bei „Animationen reduzieren“ steht die Truhe sofort offen.
3. 24 `fx_coin` steigen auf und fliegen auf Bahnen zur Brix-Pille (600 ms, 20 ms versetzt); die Pille rollt beim Eintreffen hoch; `ui_reward`, `ui_coin`.
4. Knopf wird „ABGEHOLT“, Kachel „TAG n · ABGEHOLT“.

**Kauf erfolgreich** (KAUF BESTÄTIGEN → JETZT KAUFEN)
1. Ladekreisel im Knopf, solange der Server antwortet.
2. Erfolg: Haken zeichnet sich (160 ms), Dialog schließt (120 ms).
3. 12 `fx_coin` fliegen von der Brix-Pille zur Karte (400 ms), die Pille rollt herunter.
4. Etikett „BESITZ“ ploppt auf der Karte (Feder `pop`), 12 `fx_sparkle` im Kreis; `ui_purchase`.

**Werkstatt**
| Ergebnis | Ablauf |
|---|---|
| „Erfolg!“ | `frame_ornate` + Titel-Slam (240 ms outBack); Sterne füllen sich einzeln (120 ms versetzt); 40 `fx_ember` + 20 `fx_sparkle` Gold-Burst; `ui_success`; WEITER |
| „Kein Erfolg“ | `fx_crack` wächst über das Item (Scale 0,6 → 1,0 in 120 ms), Shake ±6 px 300 ms, `fx_smoke`-Puff, 12 `fx_shard`, Item kurz entsättigt; `ui_fail`; WEITER |
| „ITEM ZERLEGEN“ → ENDGÜLTIG ZERLEGEN | Item reißt (`fx_crack`), zerfällt in 16 `fx_shard`, die zur Splitter-Pille fliegen; „+n“ rollt; `ui_disassemble` |

**Glücksbrett-Aufdecken**
1. Feld `reward_board_field` flippt: Scale x 1 → 0 (120 ms inOutQuad), Seite wechselt, 0 → 1 (160 ms outBack).
2. Hinter dem Feld leuchtet die Stufen-Farbe; `fx_star` in Stufen-Farbe: Gewöhnlich 6 · Ungewöhnlich 10 · Selten 16 · Episch 24 · Hauptgewinn 40.
3. Overlay Gewinn mit Stufen-Name und Symbol; bei Hauptgewinn dazu `frame_ornate` + `frame_ornate_crest`, `reward_rays`, 80 `fx_confetti`; `ui_reveal` bzw. `ui_jackpot`; SUPER.

### 15.9 Animationen reduzieren (**NEU**)
Einstellungen › Barrierefreiheit „Animationen reduzieren“ (an/aus). Zusätzlich gilt der Wunsch des Betriebssystems, falls verfügbar, als Startwert.

| Bereich | Verhalten bei „an“ |
|---|---|
| Bewegung | Alle Bewegungen (Gleiten, Lift, Scale, Shake, Slam, Flip, Bounce) werden zu Fades ≤ 120 ms oder zu einem Schnitt. |
| Partikel | alle aus, auch Goldstaub |
| Schleifen | Puls, Fokus-Glühen, Strahlen-Drehung, wippende Pfeile stehen still; nur Spinner und Timer-Ringe laufen. |
| Blur | statisch, ohne Überblendung |
| Zahlen und Balken | springen auf den Endwert |
| Sequenzen | Ergebnis-Sequenz zeigt alle Zeilen auf einmal; Rang-Aufstieg als statische Karte |
| HUD | unverändert sofort (15.2); Feedback-Pulse aus; Low-HP statisch |
| Ton | bleibt (Sounds sind kein Bewegungsreiz) |

---

## 16. Partikel-Spec
Ein eigener UI-Partikel-Emitter auf dem Canvas (Kapitel 18.6), Sprites aus dem Atlas `ui_fx` (IDs aus `data/ui_assets.csv`). Größen in logischen px, Geschwindigkeit in px/s, Schwerkraft in px/s².

### 16.1 Effekte

| Effekt | Sprite | Emitter | Anzahl | Lebensdauer | Geschw. | Schwerkraft | Größe über Zeit | Farbe über Zeit | Rotation | Blend | Ebene | Budget | Reduziert |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Klick-Funken | `fx_sparkle` | Punkt (Klickpunkt), 360° | Burst 6–8 | 240–380 ms | 180–320, Luftwiderstand 4 | 0 | 10 → 0 | `#FFF4C2` → `#FFC21F` → transparent | zufällig, ±180°/s | additiv | Knopf + 1 | 8 je Klick, 24 gesamt | aus |
| Goldstaub (Hub, LOBBY) | `fx_gold_dust` (4 Varianten) | Rechteck volle Breite, untere 60 % hinter dem Inhalt | 6/s | 4–7 s | 8–20 aufwärts + Sinus-Wippen ±12 px bei 0,3 Hz | −2 | 2–6 (zufällig), konstant | `#FFD148` → `#FBB21D`; Deckkraft 0 → 0,35 (1 s) → 0 (1,5 s) | keine | additiv | Hub-Hintergrund (über `bg_hub_backdrop`, unter dem Inhalt) | 36 | aus |
| Podest-Glut (LOBBY) | `fx_glow_dot` | Linie am Podest | 2/s | 2–3 s | 10–30 aufwärts | 0 | 6 → 2 | `#FFC21F` → transparent | keine | additiv | LOBBY-Bühne | 10 | aus |
| Münz-Burst / Münz-Flug | `fx_coin` | Punkt an der Quelle, Kegel 60° nach oben | Burst 12–24 | 600–800 ms | 300–500, dann Zielflug zur Pille (Bézier) | 1400 bis zum Scheitel | 24 → 14 am Ziel | Sprite-Farbe, Deckkraft 1 | „Drehen“ über Scale x-Schwingung 6 Hz | Alpha | 58 bzw. Seite | 24 | aus; Pille springt mit Gold-Puls |
| Splitter | `fx_shard` | Punkt (Item, Schild-Icon) | Burst 10–16 (Rüstung 10) | 500–700 ms | 200–420 | 900 | 12–20 → 0 | Splitter `#E8742A` → `#A85200`; bei Rüstung `#7FB2E5` → `#15406C` | ±540°/s | Alpha | Seite / HUD 11 (Kampf-HUD) | 16 | aus |
| Konfetti | `fx_confetti` | Linie an der Oberkante | Burst 60 + 20/s für 1 s (Hauptgewinn 80) | 1,6–2,4 s | 100–300 abwärts + seitliches Driften | 250 | 10–16, Flattern über Scale y 3–6 Hz | zufällig aus `#FFC21F`, `#D93233`, `#1D7DBD`, `#F4EBD9` | ±360°/s | Alpha | 45 bzw. 58 | 120 | aus |
| Funken / Glut | `fx_ember` | Punkt (Füllspitze des Rangbalkens, Amboss) | 30/s während des Füllens; Burst 40 | 300–600 ms | 80–200, Kegel 90° nach oben | 300 | 6 → 0 | `#FFF4C2` → `#FFC21F` → `#C27200` | keine | additiv | 45 / 58 | 40 | aus |
| Schockwelle | `fx_ring` | Mitte | 1 | 600 ms | – | – | Scale 0,2 → 2,2 | `#FFD148`, Deckkraft 1 → 0 | keine | additiv | 45 / 58 | 3 | aus |
| Strahlenkranz | `reward_rays` (+ `fx_ray` für Einzelstrahlen) | Mitte, hinter dem Objekt | 1 | solange sichtbar | – | – | Atmen 0,95 ↔ 1,05 (2 s) | Deckkraft 0 → 0,6 | 20°/s | additiv | 58 | 1 | statisch, Deckkraft 0,4 |
| Leuchtpunkt-Puff | `fx_glow_dot` | Punkt | Burst 4–6 | 300 ms | 40–80 | 0 | 8 → 16 | `#FFD148`, Deckkraft 1 → 0 | keine | additiv | HUD 10 (Bau-HUD) / Seite | 6 | aus |
| Sterne (Stufen) | `fx_star` | Punkt (Feld, Karte) | Burst nach Stufe: 6 / 10 / 16 / 24 / 40 | 600–900 ms | 150–350 | 200 | 12–24 → 0 | Stufen-Textfarbe (11.4) | ±180°/s | additiv | Seite / 58 | 40 | aus |
| Rauch | `fx_smoke` | Punkt | Burst 3–5 (Bau-Ablehnung 2) | 600–900 ms | 30–60 | −20 | 32 → 64 | `#A8987A`, Deckkraft 0,5 → 0 | ±30°/s | Alpha | Seite / HUD 10 (Bau-HUD) | 6 | aus |
| Riss | `fx_crack` | über dem Item | 1 | 820 ms (120 auf, 400 stehen, 300 aus) | – | – | Scale 0,6 → 1,0 | Deckkraft 1 → 0 | keine | Alpha | Seite | 1 | aus |
| Funkeln (Hover-Karte, Kauf) | `fx_sparkle` | Ecke bzw. Kreis um die Karte | 1 je 600 ms bei Hover; Burst 12 beim Kauf | 400 ms | 0–40 | 0 | 0 → 12 → 0 | `#FFF4C2` | ±90°/s | additiv | Seite | 12 | aus |

Glanz-Sweep (`fx_shine_sweep`) ist kein Partikel, sondern ein maskiertes Sprite (15.6).

### 16.2 Budgets und Regeln
- Gleichzeitig höchstens **300** UI-Partikel; im Match-HUD höchstens **24**.
- Ein Emitter überschreitet nie sein Budget; neue Bursts ersetzen die ältesten Partikel desselben Emitters.
- Goldstaub läuft nur, solange der Hub sichtbar ist und die App den Fokus hat.
- Je Canvas gibt es höchstens 2 Draw Calls für Partikel (ein Material additiv, eins Alpha, ein Atlas `ui_fx`).
- „Animationen reduzieren“ schaltet alle Partikel ab (15.9).

---

## 17. Sound-Hooks
Baut auf `UiButtonSound` auf: Dort hängt heute der Klick-Sound der `UiFactory.Button`. Neu bekommt jedes Ereignis eine Sound-ID; `UiButtonSound` wird zu `UiSound.Play(id)`. Lautstärke über Einstellungen › Sound › „Oberfläche“; HUD-Sounds über „Effekte“. „Stumm im Hintergrund“ gilt wie heute.

| Ereignis | Sound-ID | Kanal | Hinweise |
|---|---|---|---|
| Hover, Fokuswechsel | `ui_hover` | Oberfläche | sehr leise (−18 dB), höchstens 1 je 60 ms |
| Klick auf Platte | `ui_click` | Oberfläche | ersetzt den heutigen Klick-Sound |
| Auswahl (Chip, Karte, Checkbox, Radio) | `ui_select` | Oberfläche | – |
| Zurück, Esc | `ui_back` | Oberfläche | – |
| Reiter / Unterreiter | `ui_tab` | Oberfläche | Tonhöhe steigt leicht nach rechts |
| Hub, kleines Menü, Panel, Dialog öffnen | `ui_open` | Oberfläche | – |
| … schließen | `ui_close` | Oberfläche | – |
| Sozial-Panel, breite Seite, Karussell | `ui_whoosh` | Oberfläche | – |
| Schalter an / aus | `ui_toggle_on` / `ui_toggle_off` | Oberfläche | – |
| Slider-Stufe | `ui_slider_tick` | Oberfläche | je Stufe bzw. 5 %, höchstens 20/s |
| Deaktiviert-Klick, Fehler | `ui_error` | Oberfläche | – |
| Toast | `ui_toast` | Oberfläche | leise |
| Benachrichtigungskarte, Glocke | `ui_notify` | Oberfläche | höchstens 1 je 2 s |
| Suche startet / Match gefunden | `ui_search_start` / `ui_match_found` | Oberfläche | `ui_match_found` auch bei geschlossenem Hub |
| Party-Mitglied kommt / geht | `ui_party_join` / `ui_party_leave` | Oberfläche | – |
| Belohnung aufgedeckt, Truhe | `ui_reward` | Oberfläche | – |
| Münz-Ticks, Zahl rollt | `ui_coin` | Oberfläche | höchstens 12/s, Tonhöhe steigt |
| Kauf | `ui_purchase` | Oberfläche | – |
| Rang-Aufstieg | `ui_rankup` | Oberfläche | – |
| Titelkarte | `ui_slam` | Oberfläche | – |
| Werkstatt Erfolg / kein Erfolg | `ui_success` / `ui_fail` | Oberfläche | – |
| ZERLEGEN | `ui_disassemble` | Oberfläche | – |
| Glücksbrett Flip / Hauptgewinn | `ui_reveal` / `ui_jackpot` | Oberfläche | Tonhöhe nach Stufe |
| Countdown / „LOS!“ | `ui_countdown` / `ui_go` | Effekte | – |
| Trefferkreuz / Kopftreffer / Kill | `hud_hitmarker` / `hud_headshot` / `hud_kill` | Effekte | vorhandene Sounds weiter nutzen, falls es sie gibt |
| Gesundheit ≤ 25 % | `hud_heartbeat` | Effekte | Schleife, solange ≤ 25 % |
| Rüstung bricht / Heilen | `hud_armor_break` / `hud_heal` | Effekte | – |
| Nachladen / keine Munition / überhitzt | `hud_low_ammo` / `hud_no_ammo` / `hud_overheat` | Effekte | einmal je Zustandswechsel |
| Granatwarnung | `hud_grenade_warn` | Effekte | – |
| Status beginnt | `hud_status_on` | Effekte | leise |
| Waffen-/Brick-Platz wechseln | `hud_slot_switch` | Effekte | – |
| Bau-Ablehnung / Limit | `hud_build_reject` / `hud_limit` | Effekte | – |

Regeln: Dieselbe ID spielt höchstens einmal je 50 ms. Sounds hängen am Ereignis, nicht an der Animation; sie spielen deshalb auch bei „Animationen reduzieren“ und bei übersprungenen Sequenzen (dann nur der letzte Ton).

---
## 18. Unity-Umsetzung

### 18.1 Architektur
- **uGUI bleibt.** Die bestehenden Fabriken (`UiFactory*`, `EconomyUi`, `UiControls`) werden zur **Skin-Schicht**: Ein `UiTheme` (ScriptableObject) hält Tokens (Farben, Schriften, Größen, Sprites, Dauer, Federn). `UiFactory` liest nur noch aus dem Theme. Bestehende Aufrufe funktionieren weiter und sehen danach neu aus.
- **Neue Bausteine** (Hub-Leisten, Sozial-Panel, Tab-Liste, kleines Esc-Menü, Bau-HUD, Kampf-HUD-Teile) sind Prefabs mit Fabrik-Methode (`UiFactory.HubTopBar(...)` usw.).
- **Seiten** sind eigenständig und können in zwei Hosts laufen: im Hub (mit Leisten) oder als **Einzelseite** (**NEU**, ohne Hub-Leisten, Ebene 40). Die Einzelseite nutzt nur die TEAM-Seite in B und A; andere Querverweise in den Hub zeigen dort „Nur in der Plaza“ (3.14 #23). Im Match öffnen Chat-Befehle den Baukasten als eigenes Modal (Ebene 50).
- **Ebenen:** `CreateCanvas(Ebene)` setzt `sortingOrder` = Ebene aus Kapitel 9 und hängt `UiScaler` an.

### 18.2 Alte Farbnamen → Tokens

| Alt | Neu |
|---|---|
| `Accent` | `state.normal` `#FCAE0F` (Fläche) bzw. `text.gold` `#FFD148` (Text) |
| `Surface` | `bg.panel` `#0B0B0D` |
| `SurfaceLight` | `bg.raised` `#16161A` |
| `SurfaceSoft` | `bg.track` `#0B0D0F` |
| `TextPrimary` | `text.primary` `#F4EBD9` |
| `TextMuted` | `text.muted` `#A8987A` |
| `Danger` | `danger` `#7C1F17` (Fläche) / `danger.text` `#E5533F` (Text) |
| `Good` | `toggle.on` `#192F01` (Fläche) / `good.text` `#8DBF3A` (Text) |
| `Selected` | `state.hover` `#FFC21F` + Goldrahmen (Zustand A, 12.3) |
| `TileColor` | `bg.track` mit Rahmen `frame` `#AE5F00` |
| `Expired` | `text.disabled` `#8C826F` |
| `TierColor` | `tier.*` (11.4), immer mit `tier_sym_*` |
| `RankColor` | Rang-Stufen `rank_t1`–`rank_t6`: Bronze `#9C4D01`, Silber `#B4BAC2`, Gold `#FCAE0F`, Medaille Gold + Band `#C71E15`, Stern Gold `#FFD148`, Legende Gold + Edelstein `#C71E15` |
| Währungsfarben Brix / Splitter / Kristalle / Münze | `cur.brix` `#FBB21D` / `cur.splitter` `#E8742A` / `cur.kristalle` `#6CC6F0` / `cur.muenze` `#FFD148` |
| Party- / Freund- / Leiter-Farbe | `accent.potion` `#1D7DBD` (Text `#7FB2E5`) / `accent.heart` `#D93233` / `gold.light` `#FFD148` (Krone) |
| Funkfarbe | Team-Licht der eigenen Seite: `#6FB0FF` bzw. `#FF7A6B` |
| Geister (hellblau) | `ghost` `#9FD8FF` |
| Teamfarben Blau / Rot | `team.blue` (Fläche `#5C83A8` → `#15406C`, HUD-Licht `#6FB0FF`) / `team.red` (Fläche `#AE4033` → `#7C100B`, HUD-Licht `#FF7A6B`) |

### 18.3 9-Slice und Sprites
Regeln in 10.5. Kurz: 2×-Sprites mit `pixelsPerUnitMultiplier = 2`, Ränder aus der Spalte `slice` in `data/ui_assets.csv`, Mitte gestreckt, Panel-Textur separat gekachelt, kleinere Varianten statt Stauchen. Zustände: Nur Grund- und deaktiviert-Zustand sind eigene Dateien; hover, gedrückt und ausgewählt entstehen per Tint (Spalte `zustaende`).

### 18.4 Sprite-Atlanten je Bereich

| Atlas | Inhalt | Größe |
|---|---|---|
| `ui_core` | Platten, Rahmen, Panels, Eingaben, Reiter, Chips, Badges, Fokus-Ring, Tastenhinweise, Esc-Menü, Tab-Liste | 2048² |
| `ui_icons` | Funktions- und Reiter-Icons, Währungen, Rollen-Badges, Rang-Abzeichen, Stufen-Symbole | 2048² |
| `ui_hud` | HUD- und Bau-HUD-Teile, Modus-Symbole klein | 2048² |
| `ui_modes` | Modus-Kacheln (`mode_*`) | 2048² |
| `ui_reward` | Truhen, Strahlenkranz, Prunkrahmen, Banner, Wimpel, Rang-Aufstieg, Tages-Kacheln, Glücksbrett-Felder, Stufen-Rahmen | 2048² |
| `ui_fx` | Partikel-Sprites `fx_*` | 1024² |
| einzeln | Hintergründe `bg_*`, Lobby-Podest | – |

Ein Screen nutzt höchstens 3 Atlanten; das HUD nur `ui_hud`, `ui_icons`, `ui_fx`.

### 18.5 Tween-Helfer
**Empfehlung: eigener, schlanker `UiTween`** (≈ 400 Zeilen) statt DOTween.

| Kriterium | eigener `UiTween` | DOTween |
|---|---|---|
| Federn (15.4) | physikalische Feder eingebaut | nur Easing-Kurven, Federn selbst nachbauen |
| „Animationen reduzieren“ | zentral an einer Stelle | je Aufruf bzw. eigene Hülle nötig |
| GC | Struct-Pool, 0 B pro Frame | wenig, aber Tweens müssen recycelt werden |
| Abhängigkeit | keine | Fremd-Paket |
| Funktionsumfang | genau das Nötige: Float/Vector/Color, Delay, Stagger, Sequenz, Abbruch → Endzustand, `unscaledTime` | sehr groß |

Wenn das Team DOTween bereits nutzt, ist es ebenfalls in Ordnung; dann läuft alles über eine Hülle `UiMotion`, damit Federn, Reduktion und Budgets an einer Stelle bleiben.

### 18.6 UI-Partikel-Emitter
- Eigener `UiParticleEmitter : MaskableGraphic`: Simulation auf der CPU, ein Mesh je Emitter, Partikel-Pool, Atlas `ui_fx`. Er sortiert sich wie jedes UI-Element in seine Canvas-Ebene ein.
- Parameter genau wie die Spalten in 16.1 (Form, Anzahl, Lebensdauer, Geschwindigkeit, Schwerkraft, Kurven für Größe/Farbe, Rotation, Blend), dazu ein Ziel-Punkt für Münz-Flüge.
- Ein globales `UiFxBudget` setzt die Grenzen aus 16.2 durch und schaltet bei „Animationen reduzieren“ alles ab.
- Alternative: das Open-Source-Paket „ParticleEffectForUGUI“ (MIT) mit normalen Unity-Partikelsystemen; dann gelten dieselben Budgets.

### 18.7 UiState-Kennungen
Die oberste Kennung im Stapel nimmt Maus und Steuerung (wie heute).

| Alt (Inventar) | Neu |
|---|---|
| `menu` | `hub` mit Seiten-Kennungen (P) · `menu` (kleines Esc-Menü in B, A, M) |
| `whats_new` / `login_reward` / `tutorial` | `popup.whats_new` / `popup.login_reward` / `popup.tutorial` (Dialog; die HUD-Karte hat keine Kennung) |
| `player_list`, `scoreboard_pinned` | `tablist` (nur angeheftet; Halten ist nicht modal) |
| `radio` | `radio` |
| `shop` | `hub.shop.catalog` (Geschenk-Modus `hub.shop.catalog.gift`) |
| `wardrobe` | `hub.locker.loadout` / `.appearance` / `.inventory` / `.workshop` |
| `range` | `hub.locker.range` |
| `rooms` | `hub.play.browser` (+ `hub.play.browser.create`) |
| `gallery` | `hub.create.gallery` |
| `board` | `hub.shop.board` |
| `leaderboard` | `hub.career.leaderboards` |
| `ranked` / `tournaments` / `spectate` | `hub.play.ranked` / `hub.play.tournaments` / `hub.play.spectate` |
| `clan_war` | `social.clan.treasury` / `social.clan.wars` |
| `stage` | `hub.lobby.news` |
| `support` | `support` |
| `maps` | `hub.create.maps` / `hub.create.cobuild` |
| `plot` / `publish` | `plot` (+ `plot.slots`, `plot.sky`, `plot.builders`, `plot.voice`, `plot.templates`) / `plot.publish` |
| `blueprints` / `templates` / `palette` | `blueprints` / `hub.create.templates` bzw. `plot.templates` / `palette` |
| `waiting` / `results_sequence` / `results` / `replay_viewer` | unverändert |
| `social` | `social.friends` / `.party` / `.clan` / `.mail` / `.plazas` / `.blocked` |
| `profile` | `profile` (Popup) · `hub.career.profile` |
| `settings` | `settings.graphics` / `.sound` / `.controls` / `.controller` / `.voice` / `.general` / `.accessibility` |
| `servermenu` | `hub.team` (P) · Einzelseite `page.team` (B, A) · `servermenu` als Modal im Match; **NEU** Unterseiten `hub.team.<kategorie>.<menü>` bzw. `page.team.…` (3a.7) |
| `player_actions` / `report` / `photo` / `chat` | unverändert |
| **NEU** | `hub.lobby`, `hub.play.quick`, `hub.shop.featured`, `hub.career.history`, `hub.career.replays`, `hub.career.mastery`, `hub.career.achievements`, `hub.career.missions`, `system_menu`, `bell`, `dialog.<name>` |

### 18.8 PadNavigator und Fokus
- Setzt den Fokus wie heute im obersten offenen Fenster. **NEU**: Fokus-Gruppen je Screen (Top-Leiste, Unterreiter, Inhalt, Fußleiste), Steuerkreuz bewegt innerhalb der Gruppe, an der Kante in die Nachbargruppe.
- Merkt sich den letzten Fokus je Seite; beim Zurückkehren landet der Fokus dort.
- Der Fokus geht nie verloren: Fällt ein Element weg, springt er zur Primäraktion der Ansicht.
- LB/RB, LT/RT, Gamepad-Y, Gamepad-X und View werden hier zentral verteilt (3.13). Der Fokus-Ring (`frame_focus`) ist eine einzige Instanz je Ebene, die gleitet.
- In Textfeldern sind Q/E und 1–9 als Hub-Kürzel aus.

### 18.9 Animationen reduzieren
Einstellungs-Schlüssel `accessibility.reduceMotion`. `UiTween`, `UiParticleEmitter`, Blur und alle Schleifen lesen ihn; Verhalten in 15.9.

### 18.10 Bildschirmfotos ohne UI (**NEU**)
- FOTO (Foto-Modus) rendert die Kamera in eine RenderTexture ohne UI-Canvases; Toasts und Karten der Ebene 70 landen nie im Bild.
- „Screenshot anhängen“ (Hilfe und Support) nimmt das letzte Spielbild **ohne Menü**: Beim Öffnen von Hub oder kleinem Menü wird einmal ein Bild ohne UI-Ebenen ≥ 30 gemerkt (eine RenderTexture, kein Verlauf).

### 18.11 LOBBY-Bühne
Eine eigene Kamera rendert eigene Figur und Party-Figuren (höchstens „PARTY n / m“) in eine RenderTexture (1024×1024) auf eigenem Layer. Sie ist nur aktiv, solange die LOBBY sichtbar ist; bei Kompakt/Schmal kleiner (768²).

**Truhe:** Die Tägliche Belohnung nutzt die 2D-Truhen `reward_chest_closed/open` (Entscheidung: keine 3D-Truhe). Wirkung entsteht über Wackeln, Wechsel auf offen mit Federn, die Strahlen `reward_rays` hinter dem Inhalt und den Münz-Burst.

### 18.12 Performance-Budgets

| Bereich | Budget |
|---|---|
| Hub offen | CPU ≤ 2,0 ms, ≤ 60 Draw Calls, ≤ 3 Atlanten |
| Hub öffnen bis bedienbar | Eingabe ab dem ersten Frame; Inhalt ≤ 100 ms |
| HUD im Match | CPU ≤ 0,8 ms, ≤ 25 Draw Calls; Rebuild nur bei geänderten Werten |
| Tweens | ≤ 200 gleichzeitig, ≤ 0,2 ms |
| Partikel | ≤ 300 (HUD ≤ 24), CPU ≤ 0,3 ms |
| Blur | einmal je Öffnen ≤ 0,5 ms GPU, danach 0 |
| LOBBY-Bühne | GPU ≤ 1,5 ms |
| UI-Texturen im Speicher | ≤ 96 MB |
| GC | 0 B pro Frame im Leerlauf, im HUD und während Menü-Animationen |

---

## 19. Replays für alle Spieler
Heute sehen normale Spieler nur Clips („Spielzug der Runde“) und Live-Zuschauen; ganze Replays gibt es nur für Staff (TEAM › Replays, Baukasten-Effekt „Replay ansehen“). **NEU**: Alle Spieler sehen ihre eigenen Matches.

### 19.1 Einstiege

| Einstieg | Ort | Was | Neu? |
|---|---|---|---|
| KARRIERE › Replays & Highlights › Meine Replays | P | eigene ganze Matches | **NEU** |
| KARRIERE › Replays & Highlights › Highlights | P | gespeicherte „Spielzug der Runde“-Clips | **NEU** |
| KARRIERE › Replays & Highlights › Turnier-Replays | P | öffentliche Turnier-Matches | **NEU** |
| KARRIERE › Match-Verlauf › REPLAY | P | Replay des gewählten Matches | **NEU** |
| Ergebnis › „Spielzug der Runde“ › ANSEHEN | M | Clip (wie heute); „In Highlights“ speichert ihn (**NEU**) | teilweise |
| SPIELEN › Turniere › Beendet › REPLAY | P | Turnier-Match | **NEU** |
| Live: SPIELEN › Zuschauen, Freundes-Zeile ZUSCHAUEN (**NEU**), Turniere ZUSCHAUEN, Clan-Kriege ZUSCHAUEN | P (in B/A zeigen Freundes-Zeile und Clan-Kriege „Nur in der Plaza“, **NEU**) | Live-Zuschauen | wie heute + Freundes-Zeile |
| TEAM › Replays, Baukasten-Effekt „Replay ansehen“ | Staff | alle Replays | unverändert |

### 19.2 Viewer (wie heute, neu gestaltet)

| Teil | Inhalt (Inventar) |
|---|---|
| Kopf | „Replay: Map · Modus“ bzw. „Zuschauen“ / „Highlight“, Untertitel, SCHLIESSEN |
| Mitte | Killfeed („X besiegt Y (Kopftreffer)“), Namen über den Figuren; Spielerliste mit „•••“ **nur Live** (wie heute). In Aufzeichnungen zeigt die Liste nur Namen zum Verfolgen mit der Kamera NAME (**NEU**), ohne „•••“. |
| Fußleiste | Zeitleiste mit Kill-Markern; ABSPIELEN / PAUSE; Tempo 0,25× / 0,5× / 1× / 2× / 4×; NÄCHSTER KILL; „KAMERA: FREI / ÜBERSICHT / AUTOMATISCH / NAME“; „Frame n · Tempo“ |
| Steuerung | freie Kamera WASD, E/Q, Shift; Esc schließt (zurück zum Einstieg); Foto-Modus im Replay immer (P) |
| Gamepad (**NEU**) | Gamepad-A ABSPIELEN/PAUSE · LB/RB Tempo · Gamepad-Y NÄCHSTER KILL · Gamepad-X Kamera-Modus · Sticks freie Kamera · Gamepad-B schließen |
| Ebene | 46 (über Hub und Ergebnis, 9.2) |

### 19.3 Server-Arbeit (offen)

| Punkt | Vorschlag |
|---|---|
| Liste der eigenen Replays | Abfrage je Konto (Konto-Filter), sortiert nach Datum: Map, Modus, Dauer, Ergebnis, Replay-ID |
| Rechte | Spieler: nur Matches, an denen sie selbst teilgenommen haben, plus öffentliche Turnier-Replays. Staff: wie heute alle. |
| Aufbewahrung | letzte **20 Matches** je Konto bzw. **14 Tage**, was zuerst endet; Turnier-Replays bis Saisonende |
| Highlights | „In Highlights“ speichert einen Verweis (Replay-ID + Zeitbereich), kein Video. Höchstens 50 je Konto; ein gespeichertes Highlight hält sein Replay über die 14 Tage hinaus fest. |
| Match-Verlauf | Liste der letzten 20 Matches mit den Werten der Ergebnis-Tabelle |
| Last | Replays werden nur bei Bedarf gestreamt; die Liste kommt ohne Replay-Daten |

### 19.4 Datenschutz
- Ein Replay zeigt nur, was im Match ohnehin sichtbar war: Namen, Kennzeichen, Killfeed. Kein Sprachchat, kein Chat.
- Spieler sehen nur eigene Matches und öffentliche Turnier-Matches, nie fremde Matches ohne Beteiligung.
- Eigene Highlights lassen sich löschen (**NEU** LÖSCHEN); beim Löschen des Kontos verschwinden Replays, Highlights und der Match-Verlauf.
- Offen (20/O13): Namen gesperrter Spieler in Replays ausblenden oder anzeigen?

---

## 20. Offene Punkte & Entscheidungen

### 20.1 Offene Punkte

| ID | Thema | Frage | Vorschlag |
|---|---|---|---|
| O1 | Replays (Server) | Liste je Konto, Rechte, Aufbewahrung, Highlights | 19.3 |
| O2 | Schnellspiel | Kann der Schnellstart Modus und Kanal übernehmen? | Parameter am Schnellstart; bis dahin nur „Alle Modi“ |
| O3 | TEAM auf B | ~~Der Plan lässt TEAM im kleinen Menü auf B weg.~~ | **gelöst:** TEAM und TEAM-WERKZEUGE stehen für Staff auf B (3a.5, 20.2) |
| O4 | Bereit-Status | Server-Feld je Party-Mitglied nötig | Haken in der LOBBY; ohne Server-Feld ausblenden |
| O5 | „+“ an Kristalle | Das Inventar kennt keinen Kauf von Kristallen. | Ziel LADEN › Katalog › Gems oder „+“ ausblenden |
| O6 | LADEN › Empfohlen | Datenquelle | Server-Liste; Fallback: Event-Items, „-n %“, neue Items |
| O7 | Querverweise aus B/A | AUS DEM LADEN, BESTENLISTEN/RANGLISTE und ZUSCHAUEN gingen heute auch außerhalb der Plaza; neu zeigen sie dort „Nur in der Plaza“ (3.14 #23). | so lassen; falls Spieler sie vermissen, als Einzelseite ohne Hub-Leisten nachrüsten (Technik wie TEAM-Einzelseite, 18.1) |
| O8 | Karten im Spiel per Gamepad | Wie nimmt man eine Party-Einladung am Controller an, ohne das Spiel zu verlassen? | View halten = ANNEHMEN, solange eine Karte sichtbar ist |
| O9 | Bestätigungen | „Spiel beenden?“ / „Match verlassen?“; Hinweis auf Folgen bei Gewertet | Dialog mit Strafe-Hinweis, falls es eine Strafe gibt |
| O10 | Schießstand | Zeigt das HUD heute Gesundheit/Rüstung am Schießstand? | ausblenden (13.8) |
| O11 | Einstellungen speichern | sofort wirksam (heute) oder ÜBERNEHMEN | wie heute sofort; ÜBERNEHMEN nur bei Anzeige-Werten |
| O12 | Tab-Liste in P/B/A | Halten statt Umschalten | Einstellung „Tab-Liste umschalten“ in Allgemein als Option |
| O13 | Replays und Sperren | Namen gesperrter Spieler im Replay | anzeigen wie im Match |
| O14 | Melden aus Aufzeichnungen | heute nur Live über „•••“ | später; über Profil möglich |
| O15 | Glocke-Verlauf | nur Sitzung oder serverseitig | Sitzung (30 Einträge) |
| O16 | Asset-Liste | `frame_dropdown_menu` nennt „Zur Plaza“ im System-Dropdown; im Plaza-Hub erscheint der Eintrag nie | Text in `data/ui_assets.csv` anpassen |
| O17 | Fremdes Profil im Match | POST und BESTENLISTEN sind im Match ausgeblendet (**NEU**). | bestätigen |
| O18 | Konto-Akte für MOD | ~~Laut Plan liest MOD die Konto-Akte nur.~~ | **entschieden:** MOD sanktioniert, blendet Maps aus/sperrt/gibt frei und schreibt Staff-Notizen in der Konto-Akte, sonst Lesen (3a.3); DEV liest den Live-Betrieb nur |
| O19 | Freigabe beim OWNER | Wer gibt Aktionen eines OWNER über einer Schwelle frei? | ohne Freigabe, im Audit-Log markiert; gibt es mehrere OWNER, gibt ein zweiter OWNER frei |
| O20 | Chat-Live und Datenschutz | Gehören Flüstern und Party-Funk in den Live-Feed? | nein; nur über Meldungen (3a.2.1) |
| O21 | Client-Logs | Muss der Spieler dem Hochladen zustimmen? | Toast-Hinweis an den Spieler; rechtlich prüfen |
| O22 | Support-Antworten | Antwortet der Support heute im Spiel oder in einem externen Werkzeug? | ANTWORTEN in Konto-Akte › Support nur, wenn der Server es anbietet; sonst nur Lesen |
| O23 | OWNER-Konten | Gleiche Rolle ist gesperrt (3a.4 #6). Wer ändert ein OWNER-Konto? | nur über die Server-Konsole |
| O24 | Schwellen Vier-Augen-Freigabe | ~~Der Plan nennt nur Brix und Kristalle.~~ | **entschieden:** > 10.000 Brix, > 500 Kristalle, > 5.000 Splitter, > 20 Münzen |
| O25 | Truhe 2D oder 3D | ~~3D-Truhe per RenderTexture~~ | **entschieden:** 2D-Truhe; der Katalog kann 3D-Modelle (Typ `model`) weiterhin, falls später gebraucht |

### 20.2 Getroffene Entscheidungen

| Entscheidung | Quelle |
|---|---|
| Hub mit 6 Reitern nur in der Plaza; B, A, M mit kleinem Esc-Menü | ÄNDERUNG 1 + 2 |
| Plaza-Gebäude, Stationen und Portale sind keine UI; `StationView` entfällt; kein Teleport | ÄNDERUNG 2 |
| Eine Tab-Liste für alle Modi | ÄNDERUNG 2 |
| HUD-Zustände und UI-Größe schalten sofort; Menüs animieren | ÄNDERUNG 4 |
| Gesundheit/Rüstung/Status bleiben in der Bauphase; Waffenbereich ↔ Werkzeugleiste sofort | ÄNDERUNG 5 |
| Auto-Skalierung 1920×1080, Match 0.5, 0.6–2.0 × UI-Größe | ÄNDERUNG 3 |
| Replays für alle Spieler, Ort KARRIERE | User-Feedback 1 + ÄNDERUNG 1 |
| Ergebnis (43), Ergebnis-Sequenz (45) und ReplayViewer (46) liegen über dem Menü-Band; Einstellungen 44 | Review (alte Reihenfolge Ord 42/44/49 > 40 bleibt), abgestimmt mit `data/ui_migration.csv` |
| Querverweise in den Hub zeigen in B und A „Nur in der Plaza“ | ÄNDERUNG 2 (Hub nur in der Plaza), abgestimmt mit `data/ui_migration.csv` |
| Eigener `UiTween` und eigener Partikel-Emitter | 18.5, 18.6 |
| TEAM mit Kategorien, Konto-Akte, Rechte-Matrix, Sicherheitsregeln und Vier-Augen-Freigabe; TEAM im kleinen Menü auch auf B | User-Wunsch, Kapitel 3a (löst O3) |

---

## 21. Dateien & Pflege

| Datei | Inhalt | Pflege |
|---|---|---|
| `ref/Brixel_UI-Inventar.html` | UI-Inventar (Quelle, Stand 06.10.2026) | nur ersetzen, nie von Hand ändern |
| `ref/ui-asset-sheet.webp` | Asset-Sheet (Stilvorlage, Farbmessung) | – |
| `UI_KONZEPT.md` | dieses Dokument | Neue Funktionen hier und in der CSV eintragen; **NEU** markieren |
| `data/ui_migration.csv` | 67 Zeilen: `bereich,titel,klasse,knoepfe,unterdialoge,neuer_ort,zugang_alt,zugang_neu,modi,bedingungen,ebene_alt,ebene_neu,status` | nach jeder Änderung `python3 tools/check_ui_migration.py` |
| `data/ui_migration.skeleton.csv` | Gerüst aus dem Inventar | neu erzeugen mit `python3 tools/check_ui_migration.py --skeleton`, wenn sich das Inventar ändert |
| `data/ui_assets.csv` | UI-Assets: `id,name,gruppe,typ,groesse,slice,zustaende,motiv_en,verwendung,basis,name_en`; `typ` ist `nineslice`, `sprite`, `icon`, `particle`, `background`, `mockup` oder `model` (3D-Modell mit Dreiecks-Budget in `groesse`; derzeit ohne Eintrag, der Katalog baut dafür Referenzbild- und Bild-zu-3D-Prompts) | IDs werden hier referenziert; umbenennen nur zusammen mit diesem Dokument |
| `artifact/ui-katalog.template.html` → `artifact/ui-katalog.html` | Prompt-Bibliothek (Midjourney `--sref`, GPT-Image/Firefly, SD/Flux + IP-Adapter) und durchsuchbare Migration | nach Änderungen an `ui_assets.csv` oder `ui_migration.csv`: `python3 tools/build_sheet.py` |
| `artifact/ui-prototyp.html` | klickbarer Prototyp (Hub, kleines Esc-Menü, Tab-Liste, HUDs, Komponenten, „Animationen reduzieren“) | Werte aus Kapitel 11 und 15 übernehmen |
| `tools/check_ui_migration.py` | Gerüst- und Prüfmodus: 67/67 Einträge, alle `ui-label` in `knoepfe`, Knopf-Texte aus den Hinweis-Blöcken (z. B. Fußzeile der Einstellungen), alle Zeilen des Esc-Menüs in `neuer_ort`, `neuer_ort` und `zugang_neu` gefüllt, `status` erlaubt (inkl. `entfällt`) | Exit-Code 1 bei Fehlern |
| `tools/build_sheet.py` | baut `artifact/*.html` aus Templates und CSV (Seite → Daten-Keys; UI-Katalog bekommt `ui`, `uimig` und das Sheet) | – |

**Ablauf bei Änderungen**
1. Inventar ändert sich → `ref/` ersetzen → `--skeleton` → CSV ergänzen → Prüfung grün.
2. Neue Funktion → hier im passenden Kapitel und in der CSV eintragen, **NEU** markieren, ggf. Einschränkung in 3.14 begründen.
3. Neues Asset → `data/ui_assets.csv` → `python3 tools/build_sheet.py` → im Katalog prüfen.
4. Token oder Motion ändern → Kapitel 11 bzw. 15 und `UiTheme` gemeinsam ändern.
