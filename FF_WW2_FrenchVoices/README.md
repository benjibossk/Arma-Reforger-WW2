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

## Status

- [x] Directory scaffold (`Sounds/Character/`, `Sounds/RadioProtocol/Samples/FR/Male1/<categories>/`)
- [x] `addon.gproj` (GUID `AF123222FD39FDB1`)
- [x] `Translations_FR.csv` (135 lines with EN label → DE original → FR translation)
- [ ] `.acp` templates with FR `Filename` paths (clone NORTHCOM, substitute paths + GUIDs)
- [ ] 135 `.wav` recordings
- [ ] `.meta` files per `.acp` and per `.wav` (auto-generated by Workbench on first project save, or scripted)
- [ ] Hook into `FF_WW2_Core` via `Character_FIA_Base.et` override + dep
