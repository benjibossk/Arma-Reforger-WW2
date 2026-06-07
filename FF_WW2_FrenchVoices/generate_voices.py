"""
Batch ElevenLabs TTS -> WAV 48kHz stereo PCM 16-bit for FF_WW2_FrenchVoices.

Reads Translations_FR.csv, calls the ElevenLabs API for each FR_Translation,
pipes the PCM 44.1kHz output through ffmpeg to convert to 48kHz stereo
PCM_S16LE WAV matching the NORTHCOM/Reforger expected format.

Usage:
    set ELEVENLABS_API_KEY=sk_xxx
    set ELEVENLABS_VOICE_ID=<voice_id>      # any French male voice
    python generate_voices.py

Optional:
    --voice-id <id>      Override env voice id
    --stability 0.5      0..1, higher = more consistent (default 0.5)
    --similarity 0.75    0..1, higher = closer to reference (default 0.75)
    --style 0.3          0..1, higher = more expressive (default 0.3)
    --model eleven_multilingual_v2   default model (best for French)
    --force              Re-generate even if wav already exists
    --limit N            Only process first N rows (for test)
    --dry-run            Print actions but don't call API

Voice id suggestions for French male WW2 chatter (ElevenLabs voice library):
    - "Antoni" (multilingual, French support)
    - "Adam" (deep, authoritative)
    - "Sam" (younger, more agile)
    - any custom French voice clone of a 1940s recording for max immersion

Requires:
    pip install requests
    ffmpeg in PATH
"""
from __future__ import annotations

import argparse
import csv
import os
import shutil
import subprocess
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "Translations_FR.csv"
SAMPLES_ROOT = ROOT / "Sounds" / "RadioProtocol" / "Samples" / "FR" / "Male1"

API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
OUTPUT_FORMAT = "pcm_44100"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate French radio voice samples via ElevenLabs.")
    p.add_argument("--voice-id", default=os.environ.get("ELEVENLABS_VOICE_ID"))
    p.add_argument("--api-key", default=os.environ.get("ELEVENLABS_API_KEY"))
    p.add_argument("--model", default="eleven_multilingual_v2")
    p.add_argument("--stability", type=float, default=0.5)
    p.add_argument("--similarity", type=float, default=0.75)
    p.add_argument("--style", type=float, default=0.3)
    p.add_argument("--force", action="store_true", help="Re-generate existing wavs")
    p.add_argument("--limit", type=int, default=0, help="Only process first N rows")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def resolve_output_path(category: str, subcategory: str, wav_name: str) -> Path:
    """Translations CSV stores Subcategory either as 'BailOut' or as a nested path
    like 'FactionAndObject/Civilian/Character'. Reproduce the on-disk layout."""
    if subcategory:
        return SAMPLES_ROOT / category / subcategory / wav_name
    return SAMPLES_ROOT / category / wav_name


def synth_one(text: str, args: argparse.Namespace) -> bytes:
    url = API_URL.format(voice_id=args.voice_id) + f"?output_format={OUTPUT_FORMAT}"
    headers = {
        "xi-api-key": args.api_key,
        "Content-Type": "application/json",
        "Accept": "audio/pcm",
    }
    body = {
        "text": text,
        "model_id": args.model,
        "voice_settings": {
            "stability": args.stability,
            "similarity_boost": args.similarity,
            "style": args.style,
            "use_speaker_boost": True,
        },
    }
    r = requests.post(url, headers=headers, json=body, timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"ElevenLabs API error {r.status_code}: {r.text[:500]}")
    return r.content


def pcm_to_wav(pcm_bytes: bytes, out_path: Path) -> None:
    """Wrap raw PCM 44.1kHz mono 16-bit from ElevenLabs into a WAV file
    resampled to 48kHz stereo PCM_S16LE — matches NORTHCOM's format."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "s16le", "-ar", "44100", "-ac", "1",  # input: raw PCM mono 44.1kHz
        "-i", "pipe:0",
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le",  # output: 48kHz stereo PCM s16le
        str(out_path),
    ]
    proc = subprocess.run(cmd, input=pcm_bytes, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {proc.stderr.decode(errors='replace')[:500]}")


def main() -> int:
    args = parse_args()
    if not args.voice_id or not args.api_key:
        print("ERROR: set ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID (or pass --voice-id / --api-key).", file=sys.stderr)
        return 2
    if not shutil.which("ffmpeg") and not args.dry_run:
        print("ERROR: ffmpeg not in PATH.", file=sys.stderr)
        return 2
    if not CSV_PATH.exists():
        print(f"ERROR: {CSV_PATH} not found.", file=sys.stderr)
        return 2

    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    if args.limit:
        rows = rows[: args.limit]

    print(f"Loaded {len(rows)} rows from {CSV_PATH.name}")
    print(f"Voice: {args.voice_id}  Model: {args.model}  Out: {SAMPLES_ROOT}")
    print()

    done = skipped = failed = 0
    for i, row in enumerate(rows, 1):
        cat = row["Category"].strip()
        subcat = row["Subcategory"].strip()
        wav = row["WavName"].strip()
        text = row["FR_Translation"].strip()
        out = resolve_output_path(cat, subcat, wav)

        if not text:
            print(f"[{i:3}/{len(rows)}] SKIP empty translation: {wav}")
            skipped += 1
            continue
        if out.exists() and not args.force:
            print(f"[{i:3}/{len(rows)}] EXISTS  {out.relative_to(ROOT)}")
            skipped += 1
            continue

        action = "DRY-RUN" if args.dry_run else "GEN    "
        print(f"[{i:3}/{len(rows)}] {action} {out.relative_to(ROOT)}  <- {text!r}")

        if args.dry_run:
            continue

        try:
            pcm = synth_one(text, args)
            pcm_to_wav(pcm, out)
            done += 1
        except Exception as e:
            print(f"          FAILED: {e}", file=sys.stderr)
            failed += 1

    print()
    print(f"Done. generated={done}  skipped={skipped}  failed={failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
