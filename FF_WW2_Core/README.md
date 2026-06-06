# FF_WW2_Core — Registration Hub

**Required dependency for the WW2 faction pack.** This is a thin hub mod that owns the Freedom Fighters master overrides for all WW2 factions in this repo.

## What it does

Two overrides of FF master resources :

1. **`Prefabs/GameMode/JWK_FactionManager.et`** (override of FF's `{64B2F8D8059C822F}`)
   Registers all 4 WW2 SCR_Factions (WEHRMACHT, US_WW2, RED_ARMY, FFI) alongside FF's vanilla SCR_Factions (MEC, MEI, TKA).

2. **`Configs/AddonsIntegrations.conf`** (override of FF's `{A41CAA1E409C6244}`)
   Lists the 4 WW2 mod integration configs + OperationOverlordAxisGear, so FF discovers and loads them at runtime.

## Why a separate mod ?

Enfusion does not aggregate overrides — only one override per resource wins (last loaded). So a single mod must own the FF master overrides and reference all faction sources by path.

Each individual faction mod (Wehrmacht / USArmy / RedArmy / FFI) provides its own SCR_Faction `.conf` file at a known path. The Core mod's `JWK_FactionManager.et` references those paths. If a faction mod is not installed, its reference fails silently and that faction simply isn't available — exactly how vanilla FF handles MEI / TKA / MEC when those mods aren't installed.

## Installation

Required mods :
- **FF_WW2_Core** (this mod)
- **FreedomFighters** (`CAFEBEEFF0CACC1A`)
- **ArmaReforger** (base game)

Then any combination of the faction mods :
- `FF_WW2_Wehrmacht`
- `FF_WW2_USArmy`
- `FF_WW2_RedArmy`
- `FF_WW2_FFI`

## Dependencies

ArmaReforger base + FreedomFighters only. No other content.

## GUID

`C91F4FE946AF94A8`
