# Bombadil web verification

Use Bombadil for bounded exploration of changed or reported breaking web UI. It supplements Agent Browser's deliberate interaction and visual checks. It does not certify design quality, prove every path, or grant authority to change unrelated pages.

## Availability and installation

Run `command -v bombadil` and `bombadil --version`. The selected version is recorded in `~/dotfiles/setup.toml`. `python3 ~/dotfiles/bin/setup --tools` installs missing tools and preserves external binaries and existing managers. The official package is `@antithesishq/bombadil`. Its release package also provides types for specifications.

On this Arch Linux machine, 0.8.0 was installed from the official `bombadil-x86_64-linux` release under `~/.local/bin`. SHA-256 was checked against GitHub's release digest before installation. Do not replace that binary merely to normalize its manager. Missing tool/browser support is a reported blocker, not a passing check.

Read the installed `--help` and the relevant [manual](https://antithesishq.github.io/bombadil/browser/2.1-installation.html) before authoring a new specification. Follow the shared Context7 rule for documentation lookups. Version and options may change.

## Scope before exploration

Prefer an isolated fixture using actual production components with disposable auth/data and blocked external writes. Mark which boundaries are simulated. For the running app, use a verified local named HTTPS URL and public/read-only paths. Never fuzz a real signed-in profile, customer data, supplier hold/booking, payment, email, deletion or publication.

Define allowed URLs and action generators explicitly. URL boundaries limit navigation, not every subresource request or server side effect. A same-origin submit can still book, charge or send. Protect those boundaries in the fixture or test backend, not by hoping random exploration avoids them. Keep credentials, cookies and personal data out of CLI arguments and traces.

Use finite time limits and explicit viewport sizes. Trace outputs are files whose parent exists, not directories. Refuse overwrites unless replacing your own named artifact deliberately. Do not start untracked local servers; use agent-server and Portless.

## Focused properties

A top-level JavaScript/TypeScript specification exports properties and action generators only. Start with relevant defaults such as `noUncaughtExceptions`, `noUnhandledPromiseRejections` and `noConsoleErrors`. Add properties that express the reported defect or accepted behavior: no horizontal overflow, aligned controls, valid state transitions, draft retention, eventual loading completion, or no payment before confirmed review.

Use `extract` for browser state and `always`, `next` or bounded `eventually` for the property. Export filtered action generators instead of exporting both filtered and unrestricted defaults. Allow harmless interaction, keyboard, reload and scrolling only as appropriate. Expected application errors need explicit assertions rather than suppressing every error.

Example:

```sh
bombadil browser test --headless --exit-on-violation --time-limit 1m \
  --width 1366 --height 900 --output-path .plannotator/change/desktop.bin \
  https://kitse.localhost:1355 safe-spec.mjs
```

Without allow-url, exploration stays on the initial scheme/host/port; file targets stay on that file. With allow-url entries, include the initial target because those replace the implicit boundary. Use the installed match-pattern syntax. Regular Chrome/Chromium is supported; headless-shell is optional and must be available separately.

## Diagnose and verify

Never combine `--reproduce` with `--time-limit` or `--exit-on-violation`. Inspect the trace with `bombadil trace <file> --json` or `bombadil browser inspect <file>`. Reproduce a failure with the same origin, specification, viewport, browser and options using `--reproduce <trace>`. Reproduction may diverge; report that rather than calling it deterministic. Shrinking is optional and experimental.

Build a focused failing test or reproducible trace before fixing the defect. Fix its root cause within the authorized scope, rerun the original sequence and explore again. Preserve failing and passing artifacts. Do not weaken a property to hide a layout, timing or state failure.

The CLI distinguishes normal completion, execution error and property violations. Check the installed version's exit codes and inspect actual violations, not just process completion. Pair exploration with human-readable screenshots, keyboard/focus checks and watched motion.

Report tool installation, simulated fixture results and live app results separately. A bounded run with no violations proves only what its properties and explored actions covered. Record wider defects for approval; it is not permission to redesign or fix every page automatically. Close owned browsers and finalize managed servers when the authorized task and checks are complete.
