# FF_WW2_Wehrmacht

Wehrmacht (German Armed Forces) faction integration for **Freedom Fighters** on Arma Reforger.

Part of a WW2 conversion : 4 standalone factions for Freedom Fighters scenarios on WW2-themed terrains (Normandy, Eastern Front, etc.).

## Forces

| Force | Role | Units |
|---|---|---|
| Heer | `REGULAR` | Rifleman, NCO, Officer, SMG, MG34, MG-assist, AT (Panzerfaust), Sniper, Medic |
| Fallschirmjäger | `ELITE` (`FMJ`) | Rifleman (FG42), NCO, Officer, SMG, MG42, MG-assist, AT |
| Waffen-SS | `SPECIAL` (`SS`) | Rifleman (G43), NCO (STG44), Officer, STG44, MG, Sniper, AT |

## Vehicles

Kübelwagen, Opel Blitz Transport, SdKfz 251 Halftrack, WW2 Bicycle, Panzer IV Ausf. J

## Dependencies

ArmaReforger base, FreedomFighters, OO_AxisGear + SGSGearSlots (uniforms), OO_GERWeapons + Chungus(SMGs/LMGs/WW2Launchers/Rifles), RMS_WW2_CORE (Wehrmacht flag + logos + checkpoint compositions), FIE vehicles (Kubelwagen, OpelBlitz, PanzerIV, PanzerII), SDKFZ251, WW2 Bicycle.

## Integration

- `Configs/AddonsIntegrations.conf` overrides FF master to register this mod (and OperationOverlordAxisGear)
- `Configs/Addons/FF_WW2_Wehrmacht.conf` is the JWK_AddonIntegrationConfig
- `Configs/Factions/FF_Wehrmacht.conf` is the JWK_FactionConfig (3 forces, with patrol/recon/specialist/HQ groups)
- `Configs/Factions/WEHRMACHT.conf` is the SCR_Faction with German names, Wehrmacht flag, eagle logo
- `Prefabs/GameMode/JWK_FactionManager.et` overrides FF's prefab to register WEHRMACHT as a vanilla SCR_Faction (alongside MEC/MEI/TKA)
- Custom dogtags at `Prefabs/Items/Dogtag_Wehrmacht.et`
- Combat compositions : medium + large checkpoints with PAK38 anti-tank gun
