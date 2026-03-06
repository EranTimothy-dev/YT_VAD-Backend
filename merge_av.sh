#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <video_file> <audio_file> <output_file> [audio_offset_seconds]"
  echo "Example: $0 video.mp4 audio.m4a out.mp4"
  echo "Example with offset: $0 video.mp4 audio.m4a out.mp4 -0.2"
  exit 1
fi

VIDEO="$1"
AUDIO="$2"
OUT="$3"
OFFSET="${4:-0}"

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing dependency: $1"; exit 1; }; }
need ffmpeg
need ffprobe

tmpdir="$(mktemp -d)"
cleanup() { rm -rf "$tmpdir"; }
trap cleanup EXIT

# Helper: probe a single field
probe() {
  local file="$1" sel="$2" entry="$3"
  ffprobe -v error -select_streams "$sel" -show_entries "$entry" -of default=nk=1:nw=1 "$file" 2>/dev/null | head -n 1 || true
}

# Identify codecs / formats
v_codec="$(probe "$VIDEO" "v:0" "stream=codec_name")"
a_codec="$(probe "$AUDIO" "a:0" "stream=codec_name")"
a_format="$(ffprobe -v error -show_entries format=format_name -of default=nk=1:nw=1 "$AUDIO" 2>/dev/null | head -n 1 || true)"

if [[ -z "$v_codec" ]]; then
  echo "ERROR: No video stream found in: $VIDEO"
  exit 1
fi
if [[ -z "$a_codec" ]]; then
  echo "ERROR: No audio stream found in: $AUDIO"
  exit 1
fi

# 1) Normalize "raw AAC" (ADTS) into M4A so timestamps are sane.
# Your case looks like: format_name == 'aac' and ffmpeg warns estimating duration.
norm_audio="$AUDIO"
if [[ "$a_format" == "aac" ]]; then
  norm_audio="$tmpdir/audio.m4a"
  echo "[info] Audio appears to be raw AAC (format=aac). Remuxing to M4A for proper timestamps..."
  ffmpeg -hide_banner -loglevel error -fflags +genpts -i "$AUDIO" -c copy "$norm_audio"
fi

# Re-probe audio codec after normalization
a_codec="$(probe "$norm_audio" "a:0" "stream=codec_name")"

# 2) Choose container based on codec compatibility
# - MP4 is fine for H264/H265/AV1(video) and AAC/MP3/ALAC(audio) commonly.
# - VP9 in MP4 is often okay, but Opus in MP4 is a frequent fail -> use MKV.
# We'll use MKV if audio is opus/vorbis or output extension isn't mp4/m4a.
ext="${OUT##*.}"
container="mp4"
if [[ "$ext" == "mkv" ]]; then
  container="mkv"
elif [[ "$a_codec" == "opus" || "$a_codec" == "vorbis" ]]; then
  # safest: MKV (or re-encode audio for MP4)
  container="mkv"
fi

# If user requested .mp4 but audio codec is opus/vorbis, we will re-encode audio to AAC to keep mp4.
force_mp4_reencode_audio=false
if [[ "$ext" == "mp4" && ( "$a_codec" == "opus" || "$a_codec" == "vorbis" ) ]]; then
  force_mp4_reencode_audio=true
fi

# 3) Merge strategy:
# Try stream copy first (fast) if it's likely safe.
# If it fails or if we need timestamp smoothing, fall back to re-encode audio only.
out_tmp="$tmpdir/out.$container"

merge_copy() {
  if [[ "$OFFSET" != "0" ]]; then
    ffmpeg -hide_banner -loglevel error \
      -itsoffset "$OFFSET" -i "$norm_audio" -i "$VIDEO" \
      -map 1:v:0 -map 0:a:0 -c copy -shortest "$out_tmp"
  else
    ffmpeg -hide_banner -loglevel error \
      -i "$VIDEO" -i "$norm_audio" \
      -map 0:v:0 -map 1:a:0 -c copy -shortest "$out_tmp"
  fi
}

merge_audio_reencode_sync() {
  # re-encode audio only + fix timestamps/drift
  if [[ "$OFFSET" != "0" ]]; then
    ffmpeg -hide_banner -loglevel error \
      -itsoffset "$OFFSET" -i "$norm_audio" -i "$VIDEO" \
      -map 1:v:0 -map 0:a:0 \
      -c:v copy -c:a aac -b:a 192k \
      -af "aresample=async=1:first_pts=0" \
      -shortest "$out_tmp"
  else
    ffmpeg -hide_banner -loglevel error \
      -i "$VIDEO" -i "$norm_audio" \
      -map 0:v:0 -map 1:a:0 \
      -c:v copy -c:a aac -b:a 192k \
      -af "aresample=async=1:first_pts=0" \
      -shortest "$out_tmp"
  fi
}

echo "[info] Video codec: $v_codec"
echo "[info] Audio codec: $a_codec"
echo "[info] Audio format: $a_format"
echo "[info] Target container: $container (output: $OUT)"

# If MP4 requested but audio codec is opus/vorbis -> re-encode audio to AAC.
if $force_mp4_reencode_audio; then
  echo "[info] Output is MP4 but audio is $a_codec; re-encoding audio to AAC for compatibility..."
  merge_audio_reencode_sync
else
  echo "[info] Trying fast merge (stream copy)..."
  if merge_copy; then
    echo "[info] Stream copy merge succeeded."
  else
    echo "[warn] Stream copy merge failed. Falling back to audio re-encode + timestamp sync..."
    merge_audio_reencode_sync
  fi
fi

# Move to final output path
mkdir -p "$(dirname "$OUT")" 2>/dev/null || true
mv -f "$out_tmp" "$OUT"

echo "[done] Wrote: $OUT"
