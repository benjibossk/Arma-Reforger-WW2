# Arma Reforger — WW2 Faction Pack for Freedom Fighters

Standalone WW2 faction integrations for the **Freedom Fighters** game mode on Arma Reforger.

Each faction is fully self-contained, no Morks dependency, built on top of Operation Overlord (AxisGear, GER/US Weapons, FIE Vehicles), Chungus Weapons, RMS_WW2_CORE, and other community assets.

## Mods

| Folder | Mod | Status | FF dep? |
|---|---|---|---|
| [`FF_WW2_Core/`](FF_WW2_Core/) | ⚙️ Freedom Fighters integration hub — only needed for FF scenarios | ✅ Released | YES |
| [`FF_WW2_Wehrmacht/`](FF_WW2_Wehrmacht/) | 🇩🇪 Wehrmacht (Heer + Fallschirmjäger + Waffen-SS) | ✅ Released | NO (standalone) |
| [`FF_WW2_USArmy/`](FF_WW2_USArmy/) | 🇺🇸 US Army (GI + 101st Airborne) | ✅ Released | NO (standalone) |
| [`FF_WW2_RedArmy/`](FF_WW2_RedArmy/) | ⭐ Red Army (Soviet) | ✅ Released | NO (standalone) |
| [`FF_WW2_FFI/`](FF_WW2_FFI/) | 🇫🇷 French Resistance (FFI / Maquis) | ✅ Released (PLAYER) | NO (standalone) |

## Architecture

The faction mods are **pure content packs** — characters, AI groups, and vanilla `SCR_Faction` definitions. **No FreedomFighters dependency.** Usable in any vanilla scenario, custom game mode, sandbox, or Game Master.

The **`FF_WW2_Core`** mod owns all the Freedom Fighters integration : `JWK_FactionConfig` for each faction, FF master overrides (`AddonsIntegrations.conf` + `JWK_FactionManager.et`), and custom dogtags. Install it only if you want to use these factions inside FF scenarios.

### Use cases

- **FF scenarios** : install `FF_WW2_Core` + the faction mods you want
- **Custom scenarios / sandbox / Game Master / non-FF mods** : install only the faction mods (no Core, no FF needed)

### Faction missing tolerance

`FF_WW2_Core` references each faction's `SCR_Faction.conf` by path. If a faction mod isn't installed, the reference fails silently and that faction simply isn't available — same as how vanilla FF handles MEC/MEI/TKA when those mods aren't installed.

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
