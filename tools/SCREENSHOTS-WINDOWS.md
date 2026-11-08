# Windows-Screenshots für die FiveQ-Website

Arbeitsanleitung für eine Claude-Code-Sitzung (oder einen Menschen) auf einem Windows-Rechner.
Ziel: vier Bilder in `docs/img/`, danach die Website neu generieren.

| Datei | Sprache | Design |
|---|---|---|
| `win-de-light.png` | Deutsch | Hell |
| `win-de-dark.png` | Deutsch | Dunkel |
| `win-en-light.png` | Englisch | Hell |
| `win-en-dark.png` | Englisch | Dunkel |

Die Mac-Bilder (`mac-*.png`) dienen als Vorbild: gleiche Fenstergröße (1180×840 logische Pixel),
6 Karten im Raster 3×2, Demo-Inhalte statt echter Quick Thoughts.

## 1. Voraussetzungen

- Repos nebeneinander auschecken: `FiveQ` (dieses Repo) und `FiveQThoughts`.
- FiveQThoughts installiert (`FiveQThoughts-Setup-x.y.z.exe`) **oder** aus dem Quellcode gestartet (`run_windows.bat`).
- In der App ist ein funktionierender API-Key hinterlegt (⚙ API). Python 3.9+ für die Skripte.
- In den Einstellungen der App **Anzahl angezeigter Karten = 6**.
- Windows-Anzeige-Skalierung 150 % oder 200 % ergibt schärfere Bilder (wie Retina am Mac).

## 2. Port des Backends herausfinden

Die App startet ihr Backend ab Port **11525** (nächster freier Port). Prüfen:

```powershell
Invoke-RestMethod http://127.0.0.1:11525/api/config | Select-Object version, activeBackend, cardCount
```

Im Folgenden `$B = "http://127.0.0.1:11525"` (ggf. anpassen).

## 3. Demo-Inhalte anlegen (verdeckt die echten Quick Thoughts)

Die App zeigt immer die *neuesten* Quick Thoughts. Das Seed-Skript legt sechs Demo-Einträge
an (einer davon mit Whiteboard-Bild `tools/demo_<lang>.png`), die dann ganz oben stehen.

```powershell
cd FiveQ\tools
python seed_demo.py --lang de --backend $B
```

Die IDs landen in `tools/demo_ids_de.json` (nicht committen) für das spätere Aufräumen.
**Erst die deutschen Bilder aufnehmen, dann die englischen Einträge anlegen** – die englischen
liegen dann oben und verdecken die deutschen.

## 4. Aufnehmen

Automatisch (Entwurf, auf dem Mac geschrieben und **noch nicht unter Windows getestet**):

```powershell
powershell -ExecutionPolicy Bypass -File tools\capture_windows.ps1 -Lang de -Backend $B
```

Das Skript setzt Sprache/Design über `POST /api/config`, startet die App neu, bringt das Fenster
auf 1180×840 und nimmt es per `PrintWindow` (inkl. Titelleiste) auf. Falls die App nach dem
Neustart einen anderen Port wählt oder das Bild schwarz bleibt (WebView2), manuell vorgehen:

1. In der App oben rechts die Sprache (🇩🇪 DE / 🇬🇧 EN) und mit 🌗 das Design wählen.
2. Fenster auswählen und **Alt+Druck** drücken (aktives Fenster in die Zwischenablage), dann
   z. B. in Paint einfügen und als PNG unter dem Namen aus der Tabelle speichern.
   Alternativ: Snipping Tool → Modus „Fenster“.
3. Darauf achten: kein Mauszeiger, kein Tooltip, keine Toast-Meldung im Bild.

Danach Englisch:

```powershell
python seed_demo.py --lang en --backend $B
powershell -ExecutionPolicy Bypass -File tools\capture_windows.ps1 -Lang en -Backend $B
```

## 5. Prüfen und einbauen

- Jedes Bild ansehen: nur Demo-Inhalte sichtbar? Bild im Whiteboard-Eintrag geladen?
  Titelleiste vollständig, keine fremden Fenster?
- Bilder auf max. 1600 px Breite verkleinern (z. B. mit Paint → „Größe ändern“ oder
  `magick in.png -resize 1600x out.png`), damit die Seite schnell lädt.
- Website neu bauen – die Platzhalter „Screenshot folgt“ werden automatisch ersetzt:

```powershell
python tools\build_site.py
```

## 6. Aufräumen

Demo-Einträge wieder löschen und Sprache/Design in der App zurückstellen:

```powershell
python tools\seed_demo.py --lang de --backend $B --cleanup
python tools\seed_demo.py --lang en --backend $B --cleanup
```

Danach `docs/img/win-*.png` und ggf. neu generierte `docs/**/*.html` committen.
