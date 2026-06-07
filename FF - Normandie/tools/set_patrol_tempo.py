#!/usr/bin/env python3
"""Adjust patrol thresholds and manpower regeneration per town.

Anchors on the existing JWK_TownMilitaryActivityComponent block (which we
created earlier with m_iManpower) and ADDS the patrol/regen attributes.
"""
import re
from pathlib import Path

ROOT = Path(r"C:\Users\benbo\Documents\My Games\ArmaReforgerWorkbench\addons\FF - Normandie\Worlds\FF_Normandie_Layers\towns")

# (layer_filename, TC_instance, patrol_min, patrol_max, regen_rate)
TOWNS = [
    # 4 bourgs principaux : patrouilles rapides, bonne logistique
    ("BrecourtManor.layer",  "TC_Komsomolsk",   5, 40, 0.5),
    ("Hubert.layer",         "TC_Gorshkovo",    5, 40, 0.5),
    ("LaRue.layer",          "TC_Michurino",    5, 40, 0.5),
    ("SainteMere.layer",     "TC_Kamensk",      5, 40, 0.5),
    # 8 villages : patrouilles lentes, isolés
    ("Beuzeville.layer",     "TC_SosnovyMys3",  15, 60, 0.2),
    ("Carquebut.layer",      "TC_SosnovyMys2",  15, 60, 0.2),
    ("Foucarville.layer",    "TC_Mineraly2",    15, 60, 0.2),
    ("Picauville.layer",     "TC_SosnovyMys",   15, 60, 0.2),
    ("Quineville.layer",     "TC_Mineraly3",    15, 60, 0.2),
    ("Reuville.layer",       "TC_SosnovyMys4",  15, 60, 0.2),
    ("SaintCome.layer",      "TC_Mineraly",     15, 60, 0.2),
    ("SaintMarcouf.layer",   "TC_Mineraly4",    15, 60, 0.2),
]

def add_patrol(text: str, tc_inst: str, p_min: int, p_max: int, regen: float) -> tuple[str, str]:
    """Add patrol attrs inside the existing JWK_TownMilitaryActivityComponent
    block — right after m_iManpower X."""
    if 'm_iPatrolMinThreatLevel' in text:
        return text, "already has patrol attrs"

    pat = re.compile(
        r'(JWK_TownMilitaryActivityComponent "\{64E347579D05582B\}" \{\n   m_iManpower \d+)\n'
    )
    inj = (
        f'\n   m_iPatrolMinThreatLevel {p_min}\n'
        f'   m_iPatrolMaxThreatLevel {p_max}\n'
        f'   m_fManpowerRegenerationRate {regen}\n'
    )
    new, n = pat.subn(r'\1' + inj, text, count=1)
    if n == 0:
        return text, "regex NOT FOUND"
    return new, f"injected min={p_min} max={p_max} regen={regen}"

def main():
    print("=== PATROL TEMPO ===")
    for fname, tc, pmin, pmax, regen in TOWNS:
        path = ROOT / fname
        text = path.read_text(encoding="utf-8")
        new, status = add_patrol(text, tc, pmin, pmax, regen)
        print(f"  {fname:<25} -> {status}")
        if new != text:
            path.write_text(new, encoding="utf-8")

if __name__ == "__main__":
    main()
