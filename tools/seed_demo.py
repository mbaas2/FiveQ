#!/usr/bin/env python3
"""Create (or remove) demo Quick Thoughts for screenshots.

Talks to a running FiveQThoughts backend (app.py), which forwards to TheBrain
(local API or cloud). The created IDs are stored in demo_ids_<lang>.json next to
this script so they can be removed again with --cleanup.

    python3 seed_demo.py --lang de [--backend http://127.0.0.1:11599] [--image demo_de.png]
    python3 seed_demo.py --lang de --cleanup

The demo thoughts become the newest ones, so the apps show only demo content
(the apps show the N newest Quick Thoughts; N = card count, default 5-6).
"""
import argparse
import base64
import json
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Oldest first: the last entry ends up at the top of the list.
DEMO = {
    "de": [
        {"markdown": "Zitat für die Präsentation\n\n„Notizen sind Gedanken, die man wiederfinden möchte.“"},
        {"markdown": "Einkauf Team-Frühstück\n\n• Croissants\n• Obst\n• Hafermilch\n• Kaffeebohnen ☕"},
        {"markdown": "Buchtipp von Lisa\n\nBuilding a Second Brain – unbedingt das Kapitel zu Progressive Summarization lesen.",
         "links": [{"title": "Building a Second Brain", "url": "https://www.buildingasecondbrain.com"}]},
        {"markdown": "Whiteboard-Skizze Projektstruktur Q1", "image": True},
        {"markdown": "Call mit Anna\n\nAngebot bis Mittwoch schicken, Workshop-Termin im Dezember vorschlagen."},
        {"markdown": "Idee: Wochenrückblick am Freitag\n\nJeden Freitag um 16 Uhr drei Fragen:\n1. Was lief gut?\n2. Was hat gebremst?\n3. Was nehme ich mir vor?"},
    ],
    "en": [
        {"markdown": "Quote for the presentation\n\n“Notes are thoughts you want to find again.”"},
        {"markdown": "Team breakfast shopping\n\n• Croissants\n• Fruit\n• Oat milk\n• Coffee beans ☕"},
        {"markdown": "Book tip from Lisa\n\nBuilding a Second Brain – make sure to read the chapter on Progressive Summarization.",
         "links": [{"title": "Building a Second Brain", "url": "https://www.buildingasecondbrain.com"}]},
        {"markdown": "Whiteboard sketch: project structure Q1", "image": True},
        {"markdown": "Call with Anna\n\nSend the quote by Wednesday, suggest a workshop date in December."},
        {"markdown": "Idea: weekly review on Friday\n\nEvery Friday at 4 pm, three questions:\n1. What went well?\n2. What slowed me down?\n3. What's next?"},
    ],
}


def call(backend, method, path, body=None):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(backend + path, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read()
        return json.loads(raw) if raw else {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", choices=["de", "en"], required=True)
    ap.add_argument("--backend", default="http://127.0.0.1:11599")
    ap.add_argument("--image", help="PNG used for the whiteboard thought (default: demo_<lang>.png next to script)")
    ap.add_argument("--cleanup", action="store_true", help="delete the demo thoughts created earlier")
    args = ap.parse_args()

    ids_file = HERE / f"demo_ids_{args.lang}.json"

    if args.cleanup:
        ids = json.loads(ids_file.read_text()) if ids_file.exists() else []
        for tid in ids:
            try:
                call(args.backend, "DELETE", f"/api/thoughts/{tid}")
                print("deleted", tid)
            except Exception as e:
                print("could not delete", tid, e)
        ids_file.unlink(missing_ok=True)
        return

    image = Path(args.image) if args.image else HERE / f"demo_{args.lang}.png"
    ids = json.loads(ids_file.read_text()) if ids_file.exists() else []
    for item in DEMO[args.lang]:
        attachments = []
        if item.get("image"):
            b64 = base64.b64encode(image.read_bytes()).decode("ascii")
            attachments.append({"name": image.name, "contentType": "image/png",
                                "dataUrl": f"data:image/png;base64,{b64}"})
        created = call(args.backend, "POST", "/api/thoughts",
                       {"markdown": item["markdown"], "links": item.get("links", []), "attachments": attachments})
        tid = created.get("id") or created.get("thought", {}).get("id")
        print("created", tid)
        if tid:
            ids.append(tid)
            ids_file.write_text(json.dumps(ids, indent=2))
        time.sleep(1.2)  # distinct timestamps -> stable order


if __name__ == "__main__":
    main()
