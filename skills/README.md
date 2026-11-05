# Agent rules and skills

Shared behavior for maynkudu's Codex and Claude Code setup, adapted from Aryan's
original rules. Writing taste, source fidelity, and real verification remain;
the biography, private-library assumptions, and historical agent roles do not.

## Daily use

Edit `rules/`, run `bin/build`, inspect the generated diff, then run `bin/install`.
`bin/install --dry-run` previews changes. Active targets come from `../setup.toml`;
`--agents codex claude` overrides them for one install. Existing files are backed up
and repeated installation is a no-op. Each Claude rule has its own symlink, so
unrelated local rules remain visible.

`bin/check --repo-only` validates a fresh checkout. `bin/check` also verifies the
selected agents and installed skills. Neither check installs anything. Build output
for Pi, Grok, and OpenCode remains available, but they are not default install targets.

## Skills

`../bin/setup --skills` installs the current public selection from
`sources.lock.json` through Codex's bundled skill-installer helper. Sources are pinned
to commits. Existing skills are retained. Local skills and the Cloudflare skills
under `../pi/skills` are linked into `~/.agents/skills`; Claude sees the same collection
through per-skill links. Codex discovers the shared directory.

`manifest.toml` is the historical inventory, including unavailable private skills.
It is not the installer input. The lock file records missing upstream names.
`router-design` retains the private catalog as optional leads and checks availability;
its entries are not claims that those skills are installed.

The bundled `animation-fundamentals` recipes and `aryan-voice` examples work without
access to the original private design collection. Historical prompt audits in
`profile/` describe the original author, not maynkudu.

The pstack collection is pinned to `cursor/plugins` 0.15.36. `bro` and `teach`
keep their existing sources, and pstack's colliding `tdd` skill installs as
`pstack-tdd`. Agent Browser and Agent Desktop are pinned as separate public skills.

The nine tstack PR and review skills are pinned to `1085050`. `council` and
`sol-loop` need additional model support when invoked; installation does not
configure it. Executable helpers declared in `sources.lock.json` have their
permissions restored after installation, including `babysit-pr/scripts/pr-wait`.

## Patches and budgets

`bin/patch --skill-home ~/.agents/skills` reapplies declared upstream skill patches.
The setup runs this after installing skills. The explicit directory keeps the operation
scoped. Review deletion declarations in `vendored/` before applying them to an
existing collection. Missing skills are skipped, not fetched by the patcher.

Codex's generated file has a 24,576-character budget, with long verification and
writing procedures in `reference/`. Grok retains its 10,000-character cap. The build
validates all outputs before writing any file.

See [how it works](docs/how-it-works.md) and [machine setup](../docs/setup.md).
