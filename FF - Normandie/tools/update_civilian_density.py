#!/usr/bin/env python3
"""Update existing m_fPopulationSpawnFactor values in town layers."""
import re
from pathlib import Path

ROOT = Path(r"C:\Users\benbo\Documents\My Games\ArmaReforgerWorkbench\addons\FF - Normandie\Worlds\FF_Normandie_Layers\towns")

TCC_GUID = "6296F54A892986E3"

# (layer_filename, TC_instance_name, new_factor)
TOWNS = [
    ("BrecourtManor.layer",  "TC_Komsomolsk",   0.3),
    ("Hubert.layer",         "TC_Gorshkovo",    0.3),
    ("LaRue.layer",          "TC_Michurino",    0.3),
    ("SainteMere.layer",     "TC_Kamensk",      0.3),
    ("Beuzeville.layer",     "TC_SosnovyMys3",  0.2),
    ("Carquebut.layer",      "TC_SosnovyMys2",  0.2),
    ("Foucarville.layer",    "TC_Mineraly2",    0.2),
    ("Picauville.layer",     "TC_SosnovyMys",   0.2),
    ("Quineville.layer",     "TC_Mineraly3",    0.2),
    ("Reuville.layer",       "TC_SosnovyMys4",  0.2),
    ("SaintCome.layer",      "TC_Mineraly",     0.2),
    ("SaintMarcouf.layer",   "TC_Mineraly4",    0.2),
]

def update_factor(text: str, new_factor: float) -> tuple[str, str]:
    """Replace m_fPopulationSpawnFactor value inside the existing
    JWK_TownCiviliansControllerComponent block."""
    pat = re.compile(
        r'(JWK_TownCiviliansControllerComponent "\{' + TCC_GUID + r'\}" \{\s*\n\s*m_fPopulationSpawnFactor )[\d.]+'
    )
    new, n = pat.subn(r'\g<1>' + str(new_factor), text, count=1)
    if n == 0:
        return text, "NOT FOUND"
    return new, f"updated -> {new_factor}"

def main():
    print("=== UPDATE CIVILIAN FACTOR ===")
    for fname, tc, factor in TOWNS:
        path = ROOT / fname
        text = path.read_text(encoding="utf-8")
        new, status = update_factor(text, factor)
        print(f"  {fname:<25} -> {status}")
        if new != text:
            path.write_text(new, encoding="utf-8")

if __name__ == "__main__":
    main()
