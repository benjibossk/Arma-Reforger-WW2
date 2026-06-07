# Arma Reforger — WW2 Conversion for Freedom Fighters

WW2 conversion of the **Freedom Fighters** game mode on Arma Reforger, targeting **1944 occupied France**.

## Current architecture (post-pivot)

Originally this repo tried to build four custom WW2 factions from scratch (`FF_WW2_Wehrmacht`, `FF_WW2_USArmy`, `FF_WW2_RedArmy`, `FF_WW2_FFI`). After hitting too many problems — character variant leaks, missing voice integration, faction-registration crashes — we **pivoted to leveraging existing community WW2 mods** as runtime dependencies and only authoring the FF integration glue ourselves.

The active mods now are:

| Folder | Mod | Status |
|---|---|---|
| [`FF_WW2_Core/`](FF_WW2_Core/) | ⚙️ FF integration hub — overrides FF master configs, hooks community WW2 mods into FF gameplay | 🟢 Active |
| [`FF_WW2_FrenchVoices/`](FF_WW2_FrenchVoices/) | 🇫🇷 French voice pack — 263 ElevenLabs-generated wavs covering Radio Protocol (130) + FF dialogue system (133) | 🟢 Active |
| `FF_WW2_Wehrmacht/`, `FF_WW2_USArmy/`, `FF_WW2_RedArmy/`, `FF_WW2_FFI/` | Original custom faction mods | 🟡 Legacy / paused — kept in tree as reference, NOT shipped as Workshop deps |

## How it works

**Community mods do the heavy lifting**, overriding vanilla SCR_Faction characters and groups at their vanilla GUIDs (Morks pattern):

- [WWIIGermanForcesOO](https://reforger.armaplatform.com/workshop/66CA5209FF00CC8C) — 84 USSR chars → Wehrmacht, 49 USSR groups → Wehrmacht groups, USSR.conf → Germany branding
- [WWIIAmericanForcesOO](https://reforger.armaplatform.com/workshop/66CC38A9EB3FDB66) — 25 US chars → 1st Infantry 1944 + 9 Green Berets variants
- [WWIIPartisanForcesOO](https://reforger.armaplatform.com/workshop/697EA929E3C0282C) — 22 FIA chars → French Resistance, FIA.conf → "The Resistance"
- [WWIIGermanForcesATPrefab](https://reforger.armaplatform.com/workshop/672B3D60A11FD004) — Panzerschreck AT variants
- [USForcesExpandedOO](https://reforger.armaplatform.com/workshop/695A1436940B1AE3) — Suppressed Green Berets

`FF_WW2_Core` overrides FF's master `JWK_FactionConfig` files (`FF_USSR.conf`, `FF_US.conf`, `FF_FIA.conf`) to:
- Replace vanilla Cold War vehicles with WW2 vehicles (Panzer IV, Sherman, Kübelwagen, Opel Blitz, SDKFZ 251, Willys, etc.)
- Set faction languages (`GERMAN` / `ENGLISH_AMERICAN` / `FRENCH`)
- Inject Wehrmacht / Civilian French / WW2 weapon entity catalog filters
- Override `Character_USSR_Base.et` with NORTHCOM German voices (Wehrmacht radio chatter)
- Override `Character_FIA_base.et` + `JWK_Voices.acp` with French voices (FFI / civilians / officer / player)
- Override the civilian loadout to strip Cold War items (jungle boots, trucker caps...) — only 1940s-era clothing
- Block vanilla vehicle catalog imports so only WW2 vehicles spawn

Result: **no custom characters/groups owned by this repo**. The community mods drive what spawns, we just route, brand, and voice it.

## Install (Workshop user perspective)

When the mods are published, the dependency chain a player needs:

1. **ArmaReforger** (base)
2. **FreedomFighters** (`CAFEBEEFF0CACC1A`)
3. **FF_WW2_Core** (this hub)
4. *(Optional)* **FF_WW2_FrenchVoices** (`AF123222FD39FDB1`) for French voices

All Workshop dependencies (the 5 community WW2 mods, NORTHCOM German Voice Pack, OO vehicles, RMS Panzer IV, SDKFZ 251, Sherman Medium, M3A1 Halftrack, WW2 Bicycle) are pulled in automatically by `FF_WW2_Core.gproj`.

## Dev setup

Mono-repo cloned anywhere (e.g. `C:\Users\<you>\dev\Arma-Reforger-WW2\`). For Workbench to see each addon, create Windows junctions:

```powershell
New-Item -ItemType Junction `
  -Path "$env:USERPROFILE\Documents\My Games\ArmaReforgerWorkbench\addons\FF_WW2_Core" `
  -Target "$env:USERPROFILE\dev\Arma-Reforger-WW2\FF_WW2_Core"

New-Item -ItemType Junction `
  -Path "$env:USERPROFILE\Documents\My Games\ArmaReforgerWorkbench\addons\FF_WW2_FrenchVoices" `
  -Target "$env:USERPROFILE\dev\Arma-Reforger-WW2\FF_WW2_FrenchVoices"
```

Open the projects in Workbench, save once so it generates `.meta` GUIDs for all assets, then launch a FF scenario.

## Credits

- **Community WW2 mod authors** — WWIIGermanForcesOO, WWIIAmericanForcesOO, WWIIPartisanForcesOO, WWIIGermanForcesATPrefab, USForcesExpandedOO
- **NORTHCOM** — German Voice Pack (`66CC0D8D7EF6A8FF`) reused as the audio routing template for the French pack
- **Operation Overlord** team — AxisGear, US Gear, GER/US Vehicles, FIE Vehicles
- **BigChungus** — WW2 weapon packs (BoltGuns, SMGs, LMGs, Launchers, Rifles)
- **RMS** — Panzer IV, SDKFZ 251 dependencies, Ostfront Arms
- **JohnnyKerner** — Freedom Fighters game mode
- **ElevenLabs** — multilingual v3 model used to synthesize the 263 French voice lines

## License

See each mod's folder for license details. Generally permissive for non-commercial mod usage.
