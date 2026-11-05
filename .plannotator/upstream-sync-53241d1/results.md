# Upstream integration results

Source checked on 2026-11-03: `kiritocode1/dotfiles` main at
`53241d10f6bd2b1963599386a98741df8d20c0be`.

## Integrated changes

- `4db9c0b`, `bc9bc5b`, and `53241d1`: all seven isometric pixel games files,
  including the launch status correction and concrete 3x PNG export example.
- Previously omitted part of `0a1baec`: all nine tstack skills pinned to
  `1085050f3baed1ac724caa4a8166145fb2ac88af`. Its design-system update was
  already pinned locally and remains unchanged.
- Register the bundled skill in `setup.toml`, record tstack in the lock and
  historical inventory, and document the additions.
- Restore declared helper permissions during installation. GitHub ZIP
  extraction otherwise removes the executable bit from `pr-wait`.

Both plans were approved. Codex discovers all ten additions through
`~/.agents/skills`; Claude has links to the same directories. Existing
providers, personal rules, Arch setup, Google SEO, and Rune Icons remain unchanged.

The final Plannotator code review was approved with no changes requested.

## Verification

- [Upstream blob comparison](upstream-blobs.log): all seven bundled files match.
- [tstack blob comparison](tstack-blobs.json): all fourteen files match the
  pinned source, including agent metadata and the executable helper.
- [Setup tests](setup-tests.log): five pass. The new test checks helper
  permissions, dry run, repeat installation, and unchanged file content.
- [Repository checks](repo-check.log) and [installed checks](installed-check.log): pass.
- Rules build and installation: zero generated rule changes.
- [Starter checks](starter-results.json): weak throws produce zero skips,
  strong throws six; five stones end the round at eighteen; restart restores
  five stones and zero score while retaining the best. Launch status updates
  immediately. The concrete still-export mechanism creates a 1080 by 840 PNG.
- Real Space input consumes a stone and returns to aim. Rules opens and
  Escape closes it. Sound toggles its label and `aria-pressed`.
- [Desktop](starter-desktop.png) at 1280 by 800 and
  [phone-sized viewport](starter-mobile.png) at 390 by 844 inspected.
  The phone-sized canvas is 360 by 280, integer-scaled, with no horizontal overflow.
- [Reduced motion](reduced-motion.json): the media query and engine flag are true.
  Browser error and console logs are empty. The disposable browser is closed.
- The installed `pr-wait --help` runs successfully. No PR watcher, review
  workflow, model configuration, commit, push, or merge was executed.

The intentionally excluded macOS setup and original author's personal tools
remain excluded. Provider-dependent tstack workflows and actual mobile-device
behavior are not tested. The imported upstream code is unchanged, not redesigned.
