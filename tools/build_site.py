#!/usr/bin/env python3
"""Generates the GitHub Pages site in ../docs (German + English).

    python3 tools/build_site.py

All texts live in this file so both languages stay in sync. Screenshots are
picked up from docs/img/ by name; if one is missing a placeholder is shown,
so just drop new files (e.g. win-de-light.png, watch-en.png) into docs/img and
run the script again.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
IMG = DOCS / "img"

# ---------------------------------------------------------------- links
# Leave a value empty ("") to show "coming soon" instead of a button.
LINKS = {
    "windows_download": "https://github.com/mbaas2/FiveQThoughts/releases/latest",
    "mac_download": "https://github.com/mbaas2/FiveQThoughts/releases/latest",
    "appstore": "",  # App Store link for FiveQ (iPhone + Apple Watch), once live
    "repo_desktop": "https://github.com/mbaas2/FiveQThoughts",
    "repo_ios": "https://github.com/mbaas2/FiveQiOS",
    "repo_watch": "https://github.com/mbaas2/FiveQWatch",
    "coffee": "https://buymeacoffee.com/mbaas",
    "sponsors": "https://github.com/sponsors/mbaas2",
    "thebrain_keys": "https://app.thebrain.com/api-keys",
}

T = {
    "de": {
        "html_lang": "de",
        "other": ("en", "English"),
        "title": "FiveQ – Quick Thoughts für TheBrain auf Mac, Windows, iPhone & Apple Watch",
        "description": "FiveQ zeigt deine neuesten TheBrain Quick Thoughts auf einen Blick – und erfasst neue Gedanken in Sekunden: am Desktop, auf dem iPhone oder per Diktat an der Apple Watch.",
        "nav": [("#funktionen", "Funktionen"), ("#plattformen", "Plattformen"), ("#installation", "Installation"), ("#unterstuetzen", "Unterstützen")],
        "ids": {"features": "funktionen", "platforms": "plattformen", "install": "installation", "support": "unterstuetzen"},
        "hero_h1": "Deine Quick Thoughts.<br>Immer griffbereit.",
        "hero_lead": "FiveQ zeigt die neuesten Quick Thoughts aus TheBrain auf einen Blick – und hält neue Gedanken in Sekunden fest: am Mac oder PC, auf dem iPhone oder per Diktat an der Apple Watch.",
        "badges": ["🖥️ macOS", "🪟 Windows", "📱 iPhone", "⌚ Apple Watch", "🇩🇪 Deutsch / 🇬🇧 English", "🌓 Hell & Dunkel"],
        "cta_install": "Installieren",
        "cta_features": "Funktionen ansehen",
        "hero_alt": "FiveQThoughts auf dem Mac mit sechs Quick Thoughts",
        "features_h2": "Funktionen",
        "features_sub": "Gemacht für den schnellen Blick zwischendurch – und das schnelle Festhalten.",
        "features": [
            ("⚡", "Die neuesten auf einen Blick", "Die 5 (oder bis zu 20) neuesten Quick Thoughts als gleich große Kacheln – automatisch aktuell dank Live-Sync."),
            ("＋", "Blitzschnell erfassen", "Neuer Gedanke per Taste N, mit Text, Links und Bildern direkt aus der Zwischenablage."),
            ("🎙️", "Diktieren", "Auf iPhone und Apple Watch einfach lossprechen – der Gedanke landet direkt in TheBrain."),
            ("📋", "Kopieren mit einem Klick", "Text oder Grafik eines Quick Thoughts direkt in die Zwischenablage übernehmen."),
            ("✏️", "Bearbeiten & Aufräumen", "Quick Thoughts ändern, Anhänge ergänzen oder entfernen und Erledigtes löschen."),
            ("⌨️", "Globaler Shortcut", "⌃⌥Q (Mac) bzw. Strg+Alt+Q (Windows) holt das Fenster aus jeder App nach vorn."),
            ("☁️", "Lokal oder Cloud", "Nutzt die lokale TheBrain-Desktop-API und wechselt automatisch zur TheBrain Cloud, wenn TheBrain nicht läuft."),
            ("🔑", "Einfache Einrichtung", "API-Key einmal am Desktop eintragen und per QR-Code oder Handoff auf iPhone und Watch übertragen."),
        ],
        "platforms_h2": "Plattformen",
        "platforms_sub": "Eine Idee, vier Bildschirme.",
        "mac_h3": "🖥️ Mac",
        "mac_points": ["Native App mit Dock-Symbol und Menüleisten-Eintrag ⚡5Q", "Globaler Shortcut ⌃⌥Q", "Grafiken als echte Bilder in die Zwischenablage kopieren", "Hell, Dunkel oder automatisch nach System"],
        "mac_alt": "FiveQThoughts auf dem Mac",
        "win_h3": "🪟 Windows",
        "win_points": ["Eigenständige App mit Tray-Symbol", "Globaler Shortcut Strg+Alt+Q", "Installer ohne Admin-Rechte, optional mit Windows starten", "Kein Python nötig – alles ist enthalten"],
        "win_alt": "FiveQThoughts unter Windows",
        "ios_h3": "📱 iPhone",
        "ios_points": ["Gedanken diktieren, tippen oder Fotos anhängen", "Liste mit Suche und Filtern (mit Links, heute)", "Bearbeiten, kopieren, löschen", "Überträgt den API-Key auf die Apple Watch"],
        "ios_alt1": "FiveQ auf dem iPhone: Liste der Quick Thoughts",
        "ios_alt2": "FiveQ auf dem iPhone: neuer Gedanke",
        "watch_h3": "⌚ Apple Watch",
        "watch_points": ["Gedanken direkt am Handgelenk diktieren", "Haptische Bestätigung beim Speichern", "Die 5 neuesten Quick Thoughts ansehen", "Komplikation fürs Zifferblatt"],
        "watch_alt": "FiveQ auf der Apple Watch",
        "placeholder": "Screenshot folgt",
        "install_h2": "Installation",
        "install_sub": "Voraussetzung ist ein TheBrain-Konto. Für die mobilen Apps brauchst du einen Cloud-API-Key, für den Desktop wahlweise den lokalen oder den Cloud-Key.",
        "install_keys_h3": "🔑 API-Key besorgen",
        "install_keys": [
            "<strong>Cloud-Key</strong> (für iPhone, Watch und Desktop-Fallback): auf <a href=\"{thebrain_keys}\">app.thebrain.com/api-keys</a> erstellen.",
            "<strong>Lokaler Key</strong> (optional, Desktop): in TheBrain unter <em>Settings → User → Local API</em>.",
        ],
        "install_win_h3": "🪟 Windows",
        "install_win": [
            "<code>FiveQThoughts-Setup-x.y.z.exe</code> herunterladen und ausführen (keine Admin-Rechte nötig).",
            "App starten, auf <strong>⚙ API</strong> klicken und den Key eintragen.",
            "Mit <strong>Strg+Alt+Q</strong> jederzeit ein- und ausblenden.",
        ],
        "install_win_note": "Benötigt die Microsoft Edge WebView2 Runtime – in Windows 11 bereits enthalten.",
        "install_mac_h3": "🖥️ Mac",
        "install_mac": [
            "FiveQThoughts herunterladen und entpacken.",
            "<code>FiveQThoughts.app</code> öffnen – beim ersten Start wird die native App eingerichtet.",
            "Auf <strong>⚙ API</strong> klicken, Key eintragen. Shortcut: <strong>⌃⌥Q</strong>.",
        ],
        "install_mac_note": "Benötigt Python 3.9+ (z. B. über die Xcode Command Line Tools).",
        "install_ios_h3": "📱 iPhone & ⌚ Apple Watch",
        "install_ios": [
            "FiveQ aus dem App Store laden – die Watch-App wird automatisch mitinstalliert.",
            "In den <strong>Einstellungen</strong> den Cloud-Key eintragen – oder am Desktop unter ⚙ API den <strong>QR-Code</strong> scannen.",
            "Der Key wird automatisch an die Apple Watch übertragen.",
        ],
        "download": "Download",
        "appstore": "Im App Store",
        "soon": "Demnächst verfügbar",
        "support_h2": "Unterstützen",
        "support_text": "FiveQ ist ein privates Projekt und kostenlos. Wenn dir die App gefällt, freue ich mich über einen Kaffee ☕ oder einen Stern auf GitHub.",
        "coffee": "☕ Buy me a coffee",
        "sponsors": "💙 GitHub Sponsors",
        "footer_by": "Ein Projekt von Michael Baas · DLS Software &amp; Beratung GmbH",
        "footer_tm": "TheBrain ist eine Marke von TheBrain Technologies LP. FiveQ ist ein unabhängiges Projekt und steht in keiner Verbindung zu TheBrain Technologies.",
        "privacy": ("datenschutz.html", "Datenschutz"),
        "imprint": ("impressum.html", "Impressum"),
        "source": "Quellcode",
    },
    "en": {
        "html_lang": "en",
        "other": ("de", "Deutsch"),
        "title": "FiveQ – Quick Thoughts for TheBrain on Mac, Windows, iPhone & Apple Watch",
        "description": "FiveQ shows your latest TheBrain Quick Thoughts at a glance – and captures new ones in seconds: on the desktop, on your iPhone or by dictation on your Apple Watch.",
        "nav": [("#features", "Features"), ("#platforms", "Platforms"), ("#install", "Install"), ("#support", "Support")],
        "ids": {"features": "features", "platforms": "platforms", "install": "install", "support": "support"},
        "hero_h1": "Your Quick Thoughts.<br>Always at hand.",
        "hero_lead": "FiveQ shows your latest Quick Thoughts from TheBrain at a glance – and captures new ones in seconds: on your Mac or PC, on your iPhone or by dictation on your Apple Watch.",
        "badges": ["🖥️ macOS", "🪟 Windows", "📱 iPhone", "⌚ Apple Watch", "🇬🇧 English / 🇩🇪 Deutsch", "🌓 Light & Dark"],
        "cta_install": "Install",
        "cta_features": "See features",
        "hero_alt": "FiveQThoughts on the Mac showing six Quick Thoughts",
        "features_h2": "Features",
        "features_sub": "Made for a quick glance in between – and for capturing ideas fast.",
        "features": [
            ("⚡", "Latest at a glance", "The 5 (or up to 20) newest Quick Thoughts as equally sized tiles – always up to date thanks to Live Sync."),
            ("＋", "Capture in a flash", "New thought with the N key, with text, links and images straight from the clipboard."),
            ("🎙️", "Dictation", "On iPhone and Apple Watch, just start talking – the thought goes straight into TheBrain."),
            ("📋", "One-click copy", "Copy the text or image of a Quick Thought to the clipboard."),
            ("✏️", "Edit & tidy up", "Change Quick Thoughts, add or remove attachments and delete what's done."),
            ("⌨️", "Global shortcut", "⌃⌥Q (Mac) or Ctrl+Alt+Q (Windows) brings the window to the front from any app."),
            ("☁️", "Local or cloud", "Uses the local TheBrain desktop API and switches to TheBrain Cloud automatically when TheBrain isn't running."),
            ("🔑", "Easy setup", "Enter your API key once on the desktop and transfer it to iPhone and Watch via QR code or Handoff."),
        ],
        "platforms_h2": "Platforms",
        "platforms_sub": "One idea, four screens.",
        "mac_h3": "🖥️ Mac",
        "mac_points": ["Native app with Dock icon and menu bar item ⚡5Q", "Global shortcut ⌃⌥Q", "Copy images to the clipboard as real pictures", "Light, dark or following the system"],
        "mac_alt": "FiveQThoughts on the Mac",
        "win_h3": "🪟 Windows",
        "win_points": ["Standalone app with tray icon", "Global shortcut Ctrl+Alt+Q", "Installer without admin rights, optionally start with Windows", "No Python required – everything is included"],
        "win_alt": "FiveQThoughts on Windows",
        "ios_h3": "📱 iPhone",
        "ios_points": ["Dictate or type thoughts, attach photos", "List with search and filters (with links, today)", "Edit, copy, delete", "Transfers the API key to your Apple Watch"],
        "ios_alt1": "FiveQ on iPhone: list of Quick Thoughts",
        "ios_alt2": "FiveQ on iPhone: new thought",
        "watch_h3": "⌚ Apple Watch",
        "watch_points": ["Dictate thoughts right on your wrist", "Haptic confirmation when saved", "See the 5 newest Quick Thoughts", "Complication for your watch face"],
        "watch_alt": "FiveQ on Apple Watch",
        "placeholder": "Screenshot coming soon",
        "install_h2": "Installation",
        "install_sub": "You need a TheBrain account. The mobile apps use a cloud API key; the desktop app can use either the local or the cloud key.",
        "install_keys_h3": "🔑 Get an API key",
        "install_keys": [
            "<strong>Cloud key</strong> (for iPhone, Watch and desktop fallback): create one at <a href=\"{thebrain_keys}\">app.thebrain.com/api-keys</a>.",
            "<strong>Local key</strong> (optional, desktop): in TheBrain under <em>Settings → User → Local API</em>.",
        ],
        "install_win_h3": "🪟 Windows",
        "install_win": [
            "Download and run <code>FiveQThoughts-Setup-x.y.z.exe</code> (no admin rights needed).",
            "Start the app, click <strong>⚙ API</strong> and enter your key.",
            "Press <strong>Ctrl+Alt+Q</strong> anytime to show or hide it.",
        ],
        "install_win_note": "Requires the Microsoft Edge WebView2 Runtime – already included in Windows 11.",
        "install_mac_h3": "🖥️ Mac",
        "install_mac": [
            "Download and unzip FiveQThoughts.",
            "Open <code>FiveQThoughts.app</code> – the native app is set up on first launch.",
            "Click <strong>⚙ API</strong> and enter your key. Shortcut: <strong>⌃⌥Q</strong>.",
        ],
        "install_mac_note": "Requires Python 3.9+ (e.g. via the Xcode Command Line Tools).",
        "install_ios_h3": "📱 iPhone & ⌚ Apple Watch",
        "install_ios": [
            "Get FiveQ from the App Store – the Watch app is installed automatically.",
            "Enter your cloud key in <strong>Settings</strong> – or scan the <strong>QR code</strong> shown on the desktop under ⚙ API.",
            "The key is transferred to your Apple Watch automatically.",
        ],
        "download": "Download",
        "appstore": "On the App Store",
        "soon": "Coming soon",
        "support_h2": "Support",
        "support_text": "FiveQ is a free side project. If you like it, I'd be happy about a coffee ☕ or a star on GitHub.",
        "coffee": "☕ Buy me a coffee",
        "sponsors": "💙 GitHub Sponsors",
        "footer_by": "A project by Michael Baas · DLS Software &amp; Beratung GmbH",
        "footer_tm": "TheBrain is a trademark of TheBrain Technologies LP. FiveQ is an independent project and is not affiliated with TheBrain Technologies.",
        "privacy": ("privacy.html", "Privacy"),
        "imprint": ("../de/impressum.html", "Imprint"),
        "source": "Source code",
    },
}


def img(name, alt, cls="shot", t=None):
    """<picture> with dark variant if available; placeholder if the light image is missing."""
    light = IMG / f"{name}-light.png" if (IMG / f"{name}-light.png").exists() else IMG / f"{name}.png"
    dark = IMG / f"{name}-dark.png"
    if not light.exists():
        return f'<div class="placeholder">📷 {escape(t["placeholder"])}</div>'
    src = f"../img/{light.name}"
    tag = f'<img class="{cls}" src="{src}" alt="{escape(alt)}" loading="lazy">'
    if dark.exists():
        return f'<picture><source srcset="../img/{dark.name}" media="(prefers-color-scheme: dark)">{tag}</picture>'
    return tag


def button(url, label, primary=False, t=None):
    if not url:
        return f'<span class="btn" aria-disabled="true">{escape(t["soon"])}</span>'
    return f'<a class="btn{" primary" if primary else ""}" href="{url}">{escape(label)}</a>'


def header(t, lang):
    other_code, other_name = t["other"]
    nav = "".join(f'<a class="nav-section" href="{h}">{escape(n)}</a>' for h, n in t["nav"])
    return f"""<header class="site-header"><div class="wrap">
  <a class="logo" href="./"><span class="bolt">⚡</span> FiveQ</a>
  <nav class="site-nav">{nav}<a class="lang-switch" href="../{other_code}/" hreflang="{other_code}">{other_name}</a></nav>
</div></header>"""


def footer(t):
    return f"""<footer><div class="wrap">
  <div>{t["footer_by"]}<br><span class="note">{escape(t["footer_tm"])}</span></div>
  <div><a href="{t["privacy"][0]}">{t["privacy"][1]}</a> · <a href="{t["imprint"][0]}">{t["imprint"][1]}</a> · <a href="{LINKS["repo_desktop"]}">{t["source"]}</a></div>
</div></footer>"""


def page(t, lang, title, body, desc):
    other_code = t["other"][0]
    return f"""<!doctype html>
<html lang="{t["html_lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:image" content="../img/mac-{lang}-light.png">
<link rel="alternate" hreflang="{other_code}" href="../{other_code}/">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
{header(t, lang)}
<main>
{body}
</main>
{footer(t)}
</body>
</html>
"""


def li(items):
    return "".join(f"<li>{i.format(**LINKS)}</li>" for i in items)


def index(lang):
    t = T[lang]
    ids = t["ids"]
    features = "".join(
        f'<div class="feature"><div class="ico">{i}</div><h3>{escape(h)}</h3><p>{escape(p)}</p></div>'
        for i, h, p in t["features"]
    )
    badges = "".join(f'<span class="badge">{escape(b)}</span>' for b in t["badges"])
    body = f"""
<div class="hero"><div class="wrap">
  <h1>{t["hero_h1"]}</h1>
  <p class="lead">{escape(t["hero_lead"])}</p>
  <div class="badges">{badges}</div>
  <div class="cta"><a class="btn primary" href="#{ids["install"]}">{t["cta_install"]}</a><a class="btn" href="#{ids["features"]}">{t["cta_features"]}</a></div>
  <div class="hero-shot">{img(f"mac-{lang}", t["hero_alt"], t=t)}</div>
</div></div>

<section id="{ids["features"]}"><div class="wrap">
  <h2>{t["features_h2"]}</h2><p class="sub">{escape(t["features_sub"])}</p>
  <div class="features">{features}</div>
</div></section>

<section id="{ids["platforms"]}"><div class="wrap">
  <h2>{t["platforms_h2"]}</h2><p class="sub">{escape(t["platforms_sub"])}</p>

  <div class="platform">
    <div class="pl-text"><h3>{t["mac_h3"]}</h3><ul>{li(t["mac_points"])}</ul></div>
    <div>{img(f"mac-{lang}-dark", t["mac_alt"], t=t)}</div>
  </div>

  <div class="platform reverse">
    <div class="pl-text"><h3>{t["win_h3"]}</h3><ul>{li(t["win_points"])}</ul></div>
    <div>{img(f"win-{lang}", t["win_alt"], t=t)}</div>
  </div>

  <div class="platform">
    <div class="pl-text"><h3>{t["ios_h3"]}</h3><ul>{li(t["ios_points"])}</ul></div>
    <div class="phones">{img(f"ios-{lang}-list", t["ios_alt1"], cls="shot", t=t)}{img(f"ios-{lang}-new", t["ios_alt2"], cls="shot", t=t)}</div>
  </div>

  <div class="platform reverse">
    <div class="pl-text"><h3>{t["watch_h3"]}</h3><ul>{li(t["watch_points"])}</ul></div>
    <div class="phones watch">{img(f"watch-{lang}-new", t["watch_alt"], cls="shot", t=t)}{img(f"watch-{lang}-list", t["watch_alt"], cls="shot", t=t)}</div>
  </div>
</div></section>

<section id="{ids["install"]}"><div class="wrap">
  <h2>{t["install_h2"]}</h2><p class="sub">{escape(t["install_sub"])}</p>
  <div class="install">
    <div class="card"><h3>{t["install_keys_h3"]}</h3><ul>{li(t["install_keys"])}</ul></div>
    <div class="card"><h3>{t["install_win_h3"]}</h3><ol>{li(t["install_win"])}</ol><p class="note">{escape(t["install_win_note"])}</p>{button(LINKS["windows_download"], t["download"], True, t)}</div>
    <div class="card"><h3>{t["install_mac_h3"]}</h3><ol>{li(t["install_mac"])}</ol><p class="note">{escape(t["install_mac_note"])}</p>{button(LINKS["mac_download"], t["download"], True, t)}</div>
    <div class="card"><h3>{t["install_ios_h3"]}</h3><ol>{li(t["install_ios"])}</ol>{button(LINKS["appstore"], t["appstore"], True, t)}</div>
  </div>
</div></section>

<section id="{ids["support"]}" class="support"><div class="wrap">
  <h2>{t["support_h2"]}</h2><p class="sub">{escape(t["support_text"])}</p>
  <div class="cta">{button(LINKS["coffee"], t["coffee"], True, t)}{button(LINKS["sponsors"], t["sponsors"], False, t)}</div>
</div></section>
"""
    return page(t, lang, t["title"], body, t["description"])


PRIVACY = {
    "de": ("Datenschutzerklärung – FiveQ", """
<h1>Datenschutzerklärung</h1>
<p class="note">Stand: November 2026 · <span class="todo">Entwurf – bitte vor Veröffentlichung prüfen</span></p>
<h2>Kurz gesagt</h2>
<p>FiveQ (iPhone, Apple Watch) und FiveQThoughts (Mac, Windows) erheben keine Daten für uns. Es gibt kein Tracking, keine Analyse-Tools, keine Werbung und keine eigenen Server.</p>
<h2>Welche Daten verarbeitet die App?</h2>
<ul>
<li><strong>API-Schlüssel:</strong> Dein TheBrain-API-Key wird ausschließlich lokal auf deinem Gerät gespeichert (iPhone/Watch: App-Einstellungen; Desktop: lokale Konfigurationsdatei).</li>
<li><strong>Quick Thoughts:</strong> Texte, Links und Bilder, die du anlegst oder ansiehst, werden direkt zwischen deinem Gerät und TheBrain übertragen – entweder an die lokale TheBrain-Desktop-App (<code>localhost</code>) oder an die TheBrain Cloud (<code>api.bra.in</code>). Für die Verarbeitung dort gilt die Datenschutzerklärung von TheBrain Technologies.</li>
<li><strong>Spracheingabe:</strong> Diktate werden über die Spracherkennung von Apple verarbeitet (siehe Datenschutzhinweise von Apple).</li>
<li><strong>Apple Watch:</strong> Der API-Key wird vom iPhone über die Apple-WatchConnectivity-Verbindung an deine Uhr übertragen.</li>
</ul>
<h2>Diese Website</h2>
<p>Diese Seite wird über GitHub Pages bereitgestellt. GitHub kann dabei technisch notwendige Zugriffsdaten (z. B. IP-Adresse) verarbeiten; siehe die Datenschutzerklärung von GitHub. Wir setzen keine Cookies und keine Analyse-Tools ein.</p>
<h2>Kontakt</h2>
<p>Verantwortlich: Michael Baas, DLS Software &amp; Beratung GmbH – Kontaktdaten siehe <a href="impressum.html">Impressum</a>.</p>
"""),
    "en": ("Privacy Policy – FiveQ", """
<h1>Privacy Policy</h1>
<p class="note">Last updated: November 2026 · <span class="todo">Draft – please review before publishing</span></p>
<h2>In short</h2>
<p>FiveQ (iPhone, Apple Watch) and FiveQThoughts (Mac, Windows) do not collect any data for us. There is no tracking, no analytics, no advertising and no server of our own.</p>
<h2>What data does the app process?</h2>
<ul>
<li><strong>API key:</strong> Your TheBrain API key is stored only locally on your device (iPhone/Watch: app settings; desktop: local configuration file).</li>
<li><strong>Quick Thoughts:</strong> Text, links and images you create or view are transferred directly between your device and TheBrain – either the local TheBrain desktop app (<code>localhost</code>) or TheBrain Cloud (<code>api.bra.in</code>). TheBrain Technologies' privacy policy applies to processing there.</li>
<li><strong>Dictation:</strong> Dictation is processed by Apple's speech recognition (see Apple's privacy information).</li>
<li><strong>Apple Watch:</strong> The API key is sent from your iPhone to your watch via Apple's WatchConnectivity.</li>
</ul>
<h2>This website</h2>
<p>This site is hosted on GitHub Pages. GitHub may process technically necessary access data (e.g. IP address); see GitHub's privacy statement. We use no cookies and no analytics.</p>
<h2>Contact</h2>
<p>Responsible: Michael Baas, DLS Software &amp; Beratung GmbH – see the <a href="../de/impressum.html">imprint</a> for contact details.</p>
"""),
}

IMPRINT_DE = ("Impressum – FiveQ", """
<h1>Impressum</h1>
<p><span class="todo">TODO: Pflichtangaben nach § 5 DDG ergänzen</span></p>
<p>DLS Software &amp; Beratung GmbH<br>
<span class="todo">Straße Hausnummer</span><br>
<span class="todo">PLZ Ort</span></p>
<p>Vertreten durch: <span class="todo">Geschäftsführer</span><br>
Registergericht: <span class="todo">…</span>, Registernummer: <span class="todo">HRB …</span><br>
USt-IdNr.: <span class="todo">DE…</span></p>
<p>E-Mail: <span class="todo">kontakt@…</span></p>
""")


def legal(lang, title, html):
    t = T[lang]
    return page(t, lang, title, f'<div class="wrap legal">{html}</div>', title)


def main():
    for lang in ("de", "en"):
        out = DOCS / lang
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(index(lang), encoding="utf-8")
        title, html = PRIVACY[lang]
        (out / T[lang]["privacy"][0]).write_text(legal(lang, title, html), encoding="utf-8")
    (DOCS / "de" / "impressum.html").write_text(legal("de", *IMPRINT_DE), encoding="utf-8")

    # Root: redirect by browser language
    (DOCS / "index.html").write_text("""<!doctype html>
<html><head><meta charset="utf-8"><title>FiveQ</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>location.replace((navigator.language || "en").toLowerCase().startsWith("de") ? "de/" : "en/");</script>
<meta http-equiv="refresh" content="1; url=en/">
</head><body><p><a href="de/">Deutsch</a> · <a href="en/">English</a></p></body></html>
""", encoding="utf-8")
    (DOCS / ".nojekyll").write_text("")
    print("site written to", DOCS)


if __name__ == "__main__":
    main()
