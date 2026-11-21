# Integration

For a new browser page, give one runtime sole ownership of requestAnimationFrame, input and audio. A framework adapter mounts into a host and destroys that instance on unmount. Keep game state out of React's frame-by-frame render path. DOM controls call runtime methods and receive throttled snapshots.

For an existing Canvas game, use its canvas, camera and object ordering. A stack needs one layer image per height, a shared pivot, rotation about that pivot, vertical camera squash and a screen-space layer lift. Reuse the host's texture filtering. Draw complete stacks in the existing scene order.

For another game engine, adapt its native sprite draw API and existing clock. The asset format and gameplay separation remain useful; the browser runtime is not a second renderer to embed.

Use ground-contact ordering for separated ground props. Large intersecting footprints, bridges and multiple elevations need a deliberate occlusion strategy. Check that requirement before promising a flat-world runtime can implement the scene.

Keep source access separate from public play. A public preview's compiled JavaScript is visible by design. Keep original installable files, source manifests, mint keys and credentials out of public JSON and static asset directories.
