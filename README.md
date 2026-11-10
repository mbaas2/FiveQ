# ⚡ FiveQ – Website

Quellen der Produktseite für die FiveQ-Apps (Mac, Windows, iPhone, Apple Watch),
veröffentlicht über GitHub Pages aus dem Ordner `docs/`: **https://mbaas2.github.io/FiveQ/**

| App | Repo |
|---|---|
| Mac & Windows | [FiveQThoughts](https://github.com/mbaas2/FiveQThoughts) |
| iPhone | [FiveQiOS](https://github.com/mbaas2/FiveQiOS) |
| Apple Watch | [FiveQWatch](https://github.com/mbaas2/FiveQWatch) |

## Seite bearbeiten

Alle Texte (Deutsch und Englisch) stehen in [`tools/build_site.py`](tools/build_site.py).
Nach Änderungen neu generieren:

```bash
python3 tools/build_site.py
```

Screenshots liegen in `docs/img/` und werden über den Dateinamen gefunden
(`mac-de-light.png`, `ios-en-list-dark.png`, `win-de-light.png`, `watch-de-new.png` …).
Fehlt ein Bild, zeigt die Seite einen Platzhalter. Zu einer `-light`-Variante wird
eine vorhandene `-dark`-Variante automatisch im Dunkelmodus des Browsers gezeigt.

Download- und App-Store-Links stehen oben in `build_site.py` (`LINKS`).

## Screenshots erzeugen

Alle Skripte verwenden Demo-Einträge, damit keine echten Quick Thoughts sichtbar werden:

```bash
# Backend aus dem FiveQThoughts-Repo starten (nutzt dessen config.local.json)
python3 ../FiveQThoughts/app.py --no-browser --port 11599 &

python3 tools/seed_demo.py --lang de          # 6 Demo-Einträge anlegen
tools/capture_mac.sh de <outdir> <macos-host-binary> <winid-binary>
tools/capture_ios.sh de <outdir> <simulator-udid> <FiveQ.app (Debug)>
python3 tools/seed_demo.py --lang de --cleanup
```

- `capture_mac.sh` braucht den kompilierten Host (`swiftc -O ../FiveQThoughts/native/macos_host.swift -o host`)
  und `winid` (`swiftc -O tools/winid.swift -o winid`). Achtung: Es ändert Sprache und Design
  in der `config.local.json` des Backends – vorher sichern.
- `capture_ios.sh` nutzt die Debug-Startargumente `-screenshotTab` / `-screenshotAbout` der iOS-App.
- Windows: siehe [`tools/SCREENSHOTS-WINDOWS.md`](tools/SCREENSHOTS-WINDOWS.md).
- Apple Watch: `tools/capture_watch.sh <lang> <outdir> <watch-udid> <FiveQWatch.app>` (Debug-Build; der erste Boot des watchOS-Simulators dauert mehrere Minuten, danach ist die Watch anfangs sehr träge – ggf. Bilder verzögert nachholen).

## Lizenz / License

- 📄 Lizenz / License: [Apache 2.0 + Commons Clause](LICENSE) (Nutzung privat & gewerblich frei; kommerzielle Verwertung des Codes in eigenen Produkten erfordert eine Lizenz / free for personal & business use; selling or embedding the code in commercial products requires a commercial license)
