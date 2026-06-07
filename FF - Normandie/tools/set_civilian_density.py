#!/usr/bin/env python3
"""Set m_fPopulationSpawnFactor on JWK_TownCiviliansControllerComponent
per town. Higher factor = more civilians spawn in the streets.

The actual peak population is computed at runtime as
  pool = sum(JWK_PopulationComponent.m_iCapacity for buildings in POI area)
  active = pool * m_fPopulationSpawnFactor (modulated by daytime curve)

Default in parent is 0.8 (lively peacetime). For occupied 1944 Normandy
we tune down: 0.6 in main towns, 0.4 in small villages.
"""
import re
from pathlib import Path

ROOT = Path(r"C:\Users\benbo\Documents\My Games\ArmaReforgerWorkbench\addons\FF - Normandie\Worlds\FF_Normandie_Layers")

# Component instance GUID inherited from JWK_TownController.et parent prefab
TCC_GUID = "6296F54A892986E3"

# (layer_filename, TC_instance_name, spawn_factor)
TOWNS = [
    # 4 bourgs principaux — rues encore vivantes malgré l'occupation
    ("BrecourtManor.layer",  "TC_Komsomolsk",   0.6),
    ("Hubert.layer",         "TC_Gorshkovo",    0.6),
    ("LaRue.layer",          "TC_Michurino",    0.6),
    ("SainteMere.layer",     "TC_Kamensk",      0.6),
    # 8 villages ruraux — sparse, plus peureux
    ("Beuzeville.layer",     "TC_SosnovyMys3",  0.4),
    ("Carquebut.layer",      "TC_SosnovyMys2",  0.4),
    ("Foucarville.layer",    "TC_Mineraly2",    0.4),
    ("Picauville.layer",     "TC_SosnovyMys",   0.4),
    ("Quineville.layer",     "TC_Mineraly3",    0.4),
    ("Reuville.layer",       "TC_SosnovyMys4",  0.4),
    ("SaintCome.layer",      "TC_Mineraly",     0.4),
    ("SaintMarcouf.layer",   "TC_Mineraly4",    0.4),
]

def add_civilian_factor(text: str, tc_inst: str, factor: float) -> tuple[str, str]:
    """Append JWK_TownCiviliansControllerComponent override inside the existing
    components{} block of the town, after the JWK_TownMilitaryActivityComponent."""
    if 'JWK_TownCiviliansControllerComponent' in text:
        return text, "already has TCC override"

    # Anchor on the JWK_TownMilitaryActivityComponent block end (inserted earlier).
    pat = re.compile(
        r'(JWK_TownEntity ' + re.escape(tc_inst) + r' : "\{64B2F8D8059C97CC\}[^"]+" \{\n'
        r' components \{\n'
        r'  JWK_NamedLocationComponent "\{[A-F0-9]+\}" \{\n'
        r'   m_sName "[^"]*"\n  \}\n'
        r'  JWK_TownMilitaryActivityComponent "\{[A-F0-9]+\}" \{\n'
        r'   m_iManpower \d+\n  \})'
    )
    inj = (
        f'\n  JWK_TownCiviliansControllerComponent "{{{TCC_GUID}}}" {{\n'
        f'   m_fPopulationSpawnFactor {factor}\n'
        f'  }}'
    )
    new, n = pat.subn(r'\1' + inj, text, count=1)
    if n == 0:
        return text, "regex NOT FOUND"
    return new, f"injected factor={factor}"

def main():
    print("=== CIVILIAN DENSITY ===")
    for fname, tc, factor in TOWNS:
        path = ROOT / "towns" / fname
        text = path.read_text(encoding="utf-8")
        new, status = add_civilian_factor(text, tc, factor)
        print(f"  {fname:<25} ({tc:<18}) -> {status}")
        if new != text:
            path.write_text(new, encoding="utf-8")

if __name__ == "__main__":
    main()
