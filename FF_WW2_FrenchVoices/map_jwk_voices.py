"""
Map JWK_Voices.acp AudioBankSampleClass names to our Speech_FR.csv sample names,
emit a generation plan + the override .acp content.

Strategy:
- Normalize both sides (strip suffix, uppercase, no separators)
- Apply known abbreviation expansion (HOS<->Hostile, NL<->Needless, NEG<->Negative...)
- Output mapping CSV showing what's matched and what's not
- Generate the new JWK_Voices.acp with FR paths for matched samples,
  keeping originals for unmatched ones (fall back to vanilla audio).
"""
import csv
import re
from pathlib import Path

ROOT = Path("C:/Users/benbo/dev/Arma-Reforger-WW2/FF_WW2_FrenchVoices")
JWK_IN = Path("C:/Users/benbo/tools/PakInspector/ff_full_extract/Sounds/Voices/JWK_Voices.acp")
CSV_IN = ROOT / "Speech_FR.csv"
MAPPING_CSV = ROOT / "jwk_mapping.csv"
ACP_OUT = ROOT / "Sounds" / "Voices" / "JWK_Voices.acp"

FRVOICES_GUID = "AF123222FD39FDB1"

ABBREVIATIONS = {
    "HOSTILE": "HOS",
    "NEEDLESS": "NL",
    "NEGATIVE": "NEG",
    "SUPPORTER": "SUP",
    "POSITIVE": "POS",
    "HIDEOUT": "HIDE",
    "POSTERS": "POSTER",
    "ALREADYHAVE": "ALREADY",
    "COMELATER": "LATER",
    "NOSPACE": "NOSPC",
}

# Explicit JWK_Name -> (Bank, OurSampleName) for entries the fuzzy matcher misses
# because FF used wildly different naming conventions between JWK_Voices and SpeechBanks.
EXPLICIT_MAP = {
    "AskForPosters.snd":                  ("Player", "POSTERS_ASK"),
    "AskJob_01.snd":                      ("Player", "RO_ASK_JOB"),
    "AskPoster_AlreadyHave.snd":          ("ResistanceOfficer", "POSTERS_ALREADY_HAVE"),
    "AskPoster_ComeLater.snd":            ("ResistanceOfficer", "POSTERS_COME_LATER"),
    "AskPoster_NoSpace.snd":              ("ResistanceOfficer", "POSTERS_NO_SPACE"),
    "AskPoster_OK.snd":                   ("ResistanceOfficer", "POSTERS_OK"),
    "ConvertSupporter_01.snd":            ("Player", "CIV_CONVERT_01"),
    "ConvertSupporter_02.snd":            ("Player", "CIV_CONVERT_02"),
    "ConvertSupporter_03.snd":            ("Player", "CIV_CONVERT_03"),
    "ConvertSupporter_04.snd":            ("Player", "CIV_CONVERT_04"),
    "ConvertSupporter_05.snd":            ("Player", "CIV_CONVERT_05"),
    "ConvertSupporter_06.snd":            ("Player", "CIV_CONVERT_06"),
    "ConvertSupporter_07.snd":            ("Player", "CIV_CONVERT_07"),
    "ConvertSupporter_08.snd":            ("Player", "CIV_CONVERT_08"),
    "ConvertSupporter_09.snd":            ("Player", "CIV_CONVERT_09"),
    "ConvertSupporter_10.snd":            ("Player", "CIV_CONVERT_10"),
    "DontCall_01.snd":                    ("ResistanceOfficer", "DONT_CALL"),
    "ExtortCivilianNeg_01.snd":           ("AmbientCivilian", "EXTORT_NEG_01"),
    "ExtortCivilianNeg_02.snd":           ("AmbientCivilian", "EXTORT_NEG_02"),
    "ExtortCivilianNeg_03.snd":           ("AmbientCivilian", "EXTORT_NEG_03"),
    "ExtortCivilianNeg_04.snd":           ("AmbientCivilian", "EXTORT_NEG_04"),
    "ExtortCivilianNeg_05.snd":           ("AmbientCivilian", "EXTORT_NEG_05"),
    "ExtortCivilianOK_01.snd":            ("AmbientCivilian", "EXTORT_OK_01"),
    "ExtortCivilianOK_02.snd":            ("AmbientCivilian", "EXTORT_OK_02"),
    "ExtortCivilianOK_03.snd":            ("AmbientCivilian", "EXTORT_OK_03"),
    "ExtortCivilianOK_04.snd":            ("AmbientCivilian", "EXTORT_OK_04"),
    "ExtortCivilianResistance_01.snd":    ("AmbientCivilian", "EXTORT_RES_01"),
    "ExtortCivilianResistance_02.snd":    ("AmbientCivilian", "EXTORT_RES_02"),
    "ExtortCivilianUndercover_01.snd":    ("AmbientCivilian", "EXTORT_UND_01"),
    "ExtortCivilianUndercover_02.snd":    ("AmbientCivilian", "EXTORT_UND_02"),
    "ExtortCivilian_01.snd":              ("Player", "CIV_EXTORT_01"),
    "ExtortCivilian_02.snd":              ("Player", "CIV_EXTORT_02"),
    "ExtortCivilian_03.snd":              ("Player", "CIV_EXTORT_03"),
    "ExtortCivilian_04.snd":              ("Player", "CIV_EXTORT_04"),
    "ExtortCivilian_05.snd":              ("Player", "CIV_EXTORT_05"),
    "HideoutLocationReplyA_01.snd":       ("ResistanceOfficer", "HIDEOUT_OK_A"),
    "HideoutLocationReplyB_02.snd":       ("ResistanceOfficer", "HIDEOUT_OK_B"),
    "HideoutLocationReplyNeg_01.snd":     ("ResistanceOfficer", "HIDEOUT_NONE"),
    "J_DeliverItem_OK_01.snd":            ("ResistanceOperative", "DELIVER_ITEM_OK"),
    "JobDoReport_01.snd":                 ("Player", "JOB_REPORT_DONE_01"),
    "JobReplyNeg_01.snd":                 ("ResistanceOfficer", "JOB_NONE"),
    "JobReplyOkCache_01.snd":             ("ResistanceOfficer", "JOB_DEAD_DROP"),
    "JobReplyOkMeet_01.snd":              ("ResistanceOfficer", "JOB_MEET"),
    "JobReplyOkNotes_01.snd":             ("ResistanceOfficer", "JOB_GIVE_NOTE"),
    "JobReportBackInPerson_01.snd":       ("ResistanceOfficer", "JOB_REQ_REPORT_PERSON"),
    "JobReportOk_01.snd":                 ("ResistanceOfficer", "JOB_REPORT_OK"),
    "LiberatePrisoner_01.snd":            ("Player", "LIBERATE_CALL_01"),
    "LiberatePrisoner_02.snd":            ("Player", "LIBERATE_CALL_02"),
    "PassOK_01.snd":                      ("ResistanceOfficer", "PASS_OK"),
    "PhonePickupMP_01.snd":               ("MilitaryPolice", "MP_PHONE_PICKUP"),
    "Q_Dogtags_PL_1.snd":                 ("Player", "Q_PL_DOGTAGS_1"),
    "Q_Dogtags_RO_1.snd":                 ("ResistanceOfficerQuests", "Q_RO_DOGTAGS_1"),
    "Q_Dogtags_RO_2.snd":                 ("ResistanceOfficerQuests", "Q_RO_DOGTAGS_2"),
    "Q_Dogtags_RO_3.snd":                 ("ResistanceOfficerQuests", "Q_RO_DOGTAGS_3"),
    "Q_Dogtags_RO_4.snd":                 ("ResistanceOfficerQuests", "Q_RO_DOGTAGS_4"),
    "Q_Dogtags_RO_5.snd":                 ("ResistanceOfficerQuests", "Q_RO_DOGTAGS_5"),
    "Q_Fob_RO_1.snd":                     ("ResistanceOfficerQuests", "Q_RO_FOB_1"),
    "Q_Fob_RO_2.snd":                     ("ResistanceOfficerQuests", "Q_RO_FOB_2"),
    "Q_Fob_RO_3.snd":                     ("ResistanceOfficerQuests", "Q_RO_FOB_3"),
    "Q_Intro_PlayerGreet.snd":            ("Player", "Q_PL_INTRO_1"),
    "Q_Intro_RO_1.snd":                   ("ResistanceOfficerQuests", "Q_RO_INTRO_1"),
    "Q_Posters_RO_1.snd":                 ("ResistanceOfficerQuests", "Q_RO_POSTERS_1"),
    "Q_Posters_RO_2.snd":                 ("ResistanceOfficerQuests", "Q_RO_POSTERS_2"),
    "Q_Posters_RO_3.snd":                 ("ResistanceOfficerQuests", "Q_RO_POSTERS_3"),
    "RO_JobDeliverItem1.snd":             ("ResistanceOfficerJobs", "J_RO_NEW_DELIVER_ITEM"),
    "RO_JobResign_01.snd":                ("ResistanceOfficerJobs", "J_RO_JOB_RESIGN_01"),
    "RO_JobResign_02.snd":                ("ResistanceOfficerJobs", "J_RO_JOB_RESIGN_02"),
    "RO_JobResign_03.snd":                ("ResistanceOfficerJobs", "J_RO_JOB_RESIGN_03"),
    "RadioCalloutAnswer_01.snd":          ("ResistanceOfficer", "RADIO_CALLOUT_ANSWER"),
    "RadioCalloutTail_01.snd":            ("Default", "RADIO_CALLOUT_TAIL"),
    "ReportResistance_01.snd":            ("Player", "MP_REPORT_RESISTANCE_01"),
    "ResistanceReportReply_01.snd":       ("MilitaryPolice", "MP_RESISTANCE_REPORT_REPLY"),
    "StopFollow_01.snd":                  ("PlayerActions", "ASK_STOP_FOLLOW_01"),
    "StopFollow_02.snd":                  ("PlayerActions", "ASK_STOP_FOLLOW_02"),
    "TalkNoPants_01.snd":                 ("AmbientCivilian", "NO_PANTS_01"),
    "TalkNoPants_02.snd":                 ("AmbientCivilian", "NO_PANTS_02"),
}

def norm(s):
    s = s.replace(".snd", "").upper()
    # strip separators
    s = re.sub(r"[_\s\-]", "", s)
    # apply abbreviations both ways
    for long_, short_ in ABBREVIATIONS.items():
        s = s.replace(long_, short_)
    return s


def match_samples():
    content = JWK_IN.read_text(encoding="utf-8", errors="replace")
    jwk_samples = re.findall(r'AudioBankSampleClass\s+"([^"]+)"', content)

    our_samples = []
    with CSV_IN.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            our_samples.append({"Bank": r["Bank"], "SampleName": r["SampleName"]})

    jwk_idx = {norm(s): s for s in jwk_samples}
    ours_idx = {norm(s["SampleName"]): s for s in our_samples}

    matches = []
    explicit_used = set()
    for jname in jwk_samples:
        # Try explicit map first
        if jname in EXPLICIT_MAP:
            bank, sample = EXPLICIT_MAP[jname]
            matches.append({
                "JWK_Name": jname,
                "Bank": bank,
                "Our_SampleName": sample,
                "Status": "MATCH_EXPLICIT",
            })
            explicit_used.add(jname)
            continue
        # Then try fuzzy normalization
        jk = norm(jname)
        if jk in ours_idx:
            ours = ours_idx[jk]
            matches.append({
                "JWK_Name": jname,
                "Bank": ours["Bank"],
                "Our_SampleName": ours["SampleName"],
                "Status": "MATCH",
            })

    matched_jwk = {m["JWK_Name"] for m in matches}
    matched_keys = {norm(m["JWK_Name"]) for m in matches}
    unmatched_jwk = [s for s in jwk_samples if s not in matched_jwk]
    for s in unmatched_jwk:
        matches.append({
            "JWK_Name": s,
            "Bank": "",
            "Our_SampleName": "",
            "Status": "JWK_NO_MATCH",
        })

    for k, ours in ours_idx.items():
        if k not in matched_keys:
            matches.append({
                "JWK_Name": "",
                "Bank": ours["Bank"],
                "Our_SampleName": ours["SampleName"],
                "Status": "OURS_UNUSED",
            })

    with MAPPING_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["JWK_Name", "Bank", "Our_SampleName", "Status"])
        w.writeheader()
        w.writerows(matches)

    return jwk_samples, matches, content


def patch_acp(content, matches):
    """For each MATCH/MATCH_EXPLICIT row, rewrite the AudioBankSampleClass Filename to our FR wav path."""
    match_map = {m["JWK_Name"]: m for m in matches if m["Status"] in ("MATCH", "MATCH_EXPLICIT")}
    replaced = 0

    def rewrite(m_block):
        nonlocal replaced
        sample_name = re.search(r'AudioBankSampleClass\s+"([^"]+)"', m_block.group(0)).group(1)
        if sample_name not in match_map:
            return m_block.group(0)
        mp = match_map[sample_name]
        fr_path = f"{{{FRVOICES_GUID}}}Sounds/Voices/Samples/FR/{mp['Bank']}/{mp['Our_SampleName']}.wav"
        new_block = re.sub(
            r'Filename\s+"[^"]+"',
            f'Filename "{fr_path}"',
            m_block.group(0),
            count=1,
        )
        replaced += 1
        return new_block

    out = re.sub(
        r'AudioBankSampleClass\s+"[^"]+"\s*\{[^{}]*Filename\s+"[^"]+"[^{}]*\}',
        rewrite,
        content,
        flags=re.DOTALL,
    )
    return out, replaced


def main():
    jwk_samples, matches, content = match_samples()
    fuzzy = sum(1 for m in matches if m["Status"] == "MATCH")
    explicit = sum(1 for m in matches if m["Status"] == "MATCH_EXPLICIT")
    unmatched_jwk = sum(1 for m in matches if m["Status"] == "JWK_NO_MATCH")
    unused_ours = sum(1 for m in matches if m["Status"] == "OURS_UNUSED")
    print(f"Total JWK samples:      {len(jwk_samples)}")
    print(f"MATCHED (fuzzy):        {fuzzy}")
    print(f"MATCHED (explicit):     {explicit}")
    print(f"TOTAL MATCHED:          {fuzzy + explicit}")
    print(f"JWK without FR audio:   {unmatched_jwk}")
    print(f"Our FR samples unused:  {unused_ours}")
    print(f"\nMapping written to:     {MAPPING_CSV.relative_to(ROOT.parent)}")

    new_acp, replaced = patch_acp(content, matches)
    ACP_OUT.parent.mkdir(parents=True, exist_ok=True)
    ACP_OUT.write_text(new_acp, encoding="utf-8")
    print(f"Patched {replaced} Filename entries in {ACP_OUT.name}")
    print(f"Saved to: {ACP_OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
