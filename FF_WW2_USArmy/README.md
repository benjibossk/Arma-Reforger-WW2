# FF_WW2_USArmy

US Army faction integration for **Freedom Fighters** on Arma Reforger.

Part of the WW2 conversion pack.

## Forces

| Force | Role | Units |
|---|---|---|
| GI Infantry | `REGULAR` | Rifleman (Garand), NCO (Thompson + M1911), Officer, SMG, MG (BAR), MG-assist, AT (Bazooka), Sniper (Garand), Medic |
| 101st Airborne | `ELITE` (`ABN`) | Rifleman (M1A1 Para), NCO, Officer, SMG (Thompson), MG (BAR), MG-assist (M1 Carbine) |

## Faction integration

- `m_sFactionKey "US_WW2"` (to avoid collision with vanilla "US")
- `Language ENGLISH`
- Flag: US Military flag from OO_UsGear
- 30 American first names

The vanilla `SCR_Faction "US_WW2"` registration is in the **FF_WW2_Wehrmacht** mod's `JWK_FactionManager.et` override (it owns the master FF prefab override for all our WW2 factions). Same for `AddonsIntegrations.conf`. To use this mod, both `FF_WW2_Wehrmacht` and `FF_WW2_USArmy` must be installed.

## Vehicles

- Willys MB Jeep (recon / officer transport)
- GMC CCKW Cargo truck (troop transport)
- M3A1 Halftrack with .50 cal MG (armored transport)
- M4A2 Sherman 75mm (medium tank)

## Combat compositions

- `m_rGenericCheckpointMedium` → `Checkpoint_S_FIE_US_01.et` (FIE Core)

## Dependencies

ArmaReforger base, FreedomFighters, OO_UsGear + OO_USWeapons + OO_Core, BigChungus weapons (BoltGuns, Rifles, SMGs, LMGs, WW2Launchers), FIE vehicles (Willys, CCKW, M3 Stuart, M4 Sherman, LCVP), M3A1 Halftrack, M16 Halftrack, M26 Pershing, Sherman Medium.
