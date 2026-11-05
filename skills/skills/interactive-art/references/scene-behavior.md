# Scene behavior and runtime

Read this when constructing a scene or changing growth, physical response, or
interaction. The TypeScript modules are editable source with no runtime package
dependencies. The React example is optional.

## Responsibilities

| Module | Owns |
| --- | --- |
| `assets/engine/runtime.ts` | Frame loop, visible time, pointer capture, keyboard targets, resize, layer export, and cleanup |
| `assets/engine/elastic.ts` | Anchored joints, rest geometry, length constraints, pull bounds, head damping, and attachment coordinates |
| `assets/engine/math.ts` | Points, interpolation, colors, and seeded randomness |
| `assets/scenes/garden.ts` | Plant definitions, growth, hit regions, scene response, layer order, and drawing |

`SceneDefinition` in the runtime is the contract for a different scene. `update`
applies elapsed scene time, `step` advances physical state, `paint` draws selected
layers, and `targets` returns accessible interaction regions. `activate` handles
keyboard input. `release` clears temporary interactions. `inspect` supplies
scene-specific state for the host and focused checks.

The renderer receives a world-sized context. Hit regions use those same world
coordinates. The runtime translates pointer positions and positions DOM buttons
over the regions. Keep scene-specific coordinate corrections in the scene model.

## Clocks

The bundled runtime advances physics at 120 steps per second, with at most six
catch-up steps in a frame. It discards long suspended intervals. `timeScale`
multiplies scene age while physics retains its fixed step. A zero time scale
freezes growth and lighting while preserving physical interaction.

Pause, a hidden tab, an offscreen canvas, and reduced motion stop both clocks and
the frame loop. Resuming clears the previous timestamp and accumulated time.
`seek` applies a deliberate scene age and resets the pose. It works while paused
or under reduced motion.

The garden uses age for stem growth and petal opening. Plants have individual
delays and durations, so the initial view contains different growth stages.
Lighting repeats independently of the one-way growth process. Resetting age
reconstructs the appropriate geometry instead of playing the simulation backward.

## Flexible objects

An elastic chain has fixed rest points, moving joints, segment lengths, and a
maximum displacement from the rest tip. Growth updates its rest geometry. The
solver keeps the root fixed, applies damped forces, enforces segment lengths,
and clamps the tip after each constraint pass. The head has separate angular
velocity and damping.

`attachment(chain, progress)` gives the current position and tangent along a
chain. Use it for an ornament whose location falls between joints. Discrete
attachments can use an existing joint and its neighbor, as the garden leaves do.

The pull bound represents material resistance. The pointer can move beyond it,
while the object remains inside it. The solver is tuned for anchored plants and
similar objects. It does not solve collisions, self-intersection, or cloth meshes.

## Input and lifetime

Capture a pointer only after identifying an interactive object. Keep the press
offset so grabbing does not reposition the object. Use the same camera conversion
for drawing and hit testing. Clear capture and temporary targets on release,
cancellation, loss of capture, pause, invisibility, and destruction.

The garden's transparent DOM buttons provide keyboard and touch targets. They
use `touch-action: none`; the canvas uses `pan-y` so blank areas can scroll.
Keyboard activation bends a selected flower through its physical model. Under
reduced motion, disable continuous physical actions and keep explicit time
controls available.

Each mount owns its observers, abortable listeners, frame, and generated target
elements. Destroying one scene must leave other scenes and host listeners intact.
Repeated destruction is harmless.

## Exportable layers

Keep names and paint order stable. The garden separates sky, celestial objects,
landscape, water detail, pads, stems, leaves, blossoms, foreground grass, and grain.
All exports share world coordinates and a pose. A layer without an opaque
background exports with alpha. Include the sky for an opaque complete scene.

Layer exports preserve the selected drawing, not its future animation. Keep the
source modules with the PNGs when the output needs to remain interactive.
