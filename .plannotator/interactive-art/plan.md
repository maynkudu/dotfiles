# Interactive art skill and scene engine

## Goal

Create `interactive-art`, a skill that builds original layered artwork with behavior
and delivers it as an embeddable website scene. A scene can change with time,
grow new forms, respond to hovering, and let people pull elastic objects.

The first working example is an ornamental lotus garden. Its stems bend along
their length, its leaves follow their attachment points, and its flower heads
lag behind the stems. Buds open as the scene ages. Day and night repeat.

## Working preview

- [Interactive prototype](prototype/preview.html)
- [Recorded interaction](videos/garden-interaction.mp4)
- [Day](prototype/day.png), [night](prototype/night.png),
  [held flower](prototype/drag.png), and [phone layout](prototype/phone.png)
- [Browser check results](prototype/verification.json)
- [Proposed skill entrypoint](skill-draft.md)

This is an original procedural interpretation of the supplied artwork. The lotus
reference informed the pointed overlapping petals, visible veins, dark contours,
and ivory/violet palette. The other references establish the broader direction
for future scenes: paisley, scrolling foliage, radial ornament, and detailed
border work. Their colors and subjects are references, not fixed requirements
for every output of the skill.

The example opens partway through its growth cycle so several stages are visible.
"Start again" resets scene time. "Advance 20 seconds" and the speed control make
the state changes easy to inspect. Those controls belong to the example and do
not have to appear in a website integration.

### What is already demonstrated

Desktop pointer input bends flowers and can hold and pull one. The root stays
fixed, the stem retains its segment lengths, and the flower returns after release.
The maximum pull is enforced in the simulation. Keyboard activation of "Bend
lotus" produces the same physical response.

The prototype also demonstrates bud opening, repeating daylight, a pause control,
live reduced-motion changes, responsive drawing at a 390 px viewport, and cleanup
that stops its frame loop. These checks run in Chromium. Mobile-device touch
behavior and the final reusable module boundaries still need verification.

## Proposed implementation

```text
Reference artwork and requested behavior
                  |
              Scene definition
                  |
       Clock + elastic simulation
                  |
             Ordered art layers
                  |
      Website component + editable assets
```

Use Canvas 2D for the first renderer. It can draw curved stems and petals from
their current simulated geometry and can combine those with textures. The skill
will reuse a project's existing renderer when that is appropriate. A WebGL
renderer becomes useful when a requested scene needs textured deforming meshes,
shaders, or a scale that the Canvas renderer cannot handle well.

The reusable runtime will own visible time, frame scheduling, resize handling,
visibility, reduced motion, and teardown. Scene code will own objects, growth,
layer order, painting, hit regions, and the response to input. The stem solver
will be reusable by plants and other anchored elastic objects.

### Time and persistence

Scene time controls growth and lighting. Time scale changes those processes
without changing the physical response to dragging. Physics runs with a fixed
step and a bounded catch-up budget. The clock pauses when the scene is offscreen,
the tab is hidden, or the host pauses it.

Progress starts per visit by default. Expose serializable elapsed time and a
seed so a website can resume a scene. The host can opt into local or account
persistence without putting storage policy in the drawing code.

### Layers and art

Keep stable object identities, world coordinates, attachment points, and layer
names. Background, water, foliage, stems, blossoms, and foreground detail must
remain individually addressable. Support a transparent composition and still
exports of selected layers at a shared size and pose.

The skill must produce new scene composition and art for a new request. The
garden is a working construction example. Its geometry, palette, species,
density, timing, and behavior can be changed independently. Detailed guidance
will cover silhouettes, internal ornament, material texture, occlusion, and
the relationship between a painted part and its simulated attachment.

### Input and integration

Keep flower hit regions in the same coordinate system as the rendered geometry.
Preserve the grab offset, cap pull distance, and release capture on cancellation,
pause, or teardown. Add small accessible interaction targets for touch and
keyboard use so vertical page scrolling still works in the surrounding scene.

Deliver a framework-independent module and a small React integration example.
Mounting owns its listeners and observers. Unmounting cleans up only that scene.
Verify two instances on the same page. Reduced motion presents a stable garden
with explicit controls for changing scene time.

## File responsibilities

| File or directory | Responsibility |
| --- | --- |
| `skills/skills/interactive-art/SKILL.md` | Trigger, workflow, completion criteria, and reference routing |
| `agents/openai.yaml` | Discovery metadata and normal automatic invocation |
| `references/art-direction.md` | Constructing detailed original art and adapting the supplied visual vocabulary |
| `references/scene-behavior.md` | Time, growth, elasticity, attachment, hit regions, and behavior design |
| `references/integration.md` | Website use, React lifecycle, persistence, exports, and verification |
| `assets/engine/` | Reusable runtime and elastic solver |
| `assets/scenes/` | Garden definition, growth model, and layered painters |
| `assets/examples/` | Runnable example and integration usage |
| `scripts/` | Only the helpers needed to prepare or validate those deliverables |
| `setup.toml` | Register the local skill for Codex and Claude |
| `skills/README.md` | Document the new skill and its engine |

All paths after the first row are relative to the new skill unless they name a
repository file. Preview and review evidence stays in this `.plannotator` folder.

## Completion checks

1. Repeat the real hover, drag, extreme pull, release, cancellation, and keyboard
   paths. Check anchored roots, bounded displacement, and settling over time.
2. Verify growth at early and late ages, daylight at both ends of a full cycle,
   and clock behavior when paused, hidden, or offscreen.
3. Verify startup and live reduced-motion changes, responsive hit regions,
   touch input, and ordinary vertical page scrolling.
4. Verify two independent scene instances and repeated mount/unmount cleanup.
5. Compare selected transparent layer exports with the corresponding full
   composition. Inspect actual exported images and the integration example.
6. Validate skill metadata and references, run the repository checks, install
   the local skill, and check discovery for both active agents.
7. Review the implementation in Plannotator and leave the new work uncommitted.

## Scope and limitations

This first version supplies a small interactive art runtime and a complete garden
example. It does not include a general game editor, character rigging, multiplayer,
or a backend. Those are separate extensions when a real scene needs them.

The supplied raster images establish visual direction. The current example uses
original procedural drawing and needs no image-generation service. Matching the
full painted texture of a supplied image is a separate art requirement that must
be evaluated on the output when requested. This plan does not claim an exact
reproduction of any reference.
