# Representative motion proof

This isolated preview is original work for the proposed Apple motion skill. It demonstrates interaction mechanisms. It does not reproduce an Apple screen or claim Apple's implementation constants.

Open `lab.html` directly from the filesystem. It has no external assets, runtime dependencies, network calls or build step. The document and outer container have no background, padding, border or viewport height requirement.

## Controls

- Brightness stays between 0 and 100. Travel beyond an endpoint stretches only the rounded shell. Its opposite edge stays anchored. Horizontal compression preserves the shell's area. The sun and caption sit outside the transformed shell. Arrows adjust brightness by 5. Home and End select 0 and 100.
- The snap item follows horizontal pointer displacement. Its release destination is the nearest of three detents to `x + velocity / 8`. A marker shows the predicted destination during drag. Re-grabbing uses the current spring position, so the pointer offset stays intact. Buttons and keyboard input retarget the same spring.
- Circles use a polynomial smooth-union signed distance function on a small Canvas. A and B are separate HTML labels. The native range changes separation directly. Merge and Separate spring to the endpoints.
- Play sequence can be rerun or interrupted. It shows stretch, release, a snap, merging and separation. Reduced motion selects final states immediately.

## Mechanics and units

Settling uses the analytic underdamped spring solution with `omega = 20 rad/s` and `zeta = 0.85`. These are illustrative values, not Apple constants. Positions use pixels and velocities use pixels per second. Input timestamps start in milliseconds and convert once during velocity estimation.

Brightness springs latent raw overshoot `d` and its raw velocity. Each rendered frame maps raw distance through `sign(d) * L * c * abs(d) / (L + c * abs(d))`, with `L = 48 px` and `c = 0.55`. Rendered stretch therefore stays below 48 px even with an outward release velocity. Its derivative is `c * L^2 / (L + c * abs(d))^2`. `inspect()` exposes raw and rendered position and velocity separately.

Velocity uses the preceding 100 ms of samples, capped at 2500 px/s to limit outliers. A release more than 80 ms after the last actual displacement receives zero velocity. Holding after a flick cannot reuse its old speed. Cancel and lost capture settle with zero velocity. There is no pressure dependency.

The endpoint anchor remains fixed while the spring crosses its target. A negative extension compresses the same shell. Re-grabbing during this small compression retains the current shape and decays the caught compression with 12 px of pointer travel. The latent release velocity includes the derivative of this catch mapping. This is an illustrative catch policy, not Apple's documented algorithm.

Canvas evaluates radius 32 px circles with blend width 18 px. Coverage uses a one-pixel distance ramp. This is a shape approximation. It does not simulate fluid, light, refraction, volume or physical surface tension.

## Lifecycle and accessibility

The shared animation frame loop runs while a spring is active. Demo holds use finite timers. Hidden documents cancel the sequence and settle springs. Page hide also disconnects the resize observer. A persisted page show restores it.

The checkbox requests reduced motion. The system preference always applies, including changes while open. Reduced motion removes stretch and settling travel. Slider semantics, native buttons and the native range remain usable. Focus outlines are explicit. Capture has release, cancel and lost capture handling.

## Evidence and remaining checks

`window.motionLab.inspect()` exposes values, geometry, velocity, destinations, spring activity, pending animation frame state and reduced motion state. `reset()` and `playSequence()` support repeatable QA. Focused numeric helpers are under `motionLab.math`.

JavaScript syntax and a Node VM check passed. Numeric checks covered the rubberband bound and derivative, split-step equivalence of the analytic spring, and fresh versus stale release velocity. Synthetic event checks covered brightness clamping, cancellation, predicted snapping, re-grab continuity, lost capture, keyboard retargeting at 120 Hz, replay cancellation, manual and system preference changes, hidden-document cleanup and persisted-page restoration. The VM uses minimal DOM stand-ins and does not prove browser rendering or real device input.

Browser operation, responsive appearance, pointer behavior and hot system preference changes are not visually verified by the preview author. Root owns browser checks and evidence. Canvas raster quality and frame cost need that check before promotion.
