# SnapRail verification

Verified locally in Chromium through Agent Browser. The self-contained `fixture.html` mounts controlled, uncontrolled and one-detent rails inside React StrictMode. No dependencies were installed for the fixture.

## Browser evidence

`browser-results.json` records controller state at the checked interactions.

- Keyboard Home, End and destination buttons select and commit once. Independent rails do not change each other's selection.
- A native mouse flick released at 1,440 CSS px/s. Release at position 72 projected toward Center, target 266, and incremented the commit count from 7 to 8. The spring retained release velocity. The stored snapshot was taken during the subsequent settling frame.
- A native mouse drag followed by a hold released with zero velocity. The numerical stale-hold check verifies the 80 ms cutoff separately.
- A native mouse re-grab changed phase from settling to dragging with exactly zero position jump. Position remained 410.6401259091129 CSS px. Pointer ownership resets velocity for the new gesture.
- A dispatched `pointercancel` ended the gesture, restored selected geometry, and incremented cancellation without commit. This cancellation event was simulated after native pointer-down.
- Releasing native pointer capture delivered cancellation on the next pointer event. Final counts were 7 commits and 2 cancellations. The first lost-capture snapshot predates Chromium's event delivery.
- A controlled parent rejecting the Left request retained Right and target 532. The request still emitted one user commit notification.
- Manual reduced motion and a hot system preference both leave replay idle, with zero velocity, no timers and no pending frame.
- Disabled Home input, controller selection and replay retained the current selection. The slider has tabindex -1 and aria-disabled true. Destination buttons are disabled.
- One-detent Home, End and ArrowRight retain Only at the centered geometry without a keyboard commit.
- Actual scrolling suspends an offscreen rail. Switching to a second browser tab emits real visibility events and suspends hidden-tab animation and replay.
- Unmounting during two active replays destroys all three controllers, clears pending frames and replay timers, and empties the ready-controller map. Calls on old controllers do nothing. Remounting creates fresh controllers. One End keypress commits once and leaves the secondary rail at Center.
- At 390 x 844, document width is 390 and each rail is 338 px wide. Labels, destination buttons and fixture controls remain visible. The full screenshot is taller than the viewport by design.

`desktop.png` and `narrow.png` were inspected. They cover 1280 x 1100 and 390 x 844 capture conditions. Focus outlines are intentional. These are fixture layout checks, not pixel comparisons against an external design.

`a11y.json` records axe-core 4.12.1 on `.snap-rail`, with 15 passes, zero violations and zero incomplete checks. `page-errors.txt` records no fixture page errors. The only console message was React's development-tools suggestion.

## Numerical and source checks

Eight checks pass for finite ordered detents, stable projection ties, preview hysteresis, px/s velocity and stale holds, all spring damping regimes, split-time trajectory agreement, one-detent destinations and bounded visual overshoot.

Run using Modulo's existing Jiti dependency:

```sh
cd /home/maynkudu/Code/Projects/modulo
node --input-type=module -e 'import { createJiti } from "./node_modules/jiti/lib/jiti.mjs"; const jiti = createJiti(import.meta.url); await jiti.import("/home/maynkudu/dotfiles/.plannotator/apple-design-and-animation/snap-rail-evidence/motion.test.ts");'
```

The separate offline sampler passes seven checks for exact event-time retargeting, shared export frames at 30, 60 and 120 fps, authored releases, derivative-mapped bounded geometry, damping regimes, invalid configurations and CSV fields.

The earlier implementation pass completed scoped TypeScript and ESLint checks. Four original implementation files have identical SHA-256 hashes to their ignored Modulo copies. The local original repository has zero commits and no remotes. Modulo tracks none of the implementation files. `source-checks.json` records those checks.

## Scope

This verifies the reusable implementation and fixture. Complete Modulo build, access checks, component page integration, full-view rendering, media production and publication are owned by the parent task. Those results are not established by this fixture. Private repository publication and lock pins still require the user's authorization.
