# FF - Normandie — Freedom Fighters Scenario

🇫🇷 Playable **Freedom Fighters scenario** set in **occupied Normandy, June 1944**.

Lead the **French Resistance (FFI / Maquis)** against the **Wehrmacht**, supported by the **101st Airborne** dropped behind enemy lines. Liberate village after village, sabotage radio antennas, capture factories, ambush convoys.

## Factions

This scenario is built on [`FF_WW2_Core`](../FF_WW2_Core/) which re-skins the vanilla FF factions as WW2 equivalents. The FactionKeys remain vanilla (so the FF FactionManager doesn't need overriding), only the identity/visuals/voices are replaced.

| Role | FactionKey | Skinned as |
|---|---|---|
| PLAYER | `FIA` | Maquis / FFI (French Resistance) |
| ENEMY | `USSR` | Wehrmacht (German Army) |
| SUPPORTING | `US` | 101st Airborne |
| AMBIENT | `CIV` | French civilians, 1944 |

## Map

- **Terrain**: [Normandy](https://reforger.armaplatform.com/workshop/616D67C41B1DF93D) (`616D67C41B1DF93D`) — bocage normand, 4.86 × 4.86 km
- **Biome**: Woodland
- **Currency**: Franc (₣)
- **Persistence key**: `JWK_Normandie`

## Content overview

### 16 named settlements

4 main towns (manpower 30, spawn factor 0.3):
- **Hubert** · **Sainte-Mère-Église** · **La Rue** · **Manoir de Brécourt**

8 villages (manpower 12, spawn factor 0.2):
- Saint-Côme-du-Mont · Picauville · Foucarville · Quinéville · Saint-Marcouf · Carquebut · Beuzeville-au-Plain · Reuville

4 hamlets (manpower 6, spawn factor 0.15):
- Néville-sur-Mer · Fontenay-sur-Mer · Lestre · Crosville-sur-Douve

All settlements use real Cotentin toponyms or geographically plausible names. Each is wired with `JWK_NamedLocationComponent`, `JWK_TownMilitaryActivityComponent` (patrol thresholds + manpower regen), and `JWK_TownCiviliansControllerComponent` (spawn density tuned down for occupation feel).

### 12 Wehrmacht Stützpunkte + 1 abandoned castle

| Position | Garrison | Notes |
|---|---|---|
| Stützpunkt Brécourt | 45 | Front-line position (historical Band of Brothers target) |
| Stützpunkt Foucarville | 40 | Key axis near Sainte-Mère |
| Stützpunkt Picauville Nord | 40 | Defensive front |
| Stützpunkt Hubert / Saint-Côme / Picauville NO | 35 each | Garrison towns |
| Stützpunkt Picauville Est | 30 | Intermediate |
| Stützpunkt La Rue Sud / NO / Carquebut | 25 each | Coastal outposts |
| **Château de Crosville (abandonné)** | 20 | Forward observation post in ruins |

### 13 factories

- 8 fermes (6 troops each) — small rural guard
- 3 scieries (10 troops each) — strategic production
- 2 entrepôts (15 troops each) — supply depots

Each has French `m_sName` (Ferme de Picauville, Scierie de Brécourt NO, Entrepôt d'Hubert, etc.) and `JWK_AIGarrisonComponent` for size.

### 3 radio sites

`JWK_RadioSiteController` doesn't ship a `JWK_NamedLocationComponent` by default, so they were added manually with unique GUIDs (`FFAA0B100000031A` etc.) and French names: Antenne radio Hubert / Saint-Côme / Quinéville.

### 21 building overrides

WW2Assets house prefabs (House 1-10, FarmHouse_Wood, House_Mountain, France Building 2a/3a/4a, Small House(s), HouseTown, WW2_House_Town, Tavern, Loft Barn) are overridden in `Prefabs/Structures/Buildings/` to inject:
- `JWK_PopulationComponent` with `m_iCapacity` per building type (0-6)
- `JWK_SpawnPointsContainerComponent` (spawn point entities to be placed in editor)

### FFI loadout (provided by FF_WW2_Core)

Recruited Maquis can pick from **7 weapon sets**:

| Set | Weapon | Origin RP |
|---|---|---|
| Kar98_Captured | Kar98k + 6 stripper clips | Captured Wehrmacht |
| MP40_Captured | MP40 + 4 mags | Captured Wehrmacht |
| Thompson_Airdrop | Thompson M1A1 + 4 mags | Allied airdrop |
| M1Garand_Airdrop | M1 Garand + 6 en-bloc clips | US airdrop |
| M1Carbine_Para | M1A1 PARA Carbine + 5 mags | Paratrooper drop |
| BAR_Airdrop | BAR M1918A2 + 4 mags | Allied heavy support |
| Bazooka_Airdrop | M1A1 Bazooka + 3 M6A1 HEAT rockets | US anti-tank |

Plus 2× FieldDressing + 2× Mk2 Grenade default kit.

## World settings (`default.layer`)

Key attributes on `JWK_World_Normandie`:

```
m_vMapOffset 0 -204 0
m_vMapSize 4864 292 4864
m_sPersistenceKey "JWK_Normandie"
m_sRoadNetworkPath "Assets/JWK/RoadNetworks/Normandie.json"
m_fAmbientTrafficIntensity 0.4
m_iBiome WOODLAND
m_sDefaultPlayerFaction "FIA"
m_sDefaultEnemyFaction "USSR"
m_sDefaultSupportingFaction "US"
m_sDefaultAmbientFaction "CIV"
m_iMinimumPoiPlayerDistance 1200
m_iMinimumPoiSelfSpacing 1500
```

`JWK_FreedomFightersWorldSettingsComponent` overrides:
```
m_iHideoutMaxPreferredTownDistance 1500   (default 800)  → hideouts more isolated, RP Maquis
m_iHideoutMinimumEnemySiteDistance 600    (default 400)  → safer from Stützpunkte
```

## Tools

The `tools/` folder contains Python scripts used during scenario construction. Idempotent (safe to re-run after edits in Workbench).

| Script | Purpose |
|---|---|
| `hardcode_names.py` | Inject French `m_sName` into factories + milbases |
| `hardcode_towns.py` | Same for towns + add NLC on radios |
| `configure_hammeaux.py` | Rename Hammeau1-4 → real Cotentin village names + tune manpower/spawn |
| `set_garrison_sizes.py` | Inject `JWK_AIGarrisonComponent.m_iBaseForceSize` per entity |
| `set_civilian_density.py` | Add `m_fPopulationSpawnFactor` per town |
| `update_civilian_density.py` | Update existing spawn factor values |
| `set_patrol_tempo.py` | Add patrol thresholds + manpower regen per town |
| `inject_ff_components.py` | Add population + spawn container to building overrides |

## Required mods

| Workshop ID | Mod |
|---|---|
| `58D0FB3206B6F859` | ArmaReforger (base) |
| `CAFEBEEFF0CACC1A` | FreedomFighters |
| `C91F4FE946AF94A8` | FF_WW2_Core (this monorepo) |
| `616D67C41B1DF93D` | Normandy (terrain) |
| `647804D31EC300F0` | WW2Assets (building prefabs) |

FF_WW2_Core transitively pulls in: WWIIGermanForcesOO, WWIIAmericanForcesOO, WWIIPartisanForcesOO, Operation Overlord, BigChungus, RMS, NORTHCOM voice pack, etc.

## Status

🟡 **Work in progress** — placement of all controllers done, GenericSlot dynamic POIs in progress. Loadouts + factions verified. AI navmesh + spawn points inside buildings still need polish per-prefab.

## Credits

- **benjibossk** — scenario design, placement, configuration
- **JohnnyKerner** — Freedom Fighters game mode
- **Normandy terrain author** — base map (`616D67C41B1DF93D`)
- All upstream WW2 mod authors (see root [README](../README.md))
