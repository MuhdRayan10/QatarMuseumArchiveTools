#!/usr/bin/env bash
set -e

DEST="$HOME/bin"
PROFILE="$HOME/.zshrc"
FFMPEG_URL="https://www.osxexperts.net/ffmpeg711arm.zip"
FFPROBE_URL="https://www.osxexperts.net/ffprobe711arm.zip"
TMPDIR=$(mktemp -d)

mkdir -p "$DEST"

echo "Downloading ffmpeg…"
curl -L "$FFMPEG_URL"   -o "$TMPDIR/ffmpeg.zip"
echo "Downloading ffprobe…"
curl -L "$FFPROBE_URL"  -o "$TMPDIR/ffprobe.zip"

echo "Unpacking…"
unzip -q "$TMPDIR/ffmpeg.zip"   -d "$TMPDIR"
unzip -q "$TMPDIR/ffprobe.zip"  -d "$TMPDIR"

FFMPEG_BIN=$(find "$TMPDIR" -type f -name ffmpeg  | head -n1)
FFPROBE_BIN=$(find "$TMPDIR" -type f -name ffprobe | head -n1)

if [[ ! -f "$FFMPEG_BIN" ]]; then
  echo "ERROR"
  exit 1
fi
if [[ ! -f "$FFPROBE_BIN" ]]; then
  echo "ERROR"
  exit 1
fi

echo "Installing ffmpeg → $DEST/ffmpeg"
cp "$FFMPEG_BIN"  "$DEST/ffmpeg"
echo "Installing ffprobe → $DEST/ffprobe"
cp "$FFPROBE_BIN" "$DEST/ffprobe"
chmod +x "$DEST/ffmpeg" "$DEST/ffprobe"

if ! grep -q 'export PATH="$HOME/bin:$PATH"' "$PROFILE"; then
  {
    echo ""
    echo "# added by install_ffmpeg.sh"
    echo 'export PATH="$HOME/bin:$PATH"'
  } >> "$PROFILE"
  echo "Patched $PROFILE to include ~/bin"
else
  echo "~/bin already in PATH"
fi

rm -rf "$TMPDIR"

echo "Downloaded successfully"
