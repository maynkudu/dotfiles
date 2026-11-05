---
name: interactive-art
description: Build layered artwork for websites with evolving scenery, growth, and elastic pointer interactions. Use when illustrated objects need scene state, deformation, and independently animated parts.
---

# Interactive art

Build the artwork and its behavior together. Deliver editable scene code and a
working website integration. The bundled Canvas garden demonstrates the runtime;
choose the subject and composition from the current request.

## Establish the scene

Inspect the supplied references and host project. Identify the reference traits
that matter: silhouette, repeated motifs, contour weight, internal detail,
palette, texture, depth, and empty space. Read
[art direction](references/art-direction.md) when constructing new artwork.

Translate behavior into objects with identity, geometry, and state. A flower can
have an anchored stem, attached leaves, a bud age, opening petals, and a flower
head that settles separately. Rotating the whole flower does not bend its stem.

Choose the clock from the requested experience. Active visit time, wall time,
scroll position, and saved lifetime produce different results. Engagement-driven
scenery should count time while visible unless the user specifies otherwise.
Let the host decide whether to save progress between visits.

Read [scene behavior](references/scene-behavior.md) for the bundled scene contract,
growth, elasticity, input, and layer model. Reuse a host renderer when it suits
the work. The Canvas runtime is a dependency-free starting point; textured mesh
deformation can justify a WebGL renderer.

## Prove the demanding object

Build one representative object at its intended display size before filling the
scene. Give it actual artwork, attachment points, hit regions, and the complete
interaction. For a plant, prove its growing geometry, anchored root, flexible
stem, bounded pull, and return after release.

Compare the rendered object against the selected reference traits. Improve its
silhouette and internal ornament when it reads too simply. Glow, particles, and
noise cannot supply missing drawing detail.

Use generated or supplied raster parts when appropriate. Preserve transparency
and enough hidden artwork for bending and overlap. Follow the available image
generation workflow when needed. Attach or deform those parts through the scene
model instead of treating a flattened image as independently moving assets.

## Compose and integrate

Keep stable object identities and named layers in shared world coordinates.
Store attachment points with geometry so leaves and ornaments follow their
simulated owner. Growth changes geometry; lighting follows scene age; physical
response advances with a fixed simulation step. Changing growth speed must not
change how dragging behaves.

Read [integration](references/integration.md) to copy the bundled modules, embed
the scene, save progress, or export artwork. The helper copies editable source
into an empty destination and leaves the host's framework and storage policy to
the agent. Inspect the copied code before adapting it.

Preserve the grab offset, anchors, and movement limits. Release input on pointer
cancellation, pause, or teardown. Scope touch capture to interactive objects so
the surrounding page can scroll. Provide keyboard actions and a useful stable
state for reduced motion. Bound catch-up work and live object counts.

For a new subject, replace the garden's scene model and painters. The runtime
owns scheduling, visibility, resize, input targets, export, and cleanup. Its
elastic chain solver can support other anchored flexible objects. It does not
provide character rigging, mesh skinning, collisions, or a general game editor.

## Deliver against the real result

Deliver the scene source, named layers, host integration, and a still fallback.
PNG layer exports are snapshots at one pose; the editable source retains the
behavior. Export layers at a common time and size so they reconstruct the scene.

Operate the result. Exercise growth and reset, a complete lighting cycle, hover,
extreme pulling, release, cancellation, and keyboard input. Check pause,
offscreen and hidden-tab behavior, live reduced-motion changes, responsive hit
regions, independent instances, and teardown. Verify relevant touch gestures on
the available browser or device and identify any untested device behavior.

Inspect the artwork at its intended size and inspect actual exported images.
Report the working example, observed behavior, and material visual or integration
gaps. Keep the garden example distinct from new scene types that have not yet
been built or tested.
