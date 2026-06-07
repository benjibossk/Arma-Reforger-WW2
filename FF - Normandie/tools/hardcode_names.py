#!/usr/bin/env python3
"""Inject hardcoded French m_sName into every JWK_NamedLocationComponent
across towns/, factories.layer, milbases.layer.

Strategy: regex-replace ' <InstanceName> {\n  coords' with
' <InstanceName> {\n  components { JWK_NamedLocationComponent "{GUID}" {
m_sName "..." } }\n  coords' for entities that don't already have a
components block. For entities that do (e.g. 3 factories with old Kolguyev
m_sName values), the m_sName is already French — no change.

Radios use a separate path (no NamedLocationComponent in parent prefab) —
handled by adding SCR_MapDescriptor entries to placeNames.layer.
"""
import re
from pathlib import Path

ROOT = Path(r"C:\Users\benbo\Documents\My Games\ArmaReforgerWorkbench\addons\FF - Normandie\Worlds\FF_Normandie_Layers")

# Component instance GUIDs from parent prefabs (Workbench-discovered)
NLC_GUID_FACTORY  = "64E512EE3D735264"
NLC_GUID_MILBASE  = "65C2DD931B48E7EC"
NLC_GUID_TOWN     = "65C35A2F385D762F"

# Map instance name -> displayed French label
TOWNS = {
    "BrecourtManor":      "Manoir de Brécourt",
    "Hubert":             "Hubert",
    "LaRue":              "La Rue",
    "SainteMere":         "Sainte-Mère-Église",
    "Beuzeville":         "Beuzeville-au-Plain",
    "Carquebut":          "Carquebut",
    "Foucarville":        "Foucarville",
    "Picauville":         "Picauville",
    "Quineville":         "Quinéville",
    "Reuville":           "Reuville",
    "SaintCome":          "Saint-Côme-du-Mont",
    "SaintMarcouf":       "Saint-Marcouf",
}

FACTORIES = {
    "FC_Entrepot_Reuville":    "Entrepôt de Reuville",
    "FC_Ferme_BrecourtEst":    "Ferme de Brécourt-Est",
    "FC_Entrepot_Hubert":      "Entrepôt d'Hubert",
    "FC_Scierie_SainteMereNE": "Scierie de Sainte-Mère (NE)",
    "FC_Ferme_FoucarvilleEst": "Ferme de Foucarville (Est)",
    "FC_Ferme_QuinevilleNE":   "Ferme de Quinéville (NE)",
    "FC_Scierie_BrecourtNO":   "Scierie de Brécourt (NO)",
    "FC_Ferme_Picauville":     "Ferme de Picauville",
    "FC_Ferme_LaRue":          "Ferme de La Rue",
    "FC_Ferme_SaintMarcouf":   "Ferme de Saint-Marcouf",
    "FC_Ferme_Beuzeville":     "Ferme de Beuzeville",
    "FC_Scierie_BrecourtSO":   "Scierie de Brécourt (SO)",
}

MILBASES = {
    "MBC_Stutzpunkt_LaRueSud":         "Stützpunkt La Rue Sud",
    "MBC_Stutzpunkt_SaintCome":        "Stützpunkt Saint-Côme",
    "MBC_Stutzpunkt_PicauvilleNord":   "Stützpunkt Picauville Nord",
    "MBC_Stutzpunkt_Carquebut":        "Stützpunkt Carquebut",
    "MBC_Stutzpunkt_PicauvilleNO":     "Stützpunkt Picauville Nord-Ouest",
    "MBC_Stutzpunkt_LaRueNO":          "Stützpunkt La Rue Nord-Ouest",
    "MBC_Stutzpunkt_PicauvilleEst":    "Stützpunkt Picauville Est",
    "MBC_Stutzpunkt_Brecourt":         "Stützpunkt Brécourt",
    "MBC_Stutzpunkt_Hubert":           "Stützpunkt Hubert",
    "MBC_Stutzpunkt_Foucarville":      "Stützpunkt Foucarville",
}

def inject_or_update(text: str, instance: str, name: str, guid: str) -> tuple[str, str]:
    """For a given instance block, ensure JWK_NamedLocationComponent.m_sName=name.
    Returns (new_text, status)."""
    # Case 1: instance has a JWK_NamedLocationComponent already (with any m_sName) — replace
    pat_existing = re.compile(
        r'( ' + re.escape(instance) + r' \{\s*\n  components \{\s*\n   JWK_NamedLocationComponent "\{[A-F0-9]+\}" \{\s*\n    m_sName )"[^"]*"',
        re.MULTILINE,
    )
    if pat_existing.search(text):
        new = pat_existing.sub(r'\1"' + name + '"', text, count=1)
        return new, "updated"

    # Case 2: instance has NO components block — inject one before the coords line
    pat_no_comp = re.compile(
        r'( ' + re.escape(instance) + r' \{\s*\n)(  coords )',
        re.MULTILINE,
    )
    if pat_no_comp.search(text):
        injection = (
            '  components {\n'
            f'   JWK_NamedLocationComponent "{{{guid}}}" {{\n'
            f'    m_sName "{name}"\n'
            '   }\n'
            '  }\n'
        )
        new = pat_no_comp.sub(r'\1' + injection + r'\2', text, count=1)
        return new, "injected"

    return text, "NOT FOUND"

def process_file(path: Path, mapping: dict, guid: str):
    if not path.exists():
        print(f"  SKIP missing: {path}")
        return
    text = path.read_text(encoding="utf-8")
    orig = text
    for inst, name in mapping.items():
        text, status = inject_or_update(text, inst, name, guid)
        print(f"  {inst:<35} -> {status:<10} | \"{name}\"")
    if text != orig:
        path.write_text(text, encoding="utf-8")
        print(f"  >>> {path.name} saved")
    else:
        print(f"  >>> {path.name} unchanged")

def main():
    print("=== TOWNS ===")
    towns_dir = ROOT / "towns"
    for inst, name in TOWNS.items():
        layer_path = towns_dir / f"{inst}.layer"
        text = layer_path.read_text(encoding="utf-8")
        new, status = inject_or_update(text, "TC_Komsomolsk", name, NLC_GUID_TOWN)
        # Try alternative TownController instance names too
        for tc_inst in ["TC_Komsomolsk", "TC_Mineraly", "TC_Michurino", "TC_SosnovyMys",
                        "TC_Kamensk", "TC_Gorshkovo", "TC_Ugoldar"]:
            new2, status2 = inject_or_update(new, tc_inst, name, NLC_GUID_TOWN)
            if status2 != "NOT FOUND":
                new, status = new2, status2
                break
        print(f"  {inst:<20} -> {status:<10} | \"{name}\"")
        if new != text:
            layer_path.write_text(new, encoding="utf-8")

    print("\n=== FACTORIES ===")
    process_file(ROOT / "factories.layer", FACTORIES, NLC_GUID_FACTORY)

    print("\n=== MILBASES ===")
    process_file(ROOT / "milbases.layer", MILBASES, NLC_GUID_MILBASE)

if __name__ == "__main__":
    main()
