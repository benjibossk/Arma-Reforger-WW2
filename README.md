# Arma Reforger — WW2 Faction Pack for Freedom Fighters

Standalone WW2 faction integrations for the **Freedom Fighters** game mode on Arma Reforger.

Each faction is fully self-contained, no Morks dependency, built on top of Operation Overlord (AxisGear, GER/US Weapons, FIE Vehicles), Chungus Weapons, RMS_WW2_CORE, and other community assets.

## Mods

| Folder | Mod | Status |
|---|---|---|
| [`FF_WW2_Core/`](FF_WW2_Core/) | ⚙️ Registration hub — **required dependency** for any of the factions below | ✅ Released |
| [`FF_WW2_Wehrmacht/`](FF_WW2_Wehrmacht/) | 🇩🇪 Wehrmacht (Heer + Fallschirmjäger + Waffen-SS) | ✅ Released |
| [`FF_WW2_USArmy/`](FF_WW2_USArmy/) | 🇺🇸 US Army (GI + 101st Airborne) | ✅ Released |
| [`FF_WW2_RedArmy/`](FF_WW2_RedArmy/) | ⭐ Red Army (Soviet) | ✅ Released |
| [`FF_WW2_FFI/`](FF_WW2_FFI/) | 🇫🇷 French Resistance (FFI / Maquis) | ✅ Released (PLAYER faction) |

## Architecture

Install **`FF_WW2_Core`** + any combination of faction mods. Each faction is independent — pick only the ones you want. `FF_WW2_Core` owns the master Freedom Fighters resource overrides (`AddonsIntegrations.conf` + `JWK_FactionManager.et`) and references each faction by path; missing factions are tolerated silently (same pattern FF itself uses for MEC/MEI/TKA).

## Each mod includes

- A complete `JWK_FactionConfig` (Freedom Fighters integration)
- An `SCR_Faction` registration patched into FF's `JWK_FactionManager`
- Multiple forces (REGULAR / ELITE / SPECIAL) with their own characters and groups
- Custom dogtags, faction flag, eagle/national logo
- Combat compositions (checkpoints, fortifications)
- Vehicles from FIE, SDKFZ251 and other WW2 vehicle mods

## Contributing

PRs welcome ! Open an issue if you find a bug, want a new unit, or want to suggest balance tweaks. I'll review & merge regularly, then publish Workshop updates.

## Credits

- **Operation Overlord** team — AxisGear, US Gear, GER/US Weapons, FIE Vehicles
- **BigChungus** — WW2 weapon packs (BoltGuns, SMGs, LMGs, Launchers, Rifles)
- **RMS** — WW2 Core (flags, logos, checkpoint compositions), Ostfront Arms, PanzerIV alt, RedArmy gear
- **JohnnyKerner** — Freedom Fighters game mode

## License

See each mod's folder for license details. Generally permissive for non-commercial mod usage.
