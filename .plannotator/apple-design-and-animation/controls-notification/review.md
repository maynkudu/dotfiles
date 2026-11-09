# Controls and notification split

This is the requested correction to the approved Apple design and animation integration. The skill remains the main deliverable. Modulo's existing page structure, gallery, typography, source gate, and other components retain their existing treatment.

## Implemented behavior

Elastic Slider, Snap Rail, and Liquid Cluster share custom styled controls. Base UI supplies keyboard navigation, selection, switch semantics, collision-aware popup positioning, dismissal, and focus return. Controls include custom ranges, switches, an orientation dropdown, an action dropdown, and a right-click context menu. The menus use the same actions and preferences as the panel.

Liquid Cluster starts as one notification rectangle. Activating the notification or Separate opens a liquid seam into a notification card and Clear action. Clear dismisses the demo notification. Replay and Reset restore it. Independent hit targets and rigid text remain above the mask. Join, separate, and rapid reversal use the same spring. Reduced motion applies final geometry directly.

At narrow widths, the cards become taller and the decorative notification icon is omitted. Card width uses the root container's content width in both native and Canvas modes. This prevents absolute positioning from changing the measured width beneath the mask.

## Evidence

- [Desktop controls](controls-desktop.png), [orientation dropdown](orientation-menu.png), [action dropdown](actions-menu.png), [context menu](context-menu.png).
- [Joined notification](liquid-joined-desktop.png), [liquid bridge](liquid-bridge-desktop.png), [separated notification](liquid-separated-desktop.png).
- [390-pixel notification](liquid-390.png), [320-pixel notification](liquid-320.png), [full view at 390 pixels](full-view-390.png).
- [24 browser checks](checks.json), [browser errors](browser-errors.json), [reproducible check script](check.py).
- [24 installation/access assertions](install-check/results.json). Updated protected source was installed through the real Shadcn CLI. Three source/download/install comparisons and strict consumer TypeScript passed. The verification key was revoked and the temporary database and consumer removed.
- [Motion frame strip](liquid-motion-frames.png) and [public MP4](../../public/media/liquid-cluster.mp4).

Modulo lint, typecheck, production build, and the existing 72 route-handler access assertions passed. The skill's 12 numerical tests, metadata validation, and 55 local reference links passed. The installed skill resolves to the renamed local repository. The earlier independent 6.1 Sol skill exercise is recorded in that repository's tests folder.

## Source and scope

The first control implementation used native range, select, and checkbox rendering. Liquid Cluster used equal pills with height-derived corner radii. These were the causes of the requested presentation changes.

BLANK registry searches returned full-screen navigation menus. Overlay Menu was operated and its source read. Its curtain timeline and navigation scope do not fit these small controls. Bencho's Magnetic Select and DynamicLake's notification page were inspected as returned inspiration. Bencho source access was limited. No third-party implementation was copied. Modulo's installed Base UI supplied the existing accessible primitives.

Original Liquid Cluster implementation remains in `/home/maynkudu/Code/Projects/modulo-liquid-cluster/`. Modulo holds matching ignored copies, with updated local publication hashes. The system's liquid geometry reference now includes the notification construction recipe.

Private remote publication and fresh remote sync remain pending explicit commit/push authorization. No commits, pushes, deployments, Apple optics, native-device fidelity, or exact Apple reproduction are claimed.

The app reuses `http://modulo.localhost:1355`. The disposable `http://modulo-install-check.localhost:1355` server was stopped after verification.

Plannotator returned `decision: approved` for the final uncommitted implementation review, with no changes requested.
