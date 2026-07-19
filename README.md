# Echoes of the Nexus

Original Minecraft Bedrock Edition RPG addon with a 100-level story, 10 unlockable worlds, per-player progression, multiplayer boss support, custom items, NPC/story data, teleport gates, and multiple endings.

## Install
1. Run `python3 scripts/build.py` to generate binary assets and archives locally.
2. Open `dist/EchoesOfTheNexus.mcaddon` with Minecraft Bedrock Edition.
3. Enable both the Behavior Pack and Resource Pack.
4. Enable Beta APIs/Script API experiments if your Bedrock build requires them.
5. In game, run `/scriptevent nexus:menu open` to open the Nexus menu.

## Gameplay
- Each player receives private dynamic-property progress: level, XP, quest, stage, unlocked worlds, and ending alignment.
- Complete 100 story levels across the ten worlds in `EchosOfTheNexus_BP/scripts/story_data.js`.
- After level 50, every new level has a 3% chance to awaken Second Stage; level 100 guarantees it.
- Players may share coordinates, trade items, and fight spawned bosses together while retaining personal quest progression.

## Development
- Behavior pack: `EchosOfTheNexus_BP/`
- Resource pack: `EchosOfTheNexus_RP/`
- Build script: `scripts/build.py`
- Generated build artifacts (not committed): `dist/`

## Repository policy
Binary files are intentionally not tracked. Generated PNG, WAV, `.mcaddon`, and ZIP files are recreated by `python3 scripts/build.py`.
