---
name: interactive-art
description: Build layered, interactive artwork for websites, including evolving scenery, growing plants, elastic objects, and ornamental or gacha-style environments. Use when artwork needs its own scene state and physical interactions.
---

# Interactive art

Build original artwork together with the behavior that makes its parts respond
to time and input. Deliver the editable scene, its runtime, and a working website
integration. The bundled garden demonstrates the construction; choose the
composition and subject from the current request.

## Define the scene

Inspect the supplied references and the host project. Identify the forms that
matter to the artwork: silhouette, repeated motifs, contour weight, internal
detail, texture, palette, depth, and empty space. Read `references/art-direction.md`
when designing new art.

Translate the requested behavior into objects with identity and state. A flower
can have a root, a segmented stem, leaves attached along that stem, a bud age,
petal opening, and an independently settling head. One rotation on the complete
flower cannot produce that deformation.

Define the clock before using elapsed time. Active visit time, wall time, a
scroll position, and a saved lifetime produce different experiences. Reuse a
choice already established by the user. For engagement-driven scenery, count
time while the scene is visible and let the host choose whether to persist it.

Read `references/scene-behavior.md` for the scene contract, clocks, growth, and
elastic construction. Reuse the host's rendering stack when it suits the scene;
the bundled Canvas runtime is a small dependency-free starting point. Use a
mesh renderer when the requested deformation or material requires one.

## Build an object that proves the approach

Construct the most demanding object at its intended display size. Give it actual
art, meaningful internal layers, real hit regions, and its complete interaction.
For a plant, prove the root, flexible stem, attachments, growing bud, pull limit,
and settling after release before multiplying it across a field.

Compare the rendered object with the chosen reference traits. Change its shape,
internal drawing, or material when it reads too simply. More particles, glow,
or noise cannot supply a missing silhouette or missing ornamental detail.

Image generation can supply painted parts when appropriate tools are available.
Preserve their alpha and reconstruction margins, then attach or deform those
parts through the scene model. A moving flattened picture does not establish
independent layers or elastic behavior.

## Compose and animate

Give each visible layer a name, stable object identities, and common world
coordinates. Paint from the background through the foreground. Store attachment
points with the object geometry so leaves, petals, ornaments, and effects follow
their simulated owner.

Use one authoritative clock per process. Growth changes geometry and structure;
lighting follows the day/night phase; physical response uses a stable simulation
step. A fast-forward control may accelerate scene age without accelerating a
user's drag. Bound particles, constraint iterations, and catch-up work.

Keep the grab point under the pointer. Apply forces or constraints to the object's
physical model, preserve its anchors, cap movement, and release cleanly on pointer
cancellation. Let connected parts settle according to their own stiffness and
damping. Hit regions must follow the same camera transform as the artwork.

Prepare touch and keyboard paths alongside pointer interaction. Scope touch
capture to interactive objects so a decorative scene can live inside a scrolling
page. Reduced motion needs a usable stable state and deliberate controls for any
meaningful state changes.

## Deliver and verify

Read `references/integration.md` when embedding, exporting, or packaging the scene.
Keep drawing, scene data, and lifecycle ownership understandable. Supply only the
integration code the host needs, with local cleanup and independent instances.

Deliver editable scene source and named layers. When still assets are requested,
export them at the same pose, coordinates, and size; inspect transparency and
the reconstructed composition. Include a useful still fallback for an animated
integration.

Operate the actual result. Exercise time progression, reverse or reset behavior
where supported, hover, extreme dragging, release, cancellation, and keyboard use.
Check pause, offscreen and hidden-tab behavior, live reduced-motion changes,
resize, and teardown. Verify the chosen touch behavior on the available surface
and identify any device behavior that remains untested.

Judge the final artwork at its intended size against the selected reference
traits. Report observable behavior and material visual gaps with the working
example. Distinguish the completed scene from extension points that have not
been implemented or tested.
