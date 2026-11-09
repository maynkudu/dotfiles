# Elastic Slider verification

Verified on 2026-11-09. This is an original adaptation of the approved motion proof, not an exact Apple control reproduction.

## Files and API

Original source is in `/home/maynkudu/Code/Projects/modulo-elastic-slider`. It has a local Git repository with no commits or remotes. The installable files are `ElasticSlider.tsx`, `create-elastic-slider.ts`, `slider-math.ts`, and `elastic-slider.css`. Original development files include `slider.test.ts`, `fixture.tsx`, `fixture.html`, `fixture-server.ts`, `package.json`, `tsconfig.json`, and `.gitignore`. The local `node_modules` symlink is ignored.

Installable files were copied with `cp` into ignored `modulo/src/registry/elastic-slider/`. All four original and copied file bytes match. [Source checks](source-checks.json) includes their final SHA-256 values. `git check-ignore` succeeds and `git ls-files` returns no tracked Elastic Slider implementation.

Public integration owned by this task is `src/components/elastic-slider-demo.tsx`, `src/components/elastic-slider-demo.module.css`, and `src/app/components/elastic-slider/page.tsx`. Catalog, media, full views, lock entries, registry output, and publication belong to the root task.

`ElasticSlider` requires `label`. Use controlled `value` with required `onValueChange`, or uncontrolled `defaultValue` with optional `onValueChange`. The union excludes using both value props. Defaults are min 0, max 100, step 1, horizontal orientation, and enabled input. `step="any"` preserves continuous pointer values, with keyboard increments of one percent of the range. Steps are counted from min. Both bounds remain reachable even when max is off the step grid.

Optional props are `orientation`, `disabled`, `reducedMotion`, `onValueCommit`, `formatValue`, `children`, `className`, and `onReady`. Children are rigid decorative content outside the shell transform and must be noninteractive. The input target, visible label, and readout remain outside shell deformation.

Controlled changes are bounded, normalized requests. Displayed fill and accessible value remain owned by the controlled prop. A successful release commits the requested value once. Cancellation does not emit a commit. Uncontrolled live changes remain after cancellation. A controlled owner change during drag rebases semantic input while preserving current shell geometry. A stationary release retains that owner change.

The stable controller has `update(fullOptions)`, `snapshot()`, `replay()`, and `destroy()`. Snapshot includes accepted value, proposal, phase, latent and rendered stretch, velocity, release velocity, measured length, frame/replay state, visibility, reduction preference, and destruction status. Replay is finite simulated endpoint input for deterministic media. User input and lifecycle changes cancel it.

Keep `onReady` stable. It receives the controller on mount and null on cleanup. Value, orientation, preference, and callback prop updates retain the instance. Replacing `onReady` itself while mounted is not a separately supported notification protocol.

## Checks

`bun test` passed eight focused cases. They cover a nonzero step origin, semantic bounds, decimal cleanup, large finite minimums, continuous values, invalid input, off-grid maximum keyboard behavior, uncontrolled cancellation, controlled requests and owner reconciliation, bounded rendering throughout an opposing-velocity spring, and stale hold/reversal velocity.

`bun run typecheck` passed in the original project. Focused ESLint passed for the public page and demo. Repo-wide build, lint, access, and consumer installation are handled by the root task.

The isolated Agent Browser fixture produced [19 recorded observations](browser-checks.json), including repeated holds and re-grabs. All recorded checks passed. It exercised actual mouse capture, native lost capture, injected pointer cancellation, both orientations, shell bounds, rigid label/target geometry, controlled rejection, owner overrides during drag and release, disabled input, system reduced-motion hot changes, unmount cleanup, and remount. The pointercancel case was scripted. Native operating-system interruption was not separately tested.

The actual Modulo route produced [five recorded checks](modulo-checks.json). Desktop pointer stretching, narrow orientation/bounds, keyboard commit, a hot preference prop without controller replacement, and offscreen animation stoppage passed. The final math source was rechecked on the route with End followed by ArrowLeft, yielding 85 on the demo's five-unit grid.

[Desktop preview](modulo-desktop.png) was inspected at 1360 by 1000. [Narrow preview](modulo-narrow.png) was inspected at 390 by 844. Both preserved the existing Modulo layout and had no horizontal overflow. The narrow stage keeps margin around the maximum shell stretch.

[The preview accessibility audit](modulo-a11y.json) reports zero violations and zero incomplete checks with axe-core 4.12.1. Fixture and Modulo JavaScript error logs were empty. These checks do not establish compatibility with every screen reader, native device, or browser.

The isolated fixture used `http://modulo-elastic-slider.localhost:1355` through the existing HTTP portless proxy. Its owned server was stopped and the owned browser session was closed. The shared Modulo server remains at `http://modulo.localhost:1355`.

## Remaining boundary

No commit, push, GitHub repository, or remote was created. Private publication, a real full commit pin, and fresh-checkout source sync remain unverified. Local copied-source behavior does not prove reproducibility from a published source pin. No Apple constants, proprietary material fidelity, pixel match, or native-device behavior is claimed.
