//------------------------------------------------------------------------------
// FFWE_SpawnDebug.c
//
// Hooks JWK_SpawnUtils to log every AI spawn (prefab path + group prefab path)
// to the Workbench Console / runtime log.
//
// Usage:
//   - In Workbench: View → Console — filter for [FFWE_DEBUG]
//   - In runtime: check the .ADM / console log for [FFWE_DEBUG] lines
//
// Each log line tells us which character + group prefab FF is requesting,
// so we can spot paths that still resolve to vanilla Cold War units instead
// of our Wehrmacht overrides.
//
// To disable: comment out the body of the overridden methods or delete the
// .c file (and re-Build the mod afterwards).
//------------------------------------------------------------------------------

modded class JWK_SpawnUtils
{
	//------------------------------------------------------------------------------
	// Hook the high-level SpawnCharacter call (used by JWK_AISpawnRequest
	// processing and direct dev actions). Logs the requested character prefab,
	// the group prefab it joins, and the role override.
	//------------------------------------------------------------------------------
	override static IEntity SpawnCharacter(
		vector pos,
		ResourceName prefab,
		ResourceName groupPrefab = ResourceName.Empty,
		JWK_EFactionRole roleOverride = JWK_EFactionRole.UNDEFINED
	) {
		PrintFormat("[FFWE_DEBUG] SpawnCharacter prefab='%1' group='%2' role=%3 pos=%4",
			prefab, groupPrefab, roleOverride, pos);

		return super.SpawnCharacter(pos, prefab, groupPrefab, roleOverride);
	}

	//------------------------------------------------------------------------------
	// Hook the lower-level SpawnEntityPrefab to catch Character_/Group_ prefabs
	// that bypass SpawnCharacter (variant resolution, group prefab roster slots,
	// etc.). Filtered to avoid spamming non-AI entities.
	//------------------------------------------------------------------------------
	override static IEntity SpawnEntityPrefab(
		ResourceName prefab,
		vector origin,
		vector orientation = "0 0 0",
		IEntity parent = null
	) {
		IEntity e = super.SpawnEntityPrefab(prefab, origin, orientation, parent);

		string path = prefab;
		if (path.Contains("Character_") || path.Contains("Group_")) {
			PrintFormat("[FFWE_DEBUG] SpawnEntityPrefab '%1'", path);
		}

		return e;
	}
}
