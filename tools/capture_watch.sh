#!/bin/bash
# Captures Apple Watch simulator screenshots of FiveQWatch (Debug build for -screenshotTab).
# Usage: capture_watch.sh <lang> <outdir> <watch-udid> <path/to/FiveQWatch.app>
set -e
L=$1; OUT=$2; D=$3; APP=$4
BUNDLE=app.fiveq.watchkitapp
case $L in de) LOC=de_DE;; *) LOC=en_US;; esac
mkdir -p "$OUT"
# Reuse a running watch – a fresh boot of the watchOS simulator can take minutes.
if ! timeout 30 xcrun simctl list devices booted | grep -q "$D"; then
  timeout 120 xcrun simctl boot "$D"
fi
timeout 600 xcrun simctl bootstatus "$D" -b >/dev/null
timeout 120 xcrun simctl install "$D" "$APP"
xcrun simctl status_bar "$D" override --time 9:41 2>/dev/null || true
shot() { # name tab
  xcrun simctl terminate "$D" $BUNDLE 2>/dev/null || true
  timeout 60 xcrun simctl launch "$D" $BUNDLE -screenshotTab "$2" -AppleLanguages "($L)" -AppleLocale $LOC >/dev/null
  perl -e 'select(undef,undef,undef,8)'
  xcrun simctl io "$D" screenshot "$OUT/watch-$L-$1.png" >/dev/null 2>&1
  echo "captured watch-$L-$1.png"
}
shot new 0
shot list 1
