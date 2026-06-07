# FF - WW2 French Voices

Voice pack scaffold for FFI / French Resistance characters in the WW2 conversion mod.
Modeled after the NORTHCOM German Voice Pack (`66CC0D8D7EF6A8FF`) which served as the analysis reference.

## How the NORTHCOM pack is built

The `NorthcomGermanVoicePack` ships **only**:
- 9 `.acp` files (text-based `AudioClass` configs) under `Sounds/Character/` and `Sounds/RadioProtocol/`
- ~135 `.wav` recordings under `Sounds/RadioProtocol/Samples/DE/Male1/` organized by semantic category
- A tiny `addon.gproj` depending only on `58D0FB3206B6F859` (ArmaReforger)

**Important** — `Character_Voice_Code_DE.acp` does NOT replace breath/grunt/death samples; those still point to the vanilla English (`/Eng/Male1/Breath/...`) base game assets. Only the radio protocol lines are localized to German. A French pack has the same scope: ~135 short radio recordings, no breath/grunt re-recording needed.

The 9 `.acp` files split the protocol by category:

| .acp | Lines | Content |
|---|---|---|
| `Character_Voice_Code_DE.acp` | 188 (mostly Eng inherits) | Maps character voice slots to base-game breath/grunt + the German radio bank. Mostly references English samples. |
| `RadioProtocol_Actions_DE.acp` | 138 wav refs | BailOut, Covering, Door, RadioReconfigure, Rearm, ShowLocation |
| `RadioProtocol_Campaign_SL_DE.acp` | — | Squad leader campaign-specific lines |
| `RadioProtocol_CombatPatrol_DE.acp` | — | Combat patrol orders |
| `RadioProtocol_Combat_DE.acp` | — | CeaseFire, Defend, FireAtWill, ReturnFire, Suppress |
| `RadioProtocol_Confirmations_DE.acp` | — | Yes / No / Understood / Jawohl |
| `RadioProtocol_Movement_DE.acp` | — | Move, Retreat, Stop |
| `RadioProtocol_Report_DE.acp` | — | Spotted contacts, ManDown, Recruit |
| `RadioProtocol_Report_2_DE.acp` | — | Continuation / overflow of Report |

Each `.acp` is a text `AudioClass { signals { ... } samples { ... } }` config:
- `SignalClass` blocks reference shared `.sig` files (Character_Occlusion, IdentityVoice, WeaponUse, RadioProtocol_Seed, etc.) which live in vanilla — leave them identical when copying.
- `AudioBankSampleClass "<name>.wav" { Filename "{<GUID>}Sounds/.../<name>.wav" }` blocks point to the actual recordings. This is where DE → FR substitution happens.

## The 135 lines to record

See `Translations_FR.csv` for the full semantic translation table.

Categories:
- **Actions** (29): BailOut, Covering, Door, RadioReconfigure, Rearm, ShowLocation
- **Combat** (14): CeaseFire, Defend, FireAtWill, ReturnFire, Suppress
- **Confirmations** (6): Yes / Jawohl-equiv / Understood / No
- **General** (49): Base order, 8 CardinalDirections, 4 Directions, 15 Distances (50m..2.5km), FactionAndObject (Civilian/Enemy/Friendly/Unknown chars+vehicles, MachineGun, Soldier), 10 Soldier numbers (0-9), GridMarked
- **Movement** (7): Move (Get ready, I'm moving calm/loud), Retreat (FollowMe, ToMe), Stop (Halt, Stop)
- **Reports** (6): ManDown (Comrade/Medic Wounded), Recruit (3 lines + Dismiss), Contact
- **Uncategorized** (18): Attacking, BringMeAmmo, Healing (×6), ImHit (×5), MoveThere, StayDown(Whisper), StayInCover(Whisper), UseThatMachineGun, WeAreUnderAttack

## WAV format

NORTHCOM samples are PCM 16-bit stereo at 48000 Hz (verified via `xxd` on `Jawohl.wav`):
```
RIFF .... WAVEfmt 0x10 .... 0x01 (PCM) 0x02 (stereo) 0xBB80 (48000Hz) 0x10 (16bit) ....
```

When recording or rendering TTS, target the same format. `ffmpeg` example:
```
ffmpeg -i input.mp3 -ar 48000 -ac 2 -c:a pcm_s16le output.wav
```

Trim silence at start/end and normalize to roughly the same loudness as the German references (≈ -16 LUFS works well for radio chatter).

## Generation workflow

### Option A — Real human recordings (best quality)
Native French speaker, mic with low background noise. 135 short lines, ~30–60 minutes of recording.

### Option B — TTS (fastest)
Use ElevenLabs or Coqui XTTS-v2 or Bark with a French male voice prompt.
- ElevenLabs: clone voice or use preset (e.g., "Antoni FR"), settings: stability 0.5, similarity 0.7
- Coqui XTTS: prompt a short reference clip, batch-generate from CSV
- Bark: `[MAN]` speaker token, French language

### Option C — Re-use vanilla CZECH samples
The Partisan mod's chars already use Czech voices. Czech radio chatter is acceptable as "Eastern European Resistance" and requires zero new recordings — but the user wanted French specifically.

## Wiring into FF_WW2_Core

Once `.wav` files are populated and `.acp` configs reference them, integration is one override in `FF_WW2_Core`:

```
// FF_WW2_Core/Prefabs/Characters/Factions/INDFOR/FIA/Character_FIA_Base.et
// (override at vanilla FIA base GUID — same pattern as Character_USSR_Base.et for German voices)

SCR_ChimeraCharacter : "{37578B1666981FCE}Prefabs/Characters/Core/Character_Base.et" {
 ID "<unique-16-hex>"
 components {
  SCR_CommunicationSoundComponent "{54FD05D0C92D071F}" {
   Filenames {
    "{AF123222FD39FDB1}Sounds/Character/Character_Voice_Code_FR.acp"
    "{AF123222FD39FDB1}Sounds/RadioProtocol/RadioProtocol_Actions_FR.acp"
    "{AF123222FD39FDB1}Sounds/RadioProtocol/RadioProtocol_Campaign_SL_FR.acp"
    "{AF123222FD39FDB1}Sounds/RadioProtocol/RadioProtocol_CombatPatrol_FR.acp"
    "{AF123222FD39FDB1}Sounds/RadioProtocol/RadioProtocol_Combat_FR.acp"
    "{AF123222FD39FDB1}Sounds/RadioProtocol/RadioProtocol_Confirmations_FR.acp"
    "{AF123222FD39FDB1}Sounds/RadioProtocol/RadioProtocol_Movement_FR.acp"
    "{AF123222FD39FDB1}Sounds/RadioProtocol/RadioProtocol_Report_2_FR.acp"
    "{AF123222FD39FDB1}Sounds/RadioProtocol/RadioProtocol_Report_FR.acp"
   }
  }
 }
}
```

Add `AF123222FD39FDB1` to `FF_WW2_Core.gproj` Dependencies and add a `.meta` for the override file pointing at the vanilla `Character_FIA_Base.et` GUID (resolve via Workbench Resource Browser → right-click → "Override resource in current project").

Also update `FF_WW2_Core/Configs/Factions/FF_FIA.conf`:
```
m_aLanguages {
 FRENCH
}
```
(currently set to `CZECH` waiting for this pack).

## Two distinct content sources

This pack covers TWO complementary voice systems used by Freedom Fighters:

### 1. Radio Protocol (NORTHCOM-style) — 135 lines
Short tactical chatter: orders, contacts, distances, cardinal directions, confirmations.
Routed via 9 `.acp` files in `Sounds/RadioProtocol/`.
See `Translations_FR.csv`.

### 2. FF Speech System — 131 lines
Conversational dialogue: civilian recruitment/extortion, resistance officer briefings,
player remarks, prisoner interactions, passphrases.
Routed via FF's `SpeechBank_*.conf` configs that map each line to a signal ID in
`Sounds/Voices/JWK_Voices.acp` + a localization key.

**Great news**: Freedom Fighters ships `localization_FreedomFighters.fr_fr.conf`
with all subtitle texts ALREADY translated into French. Only the AUDIO is missing.

See `Speech_FR.csv` (auto-generated by `extract_ff_speech.py` from FF data).

Breakdown by bank:
| Bank | Lines | Context |
|---|---|---|
| AmbientCivilian | 35 | Civilians being recruited / extorted / hostile reactions |
| Default | 16 | Digits 0–9 + 6 standalone callouts |
| MilitaryPolice | 2 | MP reactions |
| Passphrases | 11 | Codeword challenges/responses |
| Player | 27 | Player character utterances |
| PlayerActions | 6 | Action confirmations |
| Prisoner | 0 | (uses audio only, no subtitles) |
| ResistanceOfficer | 17 | Officer dialogue |
| ResistanceOfficerJobs | 4 | Job assignments |
| ResistanceOfficerQuests | 12 | Quest dialogue |
| ResistanceOperative | 1 | Operative remark |

## Status

- [x] Directory scaffold
- [x] `addon.gproj` (GUID `AF123222FD39FDB1`)
- [x] `Translations_FR.csv` (130 radio protocol lines)
- [x] `Speech_FR.csv` (131 FF speech lines extracted + FR translations from FF localization)
- [x] `.acp` templates for radio protocol (9 files, DE → FR paths substituted)
- [x] `generate_voices.py` — ElevenLabs batch TTS → WAV 48kHz stereo
- [x] **261/261 wav generated** (120 MB total) via `eleven_v3` + emotion tags
- [ ] Override `JWK_Voices.acp` to route FF signal IDs to French .wav samples
- [ ] `.meta` files per `.acp` and per `.wav` (auto-generated by Workbench on first project save)
- [ ] Hook into `FF_WW2_Core` via `Character_FIA_Base.et` override + dep + `m_aLanguages FRENCH`

## Voice cast used (production run)

| Role | Voice | ID | Lines |
|---|---|---|---|
| soldier   | Mathieu Serious  | `ckgFqgT4MZNQ3bggyZiF` | Radio + Default + MP (148) |
| officer   | Eric Instructor  | `jdVRqFnO8jznZjspX89f` | ResistanceOfficer + Jobs + Quests (33) |
| player    | Mikovista        | `4hYlhKO9gzckfpMgfFKJ` | Player + Actions + Passphrases (44) |
| operative | (fallback Mathieu — Stellan voice id was removed from library) | `ckgFqgT4MZNQ3bggyZiF` | ResistanceOperative (1) |
| civilian1 | Martin Dupont    | `wyZnrAs18zdIj8UgFSV8` | AmbientCivilian rotated (12) |
| civilian2 | Paul K Deep      | `5l4ttmr4SKNgi0HnOelT` | AmbientCivilian rotated (12) |
| civilian3 | Hugo             | `DbbNuBL7lf62XwY7arQb` | AmbientCivilian rotated (11) |

## Generation settings (validated)

```
model       = eleven_v3
stability   = 0.75    # sharp, projected, consistent (military bark, no drift)
similarity  = 0.85    # preserve voice identity
style       = 0.95    # max emotional exaggeration / aggression
speaker_boost = true
tag-role    = true    # prefix per-role emotion tags (default on)
```

Soldier lines additionally get UPPERCASED before TTS (`ÉVACUEZ !` → harder shout).

Role-specific emotion tag prefixes (`ROLE_TAGS` in `generate_voices.py`):
- soldier: `[screaming][shouting][angry][combat][war zone]`
- officer: `[urgent][commanding][barking]`
- player: `[determined][tense][gritty]`
- operative: `[serious][tense][battle-hardened]`
- civilian1: `[scared][trembling]`
- civilian2: `[angry][hostile]`
- civilian3: `[stressed][nervous]`
