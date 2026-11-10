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
    "testflight": "https://testflight.apple.com/join/Fmn9sSgS",  # FiveQ (iPhone + Apple Watch) beta; use an App Store link here once live
    "testflight_app": "https://apps.apple.com/app/testflight/id899247664",
    "repo_desktop": "https://github.com/mbaas2/FiveQThoughts",
    "repo_ios": "https://github.com/mbaas2/FiveQiOS",
    "repo_watch": "https://github.com/mbaas2/FiveQWatch",
    "coffee": "https://buymeacoffee.com/mbaas",
    "sponsors": "https://github.com/sponsors/mbaas2",
    "thebrain": "https://www.thebrain.com",
    "thebrain_keys": "https://app.thebrain.com/api-keys",
    "issues": "https://github.com/mbaas2/FiveQThoughts/issues",
    "email": "mailto:FiveQ@mail.mbaas.de",
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
            "<strong>Lokaler Key</strong> (optional, Desktop): in <a href=\"{thebrain}\">TheBrain</a> unter <em>Settings → User → Local API</em>.",
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
            "<a href=\"{testflight_app}\"><strong>TestFlight</strong></a> aus dem App Store installieren, den Einladungslink unten öffnen und FiveQ installieren. Die Watch-App ist optional: Sie kommt automatisch auf die Uhr, wenn in der Watch-App auf dem iPhone „Apps automatisch installieren“ aktiv ist – sonst unter „Verfügbare Apps“ nachinstallieren.",
            "In den <strong>Einstellungen</strong> den Cloud-Key eintragen – oder am Desktop unter ⚙ API den <strong>QR-Code</strong> scannen.",
            "Falls die Watch-App installiert ist, wird der Key automatisch an die Apple Watch übertragen.",
        ],
        "download": "Download",
        "testflight": "Per TestFlight laden",
        "soon": "Demnächst verfügbar",
        "support_h2": "Unterstützen & Kontakt",
        "support_text": "FiveQ ist ein privates Projekt und kostenlos. Wenn dir die App gefällt, freue ich mich über einen Kaffee ☕ oder einen Stern auf GitHub.",
        "contact_text": "Hast du Feature-Wünsche, Feedback oder möchtest neue Projekte besprechen? Schreib mir gern an <a href=\"mailto:FiveQ@mail.mbaas.de\">FiveQ@mail.mbaas.de</a> oder nutze die <a href=\"https://github.com/mbaas2/FiveQThoughts/issues\">GitHub Issues</a>.",
        "coffee": "☕ Buy me a coffee",
        "sponsors": "💙 GitHub Sponsors",
        "email_btn": "✉️ FiveQ@mail.mbaas.de",
        "issues_btn": "💬 GitHub Issues",
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
            "<strong>Local key</strong> (optional, desktop): in <a href=\"{thebrain}\">TheBrain</a> under <em>Settings → User → Local API</em>.",
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
            "Install <a href=\"{testflight_app}\"><strong>TestFlight</strong></a> from the App Store, open the invitation link below and install FiveQ. The Watch app is optional: it is installed on your watch automatically if “Automatically install apps” is on in the Watch app on your iPhone – otherwise add it later under “Available Apps”.",
            "Enter your cloud key in <strong>Settings</strong> – or scan the <strong>QR code</strong> shown on the desktop under ⚙ API.",
            "If the Watch app is installed, the key is transferred to your Apple Watch automatically.",
        ],
        "download": "Download",
        "testflight": "Get it on TestFlight",
        "soon": "Coming soon",
        "support_h2": "Support & Contact",
        "support_text": "FiveQ is a free side project. If you like it, I'd be happy about a coffee ☕ or a star on GitHub.",
        "contact_text": "Have feature requests, feedback, or want to discuss new projects? Feel free to reach out at <a href=\"mailto:FiveQ@mail.mbaas.de\">FiveQ@mail.mbaas.de</a> or open a ticket in <a href=\"https://github.com/mbaas2/FiveQThoughts/issues\">GitHub Issues</a>.",
        "coffee": "☕ Buy me a coffee",
        "sponsors": "💙 GitHub Sponsors",
        "email_btn": "✉️ FiveQ@mail.mbaas.de",
        "issues_btn": "💬 GitHub Issues",
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
    toggle_label = "Design wechseln (Hell/Dunkel)" if lang == "de" else "Toggle theme (Light/Dark)"
    return f"""<header class="site-header"><div class="wrap">
  <a class="logo" href="./"><span class="bolt">⚡</span> FiveQ</a>
  <nav class="site-nav">{nav}<a class="lang-switch" href="../{other_code}/" hreflang="{other_code}">{other_name}</a><button type="button" class="theme-toggle" id="theme-toggle" title="{toggle_label}" aria-label="{toggle_label}">🌓</button></nav>
</div></header>"""


def footer(t):
    return f"""<footer><div class="wrap">
  <div>{t["footer_by"]}<br><span class="note">{link_tb(t["footer_tm"])}</span></div>
  <div><a href="{t["privacy"][0]}">{t["privacy"][1]}</a> · <a href="{t["imprint"][0]}">{t["imprint"][1]}</a> · <a href="{LINKS["repo_desktop"]}">{t["source"]}</a></div>
</div></footer>"""


THEME_SCRIPT = """<script>
(function() {
  var root = document.documentElement;
  var mq = window.matchMedia("(prefers-color-scheme: dark)");
  function currentTheme() {
    var saved = localStorage.getItem("fiveq-theme");
    if (saved === "light" || saved === "dark") return saved;
    return mq.matches ? "dark" : "light";
  }
  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    var btn = document.getElementById("theme-toggle");
    if (btn) btn.textContent = theme === "dark" ? "🌙" : "☀️";
    document.querySelectorAll("picture > source").forEach(function(src) {
      src.media = theme === "dark" ? "all" : "not all";
    });
  }
  applyTheme(currentTheme());
  window.addEventListener("DOMContentLoaded", function() {
    applyTheme(currentTheme());
    var btn = document.getElementById("theme-toggle");
    if (btn) {
      btn.addEventListener("click", function() {
        var next = currentTheme() === "dark" ? "light" : "dark";
        localStorage.setItem("fiveq-theme", next);
        applyTheme(next);
      });
    }
  });
  if (mq.addEventListener) {
    mq.addEventListener("change", function() {
      if (!localStorage.getItem("fiveq-theme")) applyTheme(currentTheme());
    });
  }
})();
</script>"""


ANALYTICS = """<script data-goatcounter="https://mbaas.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>"""


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
{THEME_SCRIPT}
{ANALYTICS}
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


def link_tb(s):
    return escape(s).replace("TheBrain", '<a href="https://www.thebrain.com">TheBrain</a>')

def li(items):
    return "".join(f"<li>{i.format(**LINKS)}</li>" for i in items)


def index(lang):
    t = T[lang]
    ids = t["ids"]
    features = "".join(
        f'<div class="feature"><div class="ico">{i}</div><h3>{escape(h)}</h3><p>{link_tb(p)}</p></div>'
        for i, h, p in t["features"]
    )
    badges = "".join(f'<span class="badge">{escape(b)}</span>' for b in t["badges"])
    body = f"""
<div class="hero"><div class="wrap">
  <h1>{t["hero_h1"]}</h1>
  <p class="lead">{link_tb(t["hero_lead"])}</p>
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
    <div>{img(f"mac-{lang}", t["mac_alt"], t=t)}</div>
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
  <h2>{t["install_h2"]}</h2><p class="sub">{link_tb(t["install_sub"])}</p>
  <div class="install">
    <div class="card"><h3>{t["install_keys_h3"]}</h3><ul>{li(t["install_keys"])}</ul></div>
    <div class="card"><h3>{t["install_win_h3"]}</h3><ol>{li(t["install_win"])}</ol><p class="note">{escape(t["install_win_note"])}</p>{button(LINKS["windows_download"], t["download"], True, t)}</div>
    <div class="card"><h3>{t["install_mac_h3"]}</h3><ol>{li(t["install_mac"])}</ol><p class="note">{escape(t["install_mac_note"])}</p>{button(LINKS["mac_download"], t["download"], True, t)}</div>
    <div class="card"><h3>{t["install_ios_h3"]}</h3><ol>{li(t["install_ios"])}</ol>{button(LINKS["testflight"], t["testflight"], True, t)}</div>
  </div>
</div></section>

<section id="{ids["support"]}" class="support"><div class="wrap">
  <h2>{escape(t["support_h2"])}</h2>
  <p class="sub">{escape(t["support_text"])}</p>
  <p class="sub">{t["contact_text"]}</p>
  <div class="cta">{button(LINKS["coffee"], t["coffee"], True, t)}{button(LINKS["sponsors"], t["sponsors"], False, t)}{button(LINKS["email"], t["email_btn"], False, t)}{button(LINKS["issues"], t["issues_btn"], False, t)}</div>
</div></section>
"""
    return page(t, lang, t["title"], body, t["description"])


PRIVACY = {
    "de": ("Datenschutzerklärung – FiveQ", """
<h1>Datenschutzerklärung</h1>
<p class="note">Stand: November 2026</p>

<h2>1. Verantwortlicher</h2>
<p>Verantwortlicher im Sinne der DSGVO:<br>
DLS Software &amp; Beratung GmbH · Michael Baas<br>
Kinzigstraße 10a<br>
63584 Gründau, Deutschland<br>
E-Mail: <a href="mailto:info@dls-software.de">info@dls-software.de</a> · Tel.: +49 (0)160 5887507</p>

<h2>2. Kurz gesagt</h2>
<p>FiveQ (iPhone, Apple Watch) und FiveQThoughts (Mac, Windows) erheben keine personenbezogenen Daten für uns. Es gibt kein Tracking, keine Analyse-Tools (auch kein Umami), keine Cookies, keine Werbung und keine eigenen Backend-Server.</p>

<h2>3. Bereitstellung dieser Website (GitHub Pages)</h2>
<p>Diese Website wird über <strong>GitHub Pages</strong> gehostet, einen Dienst der GitHub Inc., 88 Colin P. Kelly Jr. St., San Francisco, CA 94107, USA (bzw. GitHub B.V., Vijzelstraat 68–72, 1017 HL Amsterdam, Niederlande).</p>
<p>Beim Aufruf dieser Website übermittelt Ihr Browser technisch notwendige Zugriffsdaten (insbesondere IP-Adresse, Datum und Uhrzeit des Abrufs, aufgerufene URL, Referrer-URL sowie Browser-/Betriebssystem-Informationen) an die Server von GitHub, um die Seiten auszuliefern und die Sicherheit des Betriebs zu gewährleisten (Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO – berechtigtes Interesse an einer sicheren und zuverlässigen Bereitstellung). Wir selbst haben keinen Zugriff auf diese Server-Logfiles, setzen keine Cookies ein. Weitere Informationen finden Sie in der <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement">Datenschutzerklärung von GitHub</a>.</p>
<h3>Reichweitenmessung (GoatCounter)</h3>
<p>Diese Website nutzt <strong>GoatCounter</strong>, einen datensparsamen Dienst zur Reichweitenmessung. GoatCounter setzt <strong>keine Cookies</strong> und speichert keine personenbezogenen Daten: Es werden nur aggregierte Statistiken (z.&nbsp;B. Anzahl der Aufrufe je Seite, verwendete Browser, Herkunfts-Website) gespeichert, aus denen sich einzelne Besucher nicht identifizieren lassen. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an der statistischen Auswertung der Nutzung). Weitere Informationen: <a href="https://www.goatcounter.com/help/gdpr">goatcounter.com/help/gdpr</a>.</p>

<h2>4. Welche Daten verarbeiten die Apps (FiveQ &amp; FiveQThoughts)?</h2>
<ul>
<li><strong>API-Schlüssel:</strong> Ihr TheBrain-API-Key wird ausschließlich lokal auf Ihrem Gerät gespeichert (iPhone/Apple Watch: geschützte App-Einstellungen; Desktop: lokale Konfigurationsdatei).</li>
<li><strong>Quick Thoughts:</strong> Texte, Links und Bilder, die Sie anlegen, bearbeiten oder ansehen, werden direkt zwischen Ihrem Gerät und TheBrain übertragen – entweder an Ihre lokale TheBrain-Desktop-App (<code>localhost</code>) oder an die TheBrain Cloud (<code>api.bra.in</code>). Für die Verarbeitung dort gilt die Datenschutzerklärung von TheBrain Technologies LP.</li>
<li><strong>Spracheingabe:</strong> Diktate auf iPhone und Apple Watch werden über die System-Spracherkennung von Apple verarbeitet (siehe Datenschutzhinweise von Apple).</li>
<li><strong>Apple Watch:</strong> Der API-Key wird direkt von Ihrem iPhone über Apples verschlüsselte <code>WatchConnectivity</code>-Verbindung an Ihre gekoppelte Apple Watch übertragen.</li>
</ul>

<h2>5. Kontaktaufnahme per E-Mail</h2>
<p>Wenn Sie uns per E-Mail kontaktieren, werden die von Ihnen übermittelten Angaben (Name, E-Mail-Adresse, Nachrichteninhalt) ausschließlich zur Bearbeitung Ihrer Anfrage verarbeitet (Art. 6 Abs. 1 lit. b bzw. lit. f DSGVO). Eine Weitergabe an Dritte findet nicht statt; die Daten werden nach Abschluss der Bearbeitung gelöscht, sofern keine gesetzlichen Aufbewahrungspflichten bestehen.</p>

<h2>6. Ihre Rechte</h2>
<p>Sie haben gegenüber uns folgende Rechte hinsichtlich Ihrer personenbezogenen Daten: Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16 DSGVO), Löschung (Art. 17 DSGVO), Einschränkung der Verarbeitung (Art. 18 DSGVO), Widerspruch gegen die Verarbeitung (Art. 21 DSGVO) sowie Datenübertragbarkeit (Art. 20 DSGVO). Wenden Sie sich hierzu bitte an <a href="mailto:info@dls-software.de">info@dls-software.de</a>.</p>
<p>Sie haben außerdem das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren. Zuständige Aufsichtsbehörde in Hessen ist der <a href="https://datenschutz.hessen.de">Hessische Beauftragte für Datenschutz und Informationsfreiheit</a>.</p>
"""),
    "en": ("Privacy Policy – FiveQ", """
<h1>Privacy Policy</h1>
<p class="note">Last updated: November 2026</p>

<h2>1. Controller</h2>
<p>Controller within the meaning of the GDPR:<br>
DLS Software &amp; Beratung GmbH · Michael Baas<br>
Kinzigstraße 10a<br>
63584 Gründau, Germany<br>
Email: <a href="mailto:info@dls-software.de">info@dls-software.de</a> · Phone: +49 (0)160 5887507</p>

<h2>2. In short</h2>
<p>FiveQ (iPhone, Apple Watch) and FiveQThoughts (Mac, Windows) do not collect any personal data for us. There is no tracking, no analytics, no cookies, no advertising and no backend server of our own.</p>

<h2>3. Website hosting (GitHub Pages)</h2>
<p>This website is hosted on <strong>GitHub Pages</strong>, a service provided by GitHub Inc., 88 Colin P. Kelly Jr. St., San Francisco, CA 94107, USA (or GitHub B.V., Vijzelstraat 68–72, 1017 HL Amsterdam, Netherlands).</p>
<p>When you visit this website, your browser automatically transmits technically required access data (such as IP address, date and time of access, requested URL, referrer URL and browser/OS information) to GitHub's servers to deliver the site and ensure operational security (legal basis: Art. 6(1)(f) GDPR – legitimate interest). We do not have access to these server logs, set no cookies. For details, see <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub's Privacy Statement</a>.</p>
<h3>Audience measurement (GoatCounter)</h3>
<p>This website uses <strong>GoatCounter</strong>, a privacy-friendly analytics service. GoatCounter sets <strong>no cookies</strong> and stores no personal data: only aggregated statistics (e.g. number of views per page, browsers used, referring website) are stored, from which individual visitors cannot be identified. Legal basis is Art. 6(1)(f) GDPR (legitimate interest in statistically evaluating usage). More information: <a href="https://www.goatcounter.com/help/gdpr">goatcounter.com/help/gdpr</a>.</p>

<h2>4. What data do the apps (FiveQ &amp; FiveQThoughts) process?</h2>
<ul>
<li><strong>API key:</strong> Your TheBrain API key is stored exclusively locally on your device (iPhone/Apple Watch: app settings; desktop: local configuration file).</li>
<li><strong>Quick Thoughts:</strong> Text, links and images you create, edit or view are transferred directly between your device and TheBrain – either your local TheBrain desktop app (<code>localhost</code>) or TheBrain Cloud (<code>api.bra.in</code>). TheBrain Technologies LP's privacy policy applies to processing there.</li>
<li><strong>Dictation:</strong> Dictation on iPhone and Apple Watch is processed by Apple's system speech recognition (see Apple's privacy information).</li>
<li><strong>Apple Watch:</strong> The API key is transferred directly from your iPhone to your paired Apple Watch via Apple's WatchConnectivity.</li>
</ul>

<h2>5. Contact by email</h2>
<p>If you contact us by email, the data you provide (name, email address, message content) will be processed solely to handle your inquiry (Art. 6(1)(b) and (f) GDPR). It will not be shared with third parties and will be deleted once your inquiry has been resolved, unless statutory retention obligations apply.</p>

<h2>6. Your rights</h2>
<p>Under the GDPR, you have the right of access (Art. 15), rectification (Art. 16), erasure (Art. 17), restriction of processing (Art. 18), objection (Art. 21) and data portability (Art. 20). To exercise these rights, please contact <a href="mailto:info@dls-software.de">info@dls-software.de</a>. You also have the right to lodge a complaint with a supervisory authority (in Hesse: <a href="https://datenschutz.hessen.de">Hessischer Beauftragter für Datenschutz und Informationsfreiheit</a>).</p>
"""),
}

IMPRINT_DE = ("Impressum – FiveQ", """
<h1>Impressum</h1>
<h2>Angaben gemäß § 5 DDG</h2>
<p>Michael Baas<br>
DLS Software &amp; Beratung GmbH<br>
Kinzigstraße 10a<br>
63584 Gründau<br>
Deutschland</p>

<h2>Kontakt</h2>
<p>E-Mail: <a href="mailto:info@dls-software.de">info@dls-software.de</a><br>
Telefon: +49 (0)160 5887507</p>

<h2>Umsatzsteuer-Identifikationsnummer</h2>
<p>Umsatzsteuer-Identifikationsnummer gemäß § 27 a Umsatzsteuergesetz:<br>
DE273774390</p>

<h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
<p>Michael Baas<br>
Kinzigstraße 10a<br>
63584 Gründau<br>
Deutschland</p>

<h2>Haftung für Links</h2>
<p>Trotz sorgfältiger inhaltlicher Kontrolle übernehmen wir keine Haftung für die Inhalte externer Links. Für den Inhalt der verlinkten Seiten sind ausschließlich deren Betreiber verantwortlich.</p>
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
