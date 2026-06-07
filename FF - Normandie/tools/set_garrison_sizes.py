#!/usr/bin/env python3
"""Set RP-realistic garrison sizes on milbases (m_iBaseForceSize on
JWK_AIGarrisonComponent), factories (same), and towns (m_iManpower on
JWK_TownMilitaryActivityComponent).

Strategy: inside each entity's existing components{} block (which we created
earlier with the JWK_NamedLocationComponent), append the second/third
component with the garrison attribute. Match by unique instance name.
"""
import re
from pathlib import Path

ROOT = Path(r"C:\Users\benbo\Documents\My Games\ArmaReforgerWorkbench\addons\FF - Normandie\Worlds\FF_Normandie_Layers")

# GUID of the component instance template inherited from the parent prefab
AIG_GUID_MILBASE = "64A0C8691A55F98A"
AIG_GUID_FACTORY = "659EFEC227B5CEDE"
TMA_GUID_TOWN    = "64E347579D05582B"

MILBASES = {
    "MBC_Stutzpunkt_Brecourt":         45,
    "MBC_Stutzpunkt_Foucarville":      40,
    "MBC_Stutzpunkt_PicauvilleNord":   40,
    "MBC_Stutzpunkt_PicauvilleNO":     35,
    "MBC_Stutzpunkt_Hubert":           35,
    "MBC_Stutzpunkt_SaintCome":        35,
    "MBC_Stutzpunkt_PicauvilleEst":    30,
    "MBC_Stutzpunkt_LaRueSud":         25,
    "MBC_Stutzpunkt_LaRueNO":          25,
    "MBC_Stutzpunkt_Carquebut":        25,
}

FACTORIES = {
    "FC_Entrepot_Reuville":     15,
    "FC_Entrepot_Hubert":       15,
    "FC_Scierie_SainteMereNE": 10,
    "FC_Scierie_BrecourtNO":   10,
    "FC_Scierie_BrecourtSO":   10,
    "FC_Ferme_BrecourtEst":     6,
    "FC_Ferme_FoucarvilleEst":  6,
    "FC_Ferme_QuinevilleNE":    6,
    "FC_Ferme_Picauville":      6,
    "FC_Ferme_LaRue":           6,
    "FC_Ferme_SaintMarcouf":    6,
    "FC_Ferme_Beuzeville":      6,
}

# (layer_filename, TC_instance_name, manpower)
TOWNS = [
    ("BrecourtManor.layer",  "TC_Komsomolsk",   30),  # bourg historique
    ("Hubert.layer",         "TC_Gorshkovo",    30),
    ("LaRue.layer",          "TC_Michurino",    30),
    ("SainteMere.layer",     "TC_Kamensk",      30),
    ("Beuzeville.layer",     "TC_SosnovyMys3",  12),
    ("Carquebut.layer",      "TC_SosnovyMys2",  12),
    ("Foucarville.layer",    "TC_Mineraly2",    12),
    ("Picauville.layer",     "TC_SosnovyMys",   12),
    ("Quineville.layer",     "TC_Mineraly3",    12),
    ("Reuville.layer",       "TC_SosnovyMys4",  12),
    ("SaintCome.layer",      "TC_Mineraly",     12),
    ("SaintMarcouf.layer",   "TC_Mineraly4",    12),
]

def add_aigarrison(text: str, instance: str, size: int, guid: str) -> tuple[str, str]:
    """Add JWK_AIGarrisonComponent { m_iBaseForceSize X } inside the existing
    components{} block of the given entity instance, immediately after the
    closing brace of the existing JWK_NamedLocationComponent block."""
    if f'{instance} {{' not in text:
        return text, "instance NOT FOUND"
    if 'JWK_AIGarrisonComponent' in text[text.index(f'{instance} {{'):text.index(f'{instance} {{') + 800]:
        return text, "already has AIG"

    # Find the pattern: ' <instance> {\n  components {\n   JWK_NamedLocationComponent "{...}" {
    #                    m_sName "..."\n   }\n  }'  → insert before the closing  }
    pat = re.compile(
        r'( ' + re.escape(instance) + r' \{\n  components \{\n'
        r'   JWK_NamedLocationComponent "\{[A-F0-9]+\}" \{\n'
        r'    m_sName "[^"]*"\n   \})'
    )
    inj = (
        f'\n   JWK_AIGarrisonComponent "{{{guid}}}" {{\n'
        f'    m_iBaseForceSize {size}\n'
        f'   }}'
    )
    new, n = pat.subn(r'\1' + inj, text, count=1)
    if n == 0:
        return text, "regex NOT FOUND"
    return new, f"injected size={size}"

def add_townmanpower(text: str, tc_inst: str, manpower: int) -> tuple[str, str]:
    """Add JWK_TownMilitaryActivityComponent { m_iManpower X } inside the
    existing components{} of the town entity, between the NLC and the closing }."""
    if 'JWK_TownMilitaryActivityComponent' in text:
        return text, "already has TMA override"

    pat = re.compile(
        r'(JWK_TownEntity ' + re.escape(tc_inst) +
        r' : "\{64B2F8D8059C97CC\}Prefabs/Controllers/Loadtime/JWK_TownController\.et" \{\n'
        r' components \{\n'
        r'  JWK_NamedLocationComponent "\{[A-F0-9]+\}" \{\n'
        r'   m_sName "[^"]*"\n  \})'
    )
    inj = (
        f'\n  JWK_TownMilitaryActivityComponent "{{{TMA_GUID_TOWN}}}" {{\n'
        f'   m_iManpower {manpower}\n'
        f'  }}'
    )
    new, n = pat.subn(r'\1' + inj, text, count=1)
    if n == 0:
        return text, "regex NOT FOUND"
    return new, f"injected manpower={manpower}"

def process(path: Path, mapping: dict, guid: str, label: str):
    print(f"\n=== {label} ({path.name}) ===")
    text = path.read_text(encoding="utf-8")
    for inst, size in mapping.items():
        text, status = add_aigarrison(text, inst, size, guid)
        print(f"  {inst:<35} -> {status}")
    path.write_text(text, encoding="utf-8")

def process_towns():
    print("\n=== TOWNS ===")
    for fname, tc, manpower in TOWNS:
        path = ROOT / "towns" / fname
        text = path.read_text(encoding="utf-8")
        text, status = add_townmanpower(text, tc, manpower)
        print(f"  {fname:<25} ({tc:<18}) -> {status}")
        path.write_text(text, encoding="utf-8")

def main():
    process(ROOT / "milbases.layer", MILBASES, AIG_GUID_MILBASE, "MILBASES")
    process(ROOT / "factories.layer", FACTORIES, AIG_GUID_FACTORY, "FACTORIES")
    process_towns()

if __name__ == "__main__":
    main()
