# LiquidCluster verification

Verified the live Modulo route at `http://modulo.localhost:1355/components/liquid-cluster` in Chrome 156 through Agent Browser 0.37.1 on 2026-11-09. Reused the configured portless server without TLS. The owned browser session is closed.

The canvas joins and separates a common rounded background behind independent native buttons. Labels do not deform. The primary group uses controlled separation and selection. The second group uses local state.

- Enter and Space activate one button. Primary and secondary selections remain independent.
- Disabled primary buttons reject activation while secondary buttons remain usable.
- Join, Separate, Replay, and interrupted replay settle with zero velocity and no pending animation frame.
- Local and live system reduced motion render the requested final geometry without a settling frame or replay timer.
- Opaque mode produces alpha 255 and removes the canvas drop shadow.
- At 390 px, the page has no horizontal overflow. Joined native target gaps are exactly 8 px and buttons are 56 px tall. At 320 px, the group uses wrapped native buttons. Resizing restores the canvas renderer.
- Injected canvas failure preserves native activation, clears animation and replay state, and retains readable hover and focus treatment.
- Offscreen replay requests final geometry without scheduling animation. Removing and remounting the second group preserves primary state. Route navigation destroys the controller and removes its development global.
- The source section shows the locked key form. No implementation code is displayed.
- Strict standalone TypeScript and focused ESLint pass. Modulo TypeScript passed after catalog integration. Fresh browser sessions ended with zero uncaught errors.

The focused axe audit reported zero violations and 18 passes. Its five canvas-backed label contrast checks were incomplete because axe could not infer the background. Sampling the rendered fill at each target center and comparing it with computed text color produced 9.85:1 for every normal-state label.

Browser verification found and fixed two defects. A fallback hover rule removed the opaque fill, and integer button measurements reduced one target gap to 7.9 px. Final geometry and resize checks passed after the measurement fix. The original source and ignored Modulo copies have matching hashes in [structured results](./liquid-cluster-checks.json).

Evidence includes [desktop](./liquid-cluster-desktop.png), [joined](./liquid-cluster-joined.png), [narrow](./liquid-cluster-narrow.png), [320 px wrapping](./liquid-cluster-320.png), [two instances](./liquid-cluster-two-instances.png), [fallback focus and hover](./liquid-cluster-fallback.png), and [locked source](./liquid-cluster-source-locked.png).

This is a geometric adaptation of the researched grouping behavior. No Apple pixel comparison, Safari or native runtime check, screen reader check, or performance benchmark was performed. The root agent owns consumer installation, unlocked access checks, media, full builds, and repository checks.
