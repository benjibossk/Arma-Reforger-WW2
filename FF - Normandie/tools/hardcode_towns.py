#!/usr/bin/env python3
"""Inject hardcoded French m_sName into each JWK_TownController instance
inside the towns/ subfolder. Also handles 3 radios in radios.layer (which
need a fresh NLC component added, since the parent prefab doesn't have one).
"""
import re
from pathlib import Path

ROOT = Path(r"C:\Users\benbo\Documents\My Games\ArmaReforgerWorkbench\addons\FF - Normandie\Worlds\FF_Normandie_Layers")
NLC_GUID_TOWN = "65C35A2F385D762F"

# (layer_filename, TC_instance_name, displayed_french_name)
TOWNS = [
    ("BrecourtManor.layer",  "TC_Komsomolsk",   "Manoir de Brécourt"),
    ("Hubert.layer",         "TC_Gorshkovo",    "Hubert"),
    ("LaRue.layer",          "TC_Michurino",    "La Rue"),
    ("SainteMere.layer",     "TC_Kamensk",      "Sainte-Mère-Église"),
    ("Beuzeville.layer",     "TC_SosnovyMys3",  "Beuzeville-au-Plain"),
    ("Carquebut.layer",      "TC_SosnovyMys2",  "Carquebut"),
    ("Foucarville.layer",    "TC_Mineraly2",    "Foucarville"),
    ("Picauville.layer",     "TC_SosnovyMys",   "Picauville"),
    ("Quineville.layer",     "TC_Mineraly3",    "Quinéville"),
    ("Reuville.layer",       "TC_SosnovyMys4",  "Reuville"),
    ("SaintCome.layer",      "TC_Mineraly",     "Saint-Côme-du-Mont"),
    ("SaintMarcouf.layer",   "TC_Mineraly4",    "Saint-Marcouf"),
]

# Radios: parent prefab has NO JWK_NamedLocationComponent — we add it fresh
# with unique 16-hex GUIDs.
RADIOS = [
    ("RSC_Antenne_Hubert",          "Antenne radio Hubert",       "FFAA0B100000031A"),
    ("RSC_Antenne_SaintCome",       "Antenne radio Saint-Côme",   "FFAA0B100000032A"),
    ("RSC_Antenne_QuinevilleNE",    "Antenne radio Quinéville",   "FFAA0B100000033A"),
]

def inject_town(path: Path, tc_inst: str, name: str) -> str:
    text = path.read_text(encoding="utf-8")
    pat = re.compile(
        r'(JWK_TownEntity ' + re.escape(tc_inst) +
        r' : "\{64B2F8D8059C97CC\}Prefabs/Controllers/Loadtime/JWK_TownController\.et" \{\n)( coords )'
    )
    inj = (
        ' components {\n'
        f'  JWK_NamedLocationComponent "{{{NLC_GUID_TOWN}}}" {{\n'
        f'   m_sName "{name}"\n'
        '  }\n'
        ' }\n'
    )
    new = pat.sub(r'\1' + inj + r'\2', text, count=1)
    if new == text:
        return "NOT FOUND"
    path.write_text(new, encoding="utf-8")
    return "injected"

def inject_radio(path: Path, rsc_inst: str, name: str, guid: str) -> str:
    text = path.read_text(encoding="utf-8")
    pat = re.compile(
        r'( ' + re.escape(rsc_inst) + r' \{\n)(  coords )'
    )
    inj = (
        '  components {\n'
        f'   JWK_NamedLocationComponent "{{{guid}}}" {{\n'
        f'    m_sName "{name}"\n'
        '   }\n'
        '  }\n'
    )
    new = pat.sub(r'\1' + inj + r'\2', text, count=1)
    if new == text:
        return "NOT FOUND"
    path.write_text(new, encoding="utf-8")
    return "injected"

def main():
    print("=== TOWNS ===")
    for fname, tc, name in TOWNS:
        path = ROOT / "towns" / fname
        status = inject_town(path, tc, name)
        print(f"  {fname:<25} ({tc:<18}) -> {status:<10} | \"{name}\"")

    print("\n=== RADIOS ===")
    radios_path = ROOT / "radios.layer"
    for rsc, name, guid in RADIOS:
        status = inject_radio(radios_path, rsc, name, guid)
        print(f"  {rsc:<28} -> {status:<10} | \"{name}\"")

if __name__ == "__main__":
    main()
