# FF_WW2_FFI — French Resistance (Forces Françaises de l'Intérieur)

Player-side faction integration for **Freedom Fighters** on Arma Reforger.

The FFI / Maquis are civilians who took up arms against the German occupation (1940-1945). Equipped with whatever they could find : captured German weapons (Kar98, MP40), Allied airdrops (Bazooka, M1A1 Thompson, Sten), hunting rifles, civilian clothes.

## Forces

| Force | Role | Units |
|---|---|---|
| Maquis | `REGULAR` (PLAYER) | Rifleman, Cell Leader, Maquis Captain, SMG, MG (BAR airdrop), MG-assist, AT (Bazooka airdrop), Sniper (Kar98), Medic |

## Faction integration

- `m_sFactionKey "FFI"`
- `Language FRENCH`
- Configured as **PLAYER faction** — humans play this side
- 30 French first names (Jean, Pierre, Jacques, Henri, Louis, Marcel, André, François…)
- Civilian appearance (fedora, suit jacket, Maquis armband)
- Flag: Allies of WW2 (RMS_WW2_CORE)
- Custom Dogtag_FFI

## Modern item filtering

To avoid the player having access to modern weapons (AK-74, etc.) through the FF shop/loadout system :
- `m_aItemsEntityCatalogImports` — filter with `m_bEnabled 0` → no modern items imported
- `m_aDefaultVehiclesEntityCatalogImports` — filter disabled → no modern vehicles
- `m_PlayerRoleTrait.m_Loadout` — empty JWK_LoadoutConfig → player spawns with character prefab loadout (no AK-74 default)

This means the player gets WW2-era gear only when spawning as a Maquis character.

## Vehicles

- WW2 Bicycle (the iconic Resistance transport)

Add more WW2 civilian vehicles to your scenarios manually.

## Cross-faction wiring

The vanilla `SCR_Faction "FFI"` registration is in **FF_WW2_Wehrmacht** mod's `JWK_FactionManager.et` override (the master FF prefab override for all our WW2 factions). Same for `AddonsIntegrations.conf`. Both `FF_WW2_Wehrmacht` and `FF_WW2_FFI` must be installed.

## Dependencies

ArmaReforger base, FreedomFighters, OO_AxisGear (captured Wehrmacht gear), OO_GERWeapons (captured Kar98/MP40), OO_Core, OO_UsGear (Allied airdrops), OO_USWeapons (Thompson, BAR, Bazooka), ChungusCore, ChungusSMGs, ChungusLMGs, ChungusBoltGuns, ChungusRifles, ChungusWW2Launchers, SGSGearSlots, WW2_Bicycle, RMS_WW2_CORE (Allies flag).
