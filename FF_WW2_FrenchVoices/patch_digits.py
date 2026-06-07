"""Fill in digit translations for SpeechBank_Default DIGIT_0..9."""
import csv
from pathlib import Path

CSV = Path(__file__).parent / "Speech_FR.csv"

DIGITS = {
    "zero": "zéro",
    "one": "un",
    "two": "deux",
    "three": "trois",
    "four": "quatre",
    "five": "cinq",
    "six": "six",
    "seven": "sept",
    "eight": "huit",
    "nine": "neuf",
}

rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
patched = 0
for r in rows:
    if r["FR_Translation"] == "" and r["SubtitleKey"] in DIGITS:
        r["FR_Translation"] = DIGITS[r["SubtitleKey"]]
        patched += 1

with CSV.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

print(f"Patched {patched} digit translations.")
missing = sum(1 for r in rows if not r["FR_Translation"])
print(f"Still missing: {missing}")
