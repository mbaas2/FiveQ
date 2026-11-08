#!/bin/bash
# Captures iPhone simulator screenshots of FiveQ (Debug build required for -screenshot* args).
# Usage: capture_ios.sh <lang> <outdir> <device-udid> <path/to/FiveQ.app>
set -e
L=$1; OUT=$2; D=$3; APP=$4
mkdir -p "$OUT"
xcrun simctl shutdown "$D" 2>/dev/null || true   # clears leftover system dialogs
xcrun simctl boot "$D"
xcrun simctl bootstatus "$D" -b >/dev/null
xcrun simctl install "$D" "$APP"
xcrun simctl status_bar "$D" override --time 9:41 --batteryState charged --batteryLevel 100 --cellularBars 4 --wifiBars 3
shot() { # name tab theme about
  xcrun simctl ui "$D" appearance "$3"
  xcrun simctl terminate "$D" app.fiveq 2>/dev/null || true
  xcrun simctl launch "$D" app.fiveq -screenshotTab "$2" -screenshotAbout "$4" \
    -fiveq_app_language "$L" -fiveq_app_theme "$3" >/dev/null
  perl -e 'select(undef,undef,undef,7)'
  xcrun simctl io "$D" screenshot "$OUT/ios-$L-$1.png" >/dev/null 2>&1
  echo "captured ios-$L-$1.png"
}
shot list-light 1 light NO
shot list-dark 1 dark NO
shot new-light 0 light NO
shot settings-light 2 light NO
shot about-light 0 light YES
xcrun simctl ui "$D" appearance light
