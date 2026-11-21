# Verification

Keep a report for the actual source revision and generated game.

1. Scaffold to a separate empty directory. Build there and run the source's tests. A populated output directory and a corrupted source hash must fail before any copied file is written.
2. Capture the shipped car at canonical angles, a full turn, and separated layers. Compare the zero-angle reference composite at the native art resolution.
3. Test stationary behavior, acceleration, braking, reverse heading, left/right symmetry, handbrake slip, surface grip, bounded stalls and fixed-step cadence independence.
4. Complete the game's real success path. Exercise a failure/recovery path and restart. For racing, reject missing gates, reverse crossings and off-road completion.
5. Operate the actual DOM controls. Verify held input releases on keyup, pointerup, pointercancel, blur and hidden tabs. Check simultaneous steering and throttle. Verify native dialog focus and Escape behavior.
6. Inspect desktop, tablet and narrow browser viewports. Check overflow, readable HUD text over different scenery, tap targets, audio gesture gating, live reduced-motion changes and malformed/unavailable storage. Inspect console errors.
7. For skill evaluation, give a fresh invocation the skill and installed runtime. Ask it to build a delivery or drift game in a separate directory. Record exact source inputs, changed files, engine hashes before/after, resulting controls/rules and browser evidence. Grade the generated game against its own success and failure conditions. Keep this live evaluation separate from deterministic helper tests.

Record unavailable tools and any unverified sound, device or performance behavior. Keep the skill as a local draft until this evidence has been reviewed.
