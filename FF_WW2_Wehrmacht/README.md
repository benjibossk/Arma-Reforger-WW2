# FF_WW2_Wehrmacht

Wehrmacht (German Armed Forces) **content pack** for Arma Reforger.

This mod is pure content : characters, AI groups, and a vanilla `SCR_Faction` definition. **No Freedom Fighters dependency** — usable in any vanilla scenario, custom game mode, sandbox, or Game Master.

For Freedom Fighters scenarios, install `FF_WW2_Core` alongside this mod and use the WEHRMACHT faction key.

## Forces

| Force | Units |
|---|---|
| Heer (regular infantry) | Rifleman, NCO, Officer, SMG, MG34, MG-assist, AT (Panzerfaust 60), Sniper, Medic |
| Fallschirmjäger (paratroopers, FMJ) | Rifleman (FG42), NCO, Officer, SMG, MG42, MG-assist, AT |
| Waffen-SS (special forces, SS) | Rifleman (G43), NCO (STG44), Officer, STG44 soldier, MG, Sniper, AT |

Total: 23 chars + 19 AI groups.

## Vehicles

This content pack doesn't include vehicles directly — they come from external mods (FIE Kubelwagen, FIE Opel Blitz, FIE PanzerIV, SDKFZ251, WW2 Bicycle). Add them to your scenario via Worldeditor.

The FF integration (`FF_WW2_Core`) wires Kübelwagen, Opel Blitz, SdKfz 251 and Panzer IV into the Wehrmacht JWK faction config.

## Files

- `Configs/Factions/WEHRMACHT.conf` — vanilla `SCR_Faction` with German first names (30), white European visual identities, Wehrmacht flag (Iron Cross), eagle logo
- `Prefabs/Characters/Wehrmacht/*.et` — 23 character prefabs (inherit from vanilla USSR base, override loadouts and gear)
- `Prefabs/Groups/Wehrmacht/*.et` — 19 AI group prefabs

## Standalone use

To use these characters in your own scenario without Freedom Fighters :

1. Place character prefabs in Worldeditor directly
2. Or build your own factional system referencing `Configs/Factions/WEHRMACHT.conf` as an `SCR_Faction`
3. Or extract chars/groups in your own mod with this as a dependency

## Dependencies

- ArmaReforger (base game)
- `OO_AxisGear` + `SGSGearSlots` (uniforms : Stahlhelm, M43 jacket, M35 boots, vests)
- `OO_GERWeapons` + Chungus (`SMGs`, `LMGs`, `WW2Launchers`, `Rifles`) — weapons (Kar98k, MP40, MG34/42, P38, STG44, FG42, Panzerfaust 60)
- `RMS_OstfrontArms` — additional weapons
- ~~RMS_WW2_CORE~~ — removed in v1.2. Wehrmacht checkpoint compositions actually live in `FIE_Core`, not RMS. Faction flag/icon now fall back to vanilla SCR_Faction OPFOR defaults.
- FIE vehicle mods (Kubelwagen, OpelBlitz, PanzerIV, PanzerII), SDKFZ251, WW2 Bicycle — for related vehicle assets

**No FreedomFighters dependency.** Pure vanilla content.
