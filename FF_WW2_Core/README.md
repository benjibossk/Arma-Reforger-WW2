# FF_WW2_Core — Freedom Fighters WW2 Integration Hub

This mod is the **only thing this repo ships** for the WW2 conversion. It depends on existing community WW2 mods (Operation Overlord WW2 forces, NORTHCOM voices, etc.) and overrides Freedom Fighters' master configs so the WW2 content slots into FF gameplay.

## What this mod does

### Overrides FF's per-faction JWK_FactionConfig

`Configs/Factions/FF_USSR.conf` (Wehrmacht), `FF_US.conf` (US 1944), `FF_FIA.conf` (FFI Partisans) — all at FF master config GUIDs:
- WW2 vehicles in `m_aDefaultVehicles` (Panzer IV, Kübelwagen, Opel Blitz, SDKFZ 251, Sherman, Willys, WC63, M3A1 Halftrack, WW2 Bicycle)
- Catalog imports filter `m_sPrefabNameExcludeFilter "*"` to block all vanilla Cold War vehicle imports
- Languages: `GERMAN` for Wehrmacht, `ENGLISH_AMERICAN` for US, `FRENCH` for FFI
- Force keys remapped: USSR Naval Infantry → `FALLSCHIRMJAGER`, USSR KLMK → `GEBIRGSJAGER`, USSR Spetsnaz → `WAFFEN_SS`, US Green Berets → `AIRBORNE`
- Vanilla USSR/US/FIA char/group paths kept — community mods override those at their vanilla GUIDs

### Overrides the vanilla SCR_Faction for the civilian faction

`Configs/Factions/USSR.conf` (vanilla GUID `09727032415AC39B`) — strips 6 leftover Russian first names from the WWIIGermanForcesOO Wehrmacht name pool, adds 27 more German first names + 15 more surnames.

`Configs/Factions/FF_CIV.conf` (FF master GUID `00C219DF633474D1`) — language `FRENCH`, civilian vehicles reduced to the WW2 Bicycle only (no Skoda S105/S1203, no UAZ civilians).

`Configs/Identities/FactionIdentity_USSR.conf` (vanilla GUID `FBBCD73926989580`) — replaces Russian civilian names with 35 French first names (Jean, Pierre, Henri, Marcel, etc.) + 40 French surnames (Dupont, Martin, Bernard, Dubois, etc.).

`Configs/Factions/Utils/Loadouts/Loadout_CIV.conf` (GUID `596BAFA3AFB6E40A`) — drops 1944-anachronistic items from the civilian loadout pool: Jungle Boots, Trucker Caps, Zmijovka Caps, modern Raincoats, Fisherman Pants. Keeps Flat Caps, French Berets (`Hat_RadiovkaBeret_01`), Cotton/Turtleneck shirts, Suit jackets, Trousers, period boots.

### Character base overrides for voices

`Prefabs/Characters/Factions/OPFOR/USSR_Army/Character_USSR_Base.et` (vanilla GUID `5346CF7E39A65A6B`) — injects `SCR_CommunicationSoundComponent` with the 9 NORTHCOM German `.acp` files so all Wehrmacht characters speak German on radio.

`Prefabs/Characters/Factions/INDFOR/FIA/Character_FIA_base.et` (vanilla GUID `7A9EE19AB67B298B`) — same pattern, points at the 9 French `.acp` files from `FF_WW2_FrenchVoices` so all FFI characters speak French on radio.

## What this mod does NOT contain

- No characters or AI groups — community WW2 mods own those, overriding vanilla USSR/US/FIA at their vanilla GUIDs
- No weapon or vehicle prefabs — referenced from OO, RMS, BigChungus, FIE, SDKFZ 251, Sherman Medium, M3A1 Halftrack, WW2 Bicycle
- No voice samples — `FF_WW2_FrenchVoices` owns the French wavs; NORTHCOM owns the German wavs

## Dependencies (declared in `FF_WW2_Core.gproj`)

| GUID | Mod | Role |
|---|---|---|
| `58D0FB3206B6F859` | ArmaReforger | base |
| `CAFEBEEFF0CACC1A` | FreedomFighters | game mode being extended |
| `66CA5209FF00CC8C` | WWIIGermanForcesOO | overrides USSR → Wehrmacht (chars + groups + SCR_Faction) |
| `66CC38A9EB3FDB66` | WWIIAmericanForcesOO | overrides US → 1944 1st Infantry |
| `697EA929E3C0282C` | WWIIPartisanForcesOO | overrides FIA → French Resistance |
| `672B3D60A11FD004` | WWIIGermanForcesATPrefab | Panzerschreck variants |
| `695A1436940B1AE3` | USForcesExpandedOO | suppressed Green Berets |
| `66CC0D8D7EF6A8FF` | NORTHCOM German Voice Pack | Wehrmacht radio voices |
| `AF123222FD39FDB1` | FF_WW2_FrenchVoices | FFI + civilian + officer + player French voices |
| `5ADD31817243EAD5` | FIE_Core | composition prefabs (checkpoints) |
| `65AE1353B9C5BC41` | OO German Vehicles | Kübelwagen + Opel Blitz |
| `65AD797399E3CF39` | OO US Vehicles | Willys + WC63 |
| `649942D9C90389E3` | Sherman Medium | US tank |
| `692C3806D8C77463` | RMS Panzer IV | German tank |
| `69332095A2A34B7D` | RMS Hinterhalt | composition assets |
| `65C7179DA0B82317` | SDKFZ 251 | German halftrack |
| `62B4A8E40D31F94B` | WW2 Bicycle | period civilian transport |
| `65BD1CC2A0110122` | M3A1 Halftrack | US halftrack |

## GUID

`C91F4FE946AF94A8`

## Architectural note

This mod follows the "override at vanilla GUID" pattern (a.k.a. Morks pattern). Engine load order resolves: vanilla → community mod overrides → our overrides (loaded last because we depend on the community mods). So any path our override touches wins because we load after every other addon in the chain.
