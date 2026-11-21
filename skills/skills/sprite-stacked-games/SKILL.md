---
name: sprite-stacked-games
description: Build browser games with rotatable layered pixel art. Use for sprite-stacked racing, drift, delivery and vehicle games, preparing slice assets, tuning arcade handling, or extending a game made with the Sprite Racer engine.
---

# Sprite-stacked games

Build a playable loop using a known runtime, then change the world and rules. The engine and its example game are separately installed source. Keep the skill usable without an image generation service.

## 1. Establish the game and host

Read the host project and the entire game entry point. Identify renderer, language, asset directory, input ownership, simulation clock and mount/cleanup path. Record the player's goal, controls, failure/recovery and a completed attempt in one paragraph.

For an existing game, reuse its renderer and loop. Read [integration](references/integration.md) before adding sprite stacking to a host engine. For a new game, locate an authorized local Sprite Racer source directory or raw unlocked registry JSON. Run `node scripts/create-game.mjs --source <source-directory-or-registry.json> --out <empty-directory> --template delivery --title "Coast Courier" --map coast --car pickup` from this skill's directory. Use `--template racer` for the circuit game. The command checks every source checksum before writing and refuses a populated destination. Run `bun run build` and `bun run test` in the generated directory. `bun test` invokes Bun's separate test-file discovery and does not run this generated package's portable check script.

If source is not installed, set an active mint key in `MODULO_REGISTRY_KEY` through the host's secret input and run `node scripts/fetch-source.mjs --out <new-registry.json>`. Keep this raw payload local. Shadcn may reformat installed TypeScript, so use the raw payload for byte-exact checks. The skill contains no private runtime. Without authorized source, report that dependency instead of claiming to have generated a game.

Completion: the untouched starter boots, its tests pass, and the new game's scope names a complete play loop.

## 2. Author and inspect the assets

Use a supplied slice strip or author original horizontal layers with the runtime's asset recipe. Store the ground slice first and declare width, height, layer count, ground pivot, and forward axis. Keep the physics collision shape separate from visible pixels. Read [slice assets](references/slice-assets.md) when importing a PNG strip, converting views, or changing the camera.

Render the actual asset at 0, 45, 90, 180 and 270 degrees, then inspect a full turn. Inspect an exploded stack as well. Check wheels, windows, roofs, narrow posts, alpha fringes and the pivot. Correct the source layers when a part vanishes or fills incorrectly. Preserve provenance and notices for reused code and art separately.

Completion: every asset has a reproducible source, a valid layer manifest, and inspected multi-angle output.

## 3. Make the game through its own modules

Keep rendering, vehicle handling, the clock and input reusable. Put track shape, checkpoints, destinations, scoring, race state, artwork and HUD in the game modules. Read [driving and rules](references/driving-and-rules.md) for circuit, drift and delivery branches.

Tune handling with numbers before changing the integrator. Simulate floating-point positions at a fixed step; snap displayed coordinates only. Keep heading independent of velocity. Preserve capped lateral grip, explicit reverse behavior, off-road transitions and bounded collision impulses. A recorded ghost stores sampled transforms; it is visual playback, not a guarantee of identical physics across browsers.

Read [content definitions](references/content-definitions.md) when adding circuits or vehicles. The example has five circuits, a drift yard and six original car recipes; each car/map combination must finish a legal attempt. Key records and ghosts by both selections.

Expose state snapshots and explicit test inputs through an opt-in development controller. Create one successful attempt and one recoverable failure through the actual game rules. Verify ordered checkpoints before showing a completed lap. Add a focused invariant for each discovered bug.

Completion: a player can start, act, finish or fail, understand the result, and restart without reloading.

## 4. Verify the actual page

Run the runtime and game tests, then operate the browser. Use the host's browser workflow, owned sessions and named local server. Test keyboard, simultaneous controls, pointer release/cancel, pause/resume, restart, hidden-tab release, narrow layout, reduced motion, storage failure and teardown. Reduced motion preserves driving and removes camera effects and decorative particles.

Check the car against scenery at different depths, check slow turning at the shipped scale, and measure a representative populated scene. Keep fixed-step catch-up bounded after a stall. Read [verification](references/verification.md) for the concrete acceptance scenarios.

Completion: publish exact checks, captures and remaining gaps. A scaffold/build result establishes those operations only. A skill is ready for dotfiles only after a fresh invocation produces and verifies another game without modifying the shared engine.
