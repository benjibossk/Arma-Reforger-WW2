# FF_WW2_RedArmy

Red Army (Soviet) faction integration for **Freedom Fighters** on Arma Reforger.

Part of the WW2 conversion pack.

## Forces

| Force | Role | Units |
|---|---|---|
| Red Army Infantry | `REGULAR` | Rifleman (Mosin-Nagant), NCO (PPSh-41), Officer, SMG, MG (DP-28), MG-assist, AT (PTRD-41 anti-tank rifle), Sniper (Mosin PU scope) |

## Faction integration

- `m_sFactionKey "RED_ARMY"`
- `Language RUSSIAN`
- Flag: Allies of WW2 (from RMS_WW2_CORE)
- 30 Russian first names

The vanilla `SCR_Faction "RED_ARMY"` registration is in the **FF_WW2_Wehrmacht** mod's `JWK_FactionManager.et` override (it owns the master FF prefab override for all our WW2 factions). Same for `AddonsIntegrations.conf`. To use this mod, both `FF_WW2_Wehrmacht` and `FF_WW2_RedArmy` must be installed.

## Vehicles

None currently — Red Army units are foot infantry (historically common for many Soviet units in WW2). Add Soviet WW2 vehicle mods to your scenario manually if needed.

## Dependencies

ArmaReforger base, FreedomFighters, RMS_RedArmyGear, RMS_RedArmyGuns (Mosin, PPSh, DP-28, TT-33, PTRD-41), ChungusCore, ChungusBoltGuns, ChungusSMGs, SGSGearSlots, RMS_WW2_CORE (for Allies flag).
