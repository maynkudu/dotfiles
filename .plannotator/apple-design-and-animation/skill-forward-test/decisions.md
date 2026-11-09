# Photo adjustment fixture

Open `panel.html` directly. It contains its CSS, JavaScript, and original sample illustration. Choose photo accepts a local image. No packages, network resources, Apple artwork, font files, or symbol assets are required.

Exposure starts at 0.3 EV and accepts -2 to 2 in steps of 0.1. Native range and numeric controls edit one draft. Left, Center, and Right are native radio choices. Save commits both values for the current session. Restore returns both values to the most recent save. Reload starts a fresh session.

The moving image and selection pill translate horizontally toward the selected placement. A new radio choice evaluates the active spring at the input timestamp, retains position and velocity, and replaces the destination. The model uses placement intervals, with Left=0, Center=1, Right=2, omega=20 rad/s, and damping ratio=0.85. These parameters are local choices, not Apple constants. Reduced motion stops the JavaScript owner and applies the destination immediately.

The requested skill helped decide these behaviors:

- Foundations led to a content preview followed by associated controls, semantic color roles, inset corner radii, and text-aware reflow. The panel uses opaque surfaces because legibility matters more than a glass effect here.
- Interface patterns led to radios for placement and a nonmodal panel with explicit Save and Restore semantics.
- Elastic slider guidance established bounded, stepped values, exact entry, and keyboard access. A native range control supplies direct adjustment. Decorative overpull was not necessary for this task.
- Motion model and snapping guidance separated semantic selection from presentation, retained velocity during reversal, and used one spring owner.
- Offline motion supplied the executed sampler. Retarget events at 0.137, 0.423, and 0.711 seconds are evaluated at exact event times, including between output frames.
- Verification guidance led to real pointer and keyboard operation, startup and hot reduced-motion checks, enlarged text, runtime error inspection, and numerical checks separate from appearance claims.

The skill does not prescribe a complete numeric edit buffer policy, step tie policy, or persistence backend. This fixture preserves the last valid draft while numeric input is incomplete or invalid. Enter or blur clamps and rounds finite input to the nearest step. A halfway tie rounds toward the greater value. Empty input returns to the current valid draft. Save is an in-memory session commit. Exposure preview uses CSS brightness with multiplier 2^EV, so this is an interaction fixture rather than a linear-light photo processing pipeline.

Executed checks:

- `node numerical-check.mjs` passed. The written CSV was read back and verified as 241 finite data rows at 120 fps over two seconds. Position and velocity are continuous at each exact retarget time. Finite differences agree with velocity. Exports at 30, 60, and 120 fps agree at shared timestamps.
- `node browser-check.mjs` passed in an owned Agent Browser Chromium session. Checks operated numeric input, slider keyboard input, mouse drags beyond both bounds, Save, Restore, radio keyboard input, a real interrupted transition, local upload, reduced motion, and responsive text layout. The HTML and sampler spring implementations agree at forward and reversing test states.
- `wide.png`, `narrow.png`, `dark.png`, and `enlarged.png` were opened and visually inspected. The enlarged capture shows all controls in a full-page image. No runtime page errors were reported.
- The owned browser session `skill-forward-test` was closed after verification.

Observed failures and corrections:

- The first batch command used the wrong CLI argument shape. Quoted command arguments corrected it.
- Agent Browser rejected decimal mouse coordinates with a missing-arguments message. Integer coordinates allowed actual mouse checks to run.
- The first dark-mode capture exposed a dark disabled Save label. The enabled-only foreground rule corrected it. Dark primary hover and active colors were also adjusted.
- The first full enlarged-text capture exposed overlapping Center and Right labels. Viewport overflow alone had missed this. A container query now stacks placement choices when the text needs more room, and a label clipping check verifies the result. Stacked choices retain native selection feedback while the image still responds to placement.

No skill sampler or motion-model failures occurred. Native Apple rendering, exact visual fidelity, true 120 Hz browser presentation, screen-reader behavior, and a complete accessibility audit were not established. No production files, packages, commits, publishing, or subagents were involved.

Artifacts are all in this directory. `input-timeline.json` declares authored input and coordinate units. `placement-120fps.csv` is the sampled trajectory. `numerical-evidence.json` and `browser-evidence.json` contain executed assertions and the measured interruption state. The check scripts are reproducible locally with this installed skill and Agent Browser.
