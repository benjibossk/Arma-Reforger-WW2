#!/usr/bin/env python3
"""Configure the 4 new hammeaux:
- Rename layer files to French village names
- Update m_sName (was copy-pasted from villages, has wrong name)
- Tune m_iManpower (6) + m_fPopulationSpawnFactor (0.15) for hammeau tier
"""
import re
from pathlib import Path

ROOT = Path(r"C:\Users\benbo\Documents\My Games\ArmaReforgerWorkbench\addons\FF - Normandie\Worlds\FF_Normandie_Layers\towns")

# (old_file, new_file, displayed_french_name)
HAMMEAUX = [
    ("Hammeau1.layer", "Neville.layer",   "Néville-sur-Mer"),
    ("Hammeau2.layer", "Fontenay.layer",  "Fontenay-sur-Mer"),
    ("Hammeau3.layer", "Lestre.layer",    "Lestre"),
    ("Hammeau4.layer", "Crosville.layer", "Crosville-sur-Douve"),
]

MANPOWER  = 6
SPAWN_FAC = 0.15

def update(text: str, name: str) -> str:
    # Update m_sName inside the JWK_NamedLocationComponent (town one — GUID 65C35A2F385D762F)
    text = re.sub(
        r'(JWK_NamedLocationComponent "\{65C35A2F385D762F\}" \{\s*\n\s*m_sName )"[^"]*"',
        r'\g<1>"' + name + '"',
        text, count=1,
    )
    # Update m_iManpower (any current value -> our target)
    text = re.sub(
        r'(JWK_TownMilitaryActivityComponent "\{64E347579D05582B\}" \{\s*\n\s*m_iManpower )\d+',
        r'\g<1>' + str(MANPOWER),
        text, count=1,
    )
    # Update m_fPopulationSpawnFactor (any current value -> our target)
    text = re.sub(
        r'(JWK_TownCiviliansControllerComponent "\{6296F54A892986E3\}" \{\s*\n\s*m_fPopulationSpawnFactor )[\d.]+',
        r'\g<1>' + str(SPAWN_FAC),
        text, count=1,
    )
    return text

print("=== HAMMEAUX CONFIG ===")
for old, new, name in HAMMEAUX:
    src = ROOT / old
    dst = ROOT / new
    if not src.exists():
        print(f"  {old:<18} -> SKIPPED (file missing)")
        continue
    text = src.read_text(encoding="utf-8")
    new_text = update(text, name)
    dst.write_text(new_text, encoding="utf-8")
    if dst != src:
        src.unlink()
    print(f"  {old:<18} -> {new:<22} | m_sName=\"{name}\" mp={MANPOWER} spawn={SPAWN_FAC}")
