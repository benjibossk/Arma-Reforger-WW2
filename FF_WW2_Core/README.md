# FF_WW2_Core — Freedom Fighters Integration Hub

This mod owns **all the Freedom Fighters integration** for the WW2 faction pack. Required to use any of the WW2 factions inside FF scenarios.

The faction mods themselves (`FF_WW2_Wehrmacht`, `FF_WW2_USArmy`, `FF_WW2_RedArmy`, `FF_WW2_FFI`) are pure content packs (characters, AI groups, vanilla `SCR_Faction` definitions). They have **no FF dependency** and can be used standalone in any vanilla Arma Reforger scenario, custom game mode, or sandbox.

## What this mod contains

### Master Freedom Fighters overrides (only ONE place owns these)

- **`Prefabs/GameMode/JWK_FactionManager.et`** — override of FF's master prefab. Registers all 4 WW2 `SCR_Faction` keys (WEHRMACHT, US_WW2, RED_ARMY, FFI) alongside FF's MEC/MEI/TKA.
- **`Configs/AddonsIntegrations.conf`** — override of FF's master registry. Lists the 4 faction integration configs + OperationOverlordAxisGear.

### Per-faction Freedom Fighters configs

- **`Configs/Factions/FF_<Name>.conf`** — `JWK_FactionConfig` for each faction (forces, groups, vehicles, dogtag, traits, role bindings)
- **`Configs/Addons/FF_WW2_<Name>.conf`** — `JWK_AddonIntegrationConfig` wrapper for each faction

### FF-specific prefabs

- **`Prefabs/Items/Dogtag_<Name>.et`** — custom dogtags (each inherits from FF's `Dogtags_Base.et`)

## What's NOT here

- Characters → in the faction mods (vanilla `SCR_ChimeraCharacter`)
- AI Groups → in the faction mods (vanilla `SCR_AIGroup`)
- `SCR_Faction` per-faction identity files (names, flag, visual identity) → in the faction mods (vanilla `SCR_Faction`)

## Installation

Required:
- `ArmaReforger` (base game)
- `FreedomFighters` (`CAFEBEEFF0CACC1A`)
- **FF_WW2_Core** (this mod)

Then any combination of the faction mods:
- `FF_WW2_Wehrmacht`
- `FF_WW2_USArmy`
- `FF_WW2_RedArmy`
- `FF_WW2_FFI`

If a faction mod is not installed, its references in this mod's `JWK_FactionManager.et` and `AddonsIntegrations.conf` fail silently — FF tolerates missing references (same pattern as vanilla FF for MEC/MEI/TKA when those mods aren't installed).

## Dependencies in this mod's gproj

Core references vehicle and composition prefabs in its `JWK_FactionConfig` files (e.g., Wehrmacht's PanzerIV, US's M4 Sherman, FIE Wehrmacht checkpoints). So Core has dependencies on:

- ArmaReforger, FreedomFighters (required)
- ~~RMS_WW2_CORE~~ removed in v1.2 — Wehrmacht checkpoint compositions actually come from FIE_Core, and flag/icon textures fall back to vanilla SCR_Faction inheritance defaults
- OO_UsGear (US Military flag)
- FIE_Core (Wehrmacht + US checkpoint composition prefabs)
- OOGermanVehicles (Kübelwagen + Opel Blitz), RMS Panzer IV, SDKFZ251, WW2_Bicycle (Wehrmacht vehicles)
- OperationOverlordUSVehicles (Willys Jeep + Dodge WC63 truck), ShermanMedium, M3A1 Halftrack (US vehicles)

## GUID

`C91F4FE946AF94A8`
