"""
Batch ElevenLabs TTS -> WAV 48kHz stereo PCM 16-bit for FF_WW2_FrenchVoices.

Consumes BOTH:
- Translations_FR.csv (135 NORTHCOM-style radio protocol lines)
- Speech_FR.csv (131 FF speech dialogue lines)

Routes each line to a different voice based on narrative context:
- "soldier"   : radio protocol chatter + military police + digits
- "officer"   : resistance officer dialogue, jobs, quests
- "player"    : player character + player actions + passphrases
- "operative" : fellow resistance fighter
- "civilian1/2/3" : rotated across AmbientCivilian lines for diversity

Each voice is configured via env vars (or --voice-* flags). Missing voice IDs
fall back to ELEVENLABS_VOICE_ID (single-voice mode).

Usage (PowerShell):
    $env:ELEVENLABS_API_KEY = "sk_..."
    $env:ELEVENLABS_VOICE_SOLDIER   = "<voice_id_for_soldier>"     # e.g. Anthony
    $env:ELEVENLABS_VOICE_OFFICER   = "<voice_id_for_officer>"     # e.g. Nicolas
    $env:ELEVENLABS_VOICE_PLAYER    = "<voice_id_for_player>"      # e.g. Denis
    $env:ELEVENLABS_VOICE_OPERATIVE = "<voice_id_for_operative>"   # e.g. Julien
    $env:ELEVENLABS_VOICE_CIVILIAN1 = "<voice_id_for_civ1>"        # e.g. Sebastien
    $env:ELEVENLABS_VOICE_CIVILIAN2 = "<voice_id_for_civ2>"        # e.g. Frederic
    $env:ELEVENLABS_VOICE_CIVILIAN3 = "<voice_id_for_civ3>"        # e.g. Benjamin
    python generate_voices.py --limit 5    # smoke test
    python generate_voices.py              # full run

Flags:
    --voice-soldier / --voice-officer / --voice-player / etc.   override env
    --voice-id <id>      fallback for all roles (single voice mode)
    --stability 0.5      0..1, higher = more consistent (default 0.5)
    --similarity 0.75    0..1, higher = closer to reference (default 0.75)
    --style 0.3          0..1, higher = more expressive (default 0.3)
    --model eleven_multilingual_v2   default model
    --force              Re-generate even if wav already exists
    --limit N            Only process first N rows of EACH CSV (test mode)
    --only radio|speech  Restrict to one CSV
    --dry-run            Print actions but don't call API

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

# Locate ffmpeg — winget install Gyan.FFmpeg drops it under WinGet/Links.
FFMPEG = (
    shutil.which("ffmpeg")
    or shutil.which("ffmpeg.exe")
    or str(Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "WinGet" / "Links" / "ffmpeg.exe")
)

ROOT = Path(__file__).resolve().parent
TRANSLATIONS_CSV = ROOT / "Translations_FR.csv"     # NORTHCOM-style radio protocol
SPEECH_CSV = ROOT / "Speech_FR.csv"                 # FF SpeechBank dialogues

RADIO_SAMPLES_ROOT = ROOT / "Sounds" / "RadioProtocol" / "Samples" / "FR" / "Male1"
SPEECH_SAMPLES_ROOT = ROOT / "Sounds" / "Voices" / "Samples" / "FR"

API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
OUTPUT_FORMAT = "mp3_44100_128"   # universal across all tiers (pcm_* requires Pro)

# Map FF SpeechBank -> voice role.
# AmbientCivilian gets a tuple to rotate across multiple voices for diversity.
BANK_TO_ROLE: dict[str, str | tuple[str, ...]] = {
    "AmbientCivilian": ("civilian1", "civilian2", "civilian3"),
    "Default": "soldier",
    "MilitaryPolice": "soldier",
    "Passphrases": "player",
    "Player": "player",
    "PlayerActions": "player",
    "Prisoner": "operative",
    "ResistanceOfficer": "officer",
    "ResistanceOfficerJobs": "officer",
    "ResistanceOfficerQuests": "officer",
    "ResistanceOperative": "operative",
}

ROLE_ENV_VARS = {
    "soldier": "ELEVENLABS_VOICE_SOLDIER",
    "officer": "ELEVENLABS_VOICE_OFFICER",
    "player": "ELEVENLABS_VOICE_PLAYER",
    "operative": "ELEVENLABS_VOICE_OPERATIVE",
    "civilian1": "ELEVENLABS_VOICE_CIVILIAN1",
    "civilian2": "ELEVENLABS_VOICE_CIVILIAN2",
    "civilian3": "ELEVENLABS_VOICE_CIVILIAN3",
}

# Emotion tag prefix per role — only applied when --tag-role is set (requires eleven_v3).
ROLE_TAGS = {
    "soldier":   "[screaming][shouting][angry][combat][war zone]",
    "officer":   "[urgent][commanding][barking]",
    "player":    "[determined][tense][gritty]",
    "operative": "[serious][tense][battle-hardened]",
    "civilian1": "[scared][trembling]",
    "civilian2": "[angry][hostile]",
    "civilian3": "[stressed][nervous]",
}

# Roles whose text should be UPPERCASED before TTS — military shouts hit harder.
SHOUT_ROLES = {"soldier"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate French radio + dialogue voice samples via ElevenLabs.")
    p.add_argument("--api-key", default=os.environ.get("ELEVENLABS_API_KEY"))
    p.add_argument("--voice-id", default=os.environ.get("ELEVENLABS_VOICE_ID"), help="Fallback voice for any role missing a specific id")
    for role, env in ROLE_ENV_VARS.items():
        p.add_argument(f"--voice-{role}", default=os.environ.get(env), help=f"voice id for {role}")
    p.add_argument("--model", default="eleven_v3")
    # Validated 1944 hostile-territory tuning:
    # HIGH stability (0.75) = sharp, projected, consistent (military bark, no drift)
    # HIGH style (0.95) = max aggression / emotional exaggeration
    # Lower stability causes "drugged" drift — only useful for very calm narration.
    p.add_argument("--stability", type=float, default=0.75)
    p.add_argument("--similarity", type=float, default=0.85)
    p.add_argument("--style", type=float, default=0.95)
    p.add_argument("--tag-role", action="store_true", default=True,
                   help="Wrap text with emotion tags per role (default on; --no-tag-role to disable).")
    p.add_argument("--no-tag-role", action="store_false", dest="tag_role")
    p.add_argument("--force", action="store_true", help="Re-generate existing wavs")
    p.add_argument("--limit", type=int, default=0, help="Only process first N rows of each CSV")
    p.add_argument("--only", choices=["radio", "speech"], default=None)
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def resolve_voice(role: str, args: argparse.Namespace) -> str | None:
    """Return the voice id for a given role, falling back to --voice-id."""
    specific = getattr(args, f"voice_{role}", None)
    return specific or args.voice_id


def resolve_radio_path(category: str, subcategory: str, wav_name: str) -> Path:
    if subcategory:
        return RADIO_SAMPLES_ROOT / category / subcategory / wav_name
    return RADIO_SAMPLES_ROOT / category / wav_name


def resolve_speech_path(bank: str, sample_name: str) -> Path:
    return SPEECH_SAMPLES_ROOT / bank / f"{sample_name}.wav"


def synth_one(text: str, voice_id: str, args: argparse.Namespace) -> bytes:
    url = API_URL.format(voice_id=voice_id) + f"?output_format={OUTPUT_FORMAT}"
    headers = {
        "xi-api-key": args.api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
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


def mp3_to_wav(mp3_bytes: bytes, out_path: Path) -> None:
    """Decode ElevenLabs MP3 -> resample to 48kHz stereo PCM_S16LE WAV
    matching NORTHCOM's format (verified via xxd on Jawohl.wav)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-f", "mp3", "-i", "pipe:0",
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le",
        str(out_path),
    ]
    proc = subprocess.run(cmd, input=mp3_bytes, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {proc.stderr.decode(errors='replace')[:500]}")


def process_row(idx: int, row: dict, out_path: Path, role: str, voice_id: str,
                args: argparse.Namespace, totals: dict) -> None:
    text = row.get("FR_Translation", "").strip()
    if not text:
        print(f"[{idx:3}] SKIP empty translation: {out_path.name}")
        totals["skipped"] += 1
        return
    if not voice_id:
        print(f"[{idx:3}] SKIP no voice id for role={role}: {out_path.name}")
        totals["skipped"] += 1
        return
    if out_path.exists() and not args.force:
        print(f"[{idx:3}] EXISTS  {out_path.relative_to(ROOT)}")
        totals["skipped"] += 1
        return

    # Uppercase shouted roles to push TTS intonation harder, then optionally
    # prefix emotion tags for v3 model (military bark, scared civilian, etc.).
    body = text.upper() if args.tag_role and role in SHOUT_ROLES else text
    tagged = f"{ROLE_TAGS.get(role, '')} {body}".strip() if args.tag_role else body
    label = "DRY-RUN" if args.dry_run else f"GEN[{role}]"
    print(f"[{idx:3}] {label:13}  {out_path.relative_to(ROOT)}  <- {tagged!r}")
    if args.dry_run:
        return
    try:
        mp3 = synth_one(tagged, voice_id, args)
        mp3_to_wav(mp3, out_path)
        totals["done"] += 1
    except Exception as e:
        print(f"      FAILED: {e}", file=sys.stderr)
        totals["failed"] += 1


def run_radio(args: argparse.Namespace, totals: dict) -> None:
    if not TRANSLATIONS_CSV.exists():
        print(f"ERROR: {TRANSLATIONS_CSV} not found.", file=sys.stderr)
        return
    voice_id = resolve_voice("soldier", args)
    with TRANSLATIONS_CSV.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if args.limit:
        rows = rows[: args.limit]
    print(f"\n=== Radio Protocol ({len(rows)} rows, voice={voice_id or '<MISSING>'}) ===")
    for i, row in enumerate(rows, 1):
        out = resolve_radio_path(
            row["Category"].strip(),
            row["Subcategory"].strip(),
            row["WavName"].strip(),
        )
        process_row(i, row, out, "soldier", voice_id, args, totals)


def run_speech(args: argparse.Namespace, totals: dict) -> None:
    if not SPEECH_CSV.exists():
        print(f"ERROR: {SPEECH_CSV} not found.", file=sys.stderr)
        return
    with SPEECH_CSV.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if args.limit:
        rows = rows[: args.limit]
    print(f"\n=== FF Speech ({len(rows)} rows) ===")
    civ_counter = 0
    for i, row in enumerate(rows, 1):
        bank = row["Bank"].strip()
        sample = row["SampleName"].strip()
        role_or_rotation = BANK_TO_ROLE.get(bank, "soldier")
        if isinstance(role_or_rotation, tuple):
            role = role_or_rotation[civ_counter % len(role_or_rotation)]
            civ_counter += 1
        else:
            role = role_or_rotation
        voice_id = resolve_voice(role, args)
        out = resolve_speech_path(bank, sample)
        process_row(i, row, out, role, voice_id, args, totals)


def print_voice_summary(args: argparse.Namespace) -> None:
    print("\nVoice assignments:")
    for role in ROLE_ENV_VARS:
        vid = resolve_voice(role, args)
        marker = "[OK]" if vid else "[--]"
        print(f"  {marker} {role:11} -> {vid or '<missing>'}")


def main() -> int:
    args = parse_args()
    if not args.api_key:
        print("ERROR: set ELEVENLABS_API_KEY.", file=sys.stderr)
        return 2
    print_voice_summary(args)
    totals = {"done": 0, "skipped": 0, "failed": 0}
    if args.only != "speech":
        run_radio(args, totals)
    if args.only != "radio":
        run_speech(args, totals)
    print(f"\nDone. generated={totals['done']}  skipped={totals['skipped']}  failed={totals['failed']}")
    return 0 if totals["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
