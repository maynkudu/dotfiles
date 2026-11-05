# Integrate and verify a scene

Read this when adding the artwork to a website, saving progress, exporting
layers, or packaging a completed scene.

## Copy editable source

Run the helper from the installed skill directory with an empty destination:

```sh
python3 scripts/copy_assets.py /path/to/project/src/interactive-art --react
```

Use `--react` for the optional `GardenCanvas` component. Without it, the helper
copies only the engine, stylesheet, and scene modules. It refuses to overwrite
an existing nonempty directory. Adapt these project copies to the requested scene.

The source uses TypeScript imports with `.ts` and `.tsx` extensions. A checked
Vite integration uses `moduleResolution: "Bundler"`, `allowImportingTsExtensions:
true`, and `noEmit: true`. Follow the host's compilation conventions when adapting
these imports.

## Mount a garden

For React, import the copied example:

```tsx
import { GardenCanvas } from './interactive-art/examples/GardenCanvas';

export function Artwork() {
  return <GardenCanvas initialTime={16} timeScale={1} fallback="/garden-still.png" />;
}
```

The component owns a mount and destroys it on unmount. Keep `onReady`, `onFrame`,
`onError`, and custom plant arrays stable across renders. Changing scene options
remounts the example. Use the controller from `onReady` for routine pause, seek,
or speed controls instead of rebuilding the scene.

For another framework, put a canvas in a positioned container with an explicit
size and mount the framework-independent module:

```ts
import { createGarden } from './interactive-art/scenes/garden';

const garden = createGarden(canvas, { initialTime: 16, seed: 1486 });
// Call from the host's unmount or disposal hook.
garden.destroy();
```

Keep the scene and target styles from `engine/scene.css`, including the focus
outline and separate canvas and target touch behavior. Give the canvas a text
description. Supply a still fallback exported from the finished scene.
`examples/garden-still.png` is the bundled garden's fallback. Copy it to the
host's public assets when using this garden, and regenerate it for a new scene.

## Controls and saved progress

The controller provides `pause`, `resume`, `setTimeScale`, `seek`, `bend`,
`snapshot`, `exportPNG`, `saveState`, and `destroy`. `snapshot` includes scene age,
visibility, reduced motion, rendering status, screen-space targets, and plant
geometry. It is useful for host controls and focused verification.

`onFrame` runs after a render. Keep drawing updates outside React state. Update
a time label only when its displayed value changes. Make the UI reflect pauses
and reduced motion so it does not offer an unavailable action.

Progress is per visit by default. When persistence belongs in the product, let the
host store `garden.saveState()`. Pass loaded data through `readGardenState` before
creating a new garden:

```ts
const saved: unknown = JSON.parse(storedText);
const options = readGardenState(saved);
const garden = createGarden(canvas, options);
```

Catch malformed saved data in the host and choose its fallback policy. The saved
state contains a version, seed, and age. It restores growth and composition, not
an in-progress drag. Custom plant definitions and cycle settings remain host
configuration and must be supplied again.

## Export artwork

Pause before exporting several layers so they share one pose:

```ts
garden.pause();
const full = await garden.exportPNG();
const plants = await garden.exportPNG({ layers: ['stems', 'leaves', 'blossoms'] });
const flowers = await garden.exportPNG({ layers: ['blossoms'] });
garden.resume();
```

The default output is 1000 by 680 pixels. Pass common `width` and `height` values
for another size, preserving the aspect ratio unless stretching is intended.
Each call returns a PNG `Blob`. The host can download it or use an object URL.
Restore the host's previous pause state after export rather than always resuming.

Inspect the actual files for alpha edges, attachment gaps, and clipping. Composite
individual exports in their declared order and compare with a full export at the
same pose. Transparent PNG compositing may introduce small rounding differences;
geometry, coordinates, and layer content must still agree.

## Focused verification

Use the host project's browser or device tooling. Test the finished integration,
including its controls and scrolling, rather than only the module in isolation.

- Grow from early to mature, reset, and cross a full lighting cycle.
- Hover, grab at an offset, pull beyond the limit, release outside, and cancel.
  Check root position, segment lengths, bounded displacement, and settling.
- Use the keyboard to activate each available object. Check focus visibility.
- Exercise touch dragging over an object and vertical scrolling over empty space.
  A desktop viewport change alone does not verify touch gestures.
- Pause, move offscreen, hide the tab, and change reduced motion while mounted.
  Verify that both clocks and render work stop, then resume appropriately.
- Mount two scenes. Destroy one, interact with the other, and repeat mounting.
  Check for leftover target elements, listeners, and running frames.
- Export selected layers and a still fallback. Inspect the exported images and
  compare the reconstructed composition.

Keep evidence for these scenarios with the task. Report missing device or
rendering evidence precisely. A typecheck validates interfaces, not animation.
