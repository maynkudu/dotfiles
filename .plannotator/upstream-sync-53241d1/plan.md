# Sync the latest upstream skill

## Goal

Integrate the three new commits from `kiritocode1/dotfiles` through
`53241d10f6bd2b1963599386a98741df8d20c0be`, preserving this repository's
Arch setup, maynkudu identity, Google SEO skill, and Rune Icons preference.

The previous local sync covers the portable changes before `0a1baec` and its
design-system update. Its nine tstack skills are still missing. Include that
omitted part too. Do not reintroduce the intentionally excluded macOS configuration,
personal account tooling, Pi provider defaults, or upstream review artifacts.

## Upstream changes

| Commit | Change |
| --- | --- |
| `0a1baec` | Add nine tstack workflow skills at `1085050f3baed1ac724caa4a8166145fb2ac88af`. The design-system update to `7ba4371` is already pinned locally. |
| `4db9c0b` | Add the isometric pixel games skill, MIT renderer, page shell, stone-skipping starter, and two technique references. |
| `bc9bc5b` | Set the starter's status to `watch it skip` when the stone launches. |
| `53241d1` | Add a concrete nearest-neighbour PNG export example for still illustrations. |

## Proposed integration

```text
upstream 53241d1
  -> skills/skills/isometric-pixel-games/   seven unchanged files
  -> setup.toml [skills].local              register the bundled skill
  -> bin/setup --skills                    link for Codex and Claude
```

Import all seven files byte for byte. The renderer draws a fixed isometric
pond; holding charges the throw and releasing launches a stone. Its floating
indicator points down, not northeast. The engine and shell pass Node syntax
checks in an isolated reference directory.

The bundled-skill installer change is appending `isometric-pixel-games` to
`setup.toml`'s local skill list. This list, not the historical manifest,
controls installation. Add a short note to `skills/README.md` identifying the
bundled skill and its licensed assets.

Also add one pinned `t3dotgg/tstack` entry to `skills/sources.lock.json` and
record the nine names in the historical `skills/manifest.toml` inventory:
`babysit-pr`, `council`, `file-pr`, `full-send`, `full-stop`,
`leaving-pr-comments`, `modernize`, `sol-loop`, and `takeover`. Install their
unchanged source directories through `bin/setup --skills`; retain support
scripts and agent metadata. There are no naming collisions. The upstream
empty patch declarations need not be copied because they apply no changes.

The GitHub ZIP installer discards executable bits. Declare `scripts/pr-wait`
in the pinned skill's `executables` list and have `bin/setup` restore those
permissions without changing file content. Add one focused installer test
covering dry run, repeated installation, permissions, and unchanged content.

Installation does not invoke these workflows, configure additional models,
or authorize a commit, push, PR, or merge. Existing instructions still take
precedence. Review-oriented skills may need other providers when explicitly
invoked. No changes to rules, providers, existing public pins, shell
configuration, or existing skills are needed.

## Verification

- Compare all seven imported files against the fetched upstream blobs.
- Validate the nine pinned tstack paths and compare all installed supporting
  files against `1085050`, including executable permissions on `pr-wait`.
- Run the rules build and repository integrity check. Generated rules should remain unchanged.
- Run the existing focused setup tests. Do not add tests for unchanged upstream internals.
- Open the actual starter in a disposable Agent Browser session. Check launch
  status, good and bad throws, round reset, Rules, sound toggle, keyboard input,
  desktop and phone-sized rendering, and console errors.
- Inspect the skill installer dry run, then install the selected skills and
  verify discovery through both active clients' directories.
- Review the final diff in Plannotator. Leave the result uncommitted and do not push.

The UI is an upstream example, not a redesign. Preserve its content and code.
Report any upstream limitations separately rather than changing the reference.
