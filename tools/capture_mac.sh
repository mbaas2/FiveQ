#!/bin/bash
# Captures the native macOS window of FiveQThoughts in light and dark mode.
# Usage: capture_mac.sh <lang> <outdir> <host-binary> <winid-binary> [backend]
set -e
LANG_CODE=$1; OUT=$2; HOST=$3; WINID=$4; BACKEND=${5:-http://127.0.0.1:11599}
mkdir -p "$OUT"
for THEME in light dark; do
  curl -s -X POST "$BACKEND/api/config" -H 'Content-Type: application/json' \
    -d "{\"language\":\"$LANG_CODE\",\"theme\":\"$THEME\",\"languageOnly\":true}" > /dev/null
  "$HOST" --url "$BACKEND" >/dev/null 2>&1 &
  PID=$!
  W=""
  for i in $(seq 1 20); do W=$("$WINID" $PID); [ -n "$W" ] && break; perl -e 'select(undef,undef,undef,0.5)'; done
  perl -e 'select(undef,undef,undef,9)'   # let thoughts + images load
  screencapture -l "$W" -o "$OUT/mac-$LANG_CODE-$THEME.png"
  kill $PID; wait $PID 2>/dev/null || true
  echo "captured $OUT/mac-$LANG_CODE-$THEME.png"
done
