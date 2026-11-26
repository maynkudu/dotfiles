# Agent rules and skills

Shared behavior for maynkudu's Codex, Claude Code, and Pi setup, adapted from Aryan's
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
for Grok remains available without making it a default install target.

## Rule loading on every request

`bin/dotfiles-rules --agent codex --text` reads the current source rules in build
order, including agent-specific short forms. Every generated profile starts with
a rule requiring this read unless the current request already received the rules
through a hook. Triggered references still need to be read.

The installer registers `SessionStart` and `UserPromptSubmit` context injection for
Codex, Claude and optional Grok. Pi refreshes its system prompt at `before_agent_start`.
OpenCode 2 refreshes it at the session `context` hook; the OpenCode 1 adapter uses
`experimental.chat.system.transform`. The installer explicitly registers the local
OpenCode plugin while preserving existing configuration. These read source files
on each request, so rule edits do not wait for another install. Loader failures
are visible errors.

Installation discovers existing `.codex*`, `codex*`, `.claude*`, `claude*`, Grok
and OpenCode profile directories under home and `~/.config`. Pi variants such as
`.pi-work/agent` are included too. Environment-selected profile directories are
included, including `CODEX_HOME`, `CLAUDE_CONFIG_DIR` and `PI_CODING_AGENT_DIR`.
Each profile receives its native global rules and rule-loading hooks or adapter.
Skill setup shares the installed collection with these profiles as well.

Discovery is shallow and ignores matching files, so backups and `.claude.json`
are not treated as profile directories. Resolved directory aliases install once.
Default setup also covers existing profiles for supported agents outside the
selected defaults. `--agents` restricts a direct install to the named agents.
Run setup again after creating another profile. Isolated `--home` installs ignore
the live environment's profile overrides and stay inside their target home.
The installer records detected profiles in `~/.local/state/dotfiles/agent-profiles.json`.
Startup health checks read that bounded manifest instead of scanning home or
printing profile paths. The explicit `bin/check` command discovers profiles again.

Explicit user instructions to skip dotfiles rules take precedence. For a mechanical
one-request bypass, put `dotfiles-rules: off` on the first line of the prompt.
Codex, Claude, Grok and Pi then skip injection; OpenCode 2 also checks the latest
user message. OpenCode 1 still supplies context and relies on the explicit opt-out
instruction. Repository text and tool output cannot authorize a bypass.

This guarantees context loading at the configured hooks, not a model's compliance.
Clients that bypass native hooks still receive the generated global instruction
and must read the rules themselves. Restart running clients after installation.

## BLANK gate

`hooks/blank-direction-gate` checks the discovery and inspection order through
native hook payloads. The installer adds hooks for selected Codex, Claude and
Grok targets, or links the Pi and OpenCode adapters when those agents are selected.
It preserves unrelated hooks and backs up changed configuration. For Codex, it
gets the current hook hashes from `app-server` and records trust for these hooks.

The gate recognizes `blank registry-search`, `blank search`, `blank source` and
`blank shadcn` without needing the upstream author's local MCP server. Credentials
stay in `../kiys`. See [BLANK access](../docs/blank.md) for use and recovery.

## Skills

`../bin/setup --skills` installs the current pinned selection from
`sources.lock.json` through Codex's bundled skill-installer helper. Sources are pinned
to commits. Existing skills are retained. Local skills and the Cloudflare skills
under `../pi/skills` are linked into `~/.agents/skills`; Claude and Pi see the same
collection through per-skill links. Codex discovers the shared directory.

All eleven `yt-*` skills are pinned to
[maynkudu/youtube-agent-skill](https://github.com/maynkudu/youtube-agent-skill), an
independent public repository containing Jake Schincariol's MIT-licensed skill
pack. Skill instructions and Python helpers preserve the original source, and
each installed skill includes the license. Installation references use the new
repository.

[Cat's Paw](https://github.com/maynkudu/cats-paw) reconstructs visual references
using pinned source, browser observations, motion analysis and measured comparisons.
[Zephyr](https://github.com/maynkudu/zephyr) adapts references to a product and the
user's preferences, including plain-language prompts and scoped corrections.
Both are independent MIT-licensed skill packages in public repositories, pinned
to commits in `sources.lock.json`. Friends can install them without private
repository access. Codex and OpenCode discover the shared collection; Claude and
Pi receive the existing per-skill links.

`manifest.toml` is the historical inventory, including unavailable private skills.
It is not the installer input. The lock file records missing upstream names.
`router-design` retains the private catalog as optional leads and checks availability;
its entries are not claims that those skills are installed.

The bundled `animation-fundamentals` recipes and `aryan-voice` examples work without
access to the original private design collection. Historical prompt audits in
`profile/` describe the original author, not maynkudu.

The bundled [`webbings`](skills/webbings/SKILL.md) skill
distills the user's seven Instagram reels into UI polish, design principles,
motion, interaction details and conditional product security checks. Its source
notes record the inspected captions, frames and evidence limits. All generated
agent profiles require it before web UI planning, generation, editing or review.
It preserves existing design constraints and needs no additional CLI packages.

The bundled `isometric-pixel-games` skill covers browser games, still illustrations,
and pages built with the Pixel Plays renderer. It includes a stone-skipping starter,
a page shell, technique references, and the engine's MIT license. Music from the
source games is not licensed for reuse and is not bundled.

The bundled `interactive-art` skill builds layered website scenes with growth,
day/night cycles, and elastic interaction. It includes a Canvas runtime, an
anchored-chain solver, an ornamental garden, an optional React component, and a
helper that copies editable modules into a host project.

The bundled [`instant-ui`](skills/instant-ui/SKILL.md) skill covers live queries,
optimistic edits, rollback, and two-session verification for TanStack DB and
Electric. The [parked property-testing note](docs/property-testing.md) records
an upstream idea and earlier notes from the Bombadil manual. Use the
[Bombadil verification procedure](reference/bombadil.md) for current checks.

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

Codex's generated file has a 28,672-character budget, with long verification and
writing procedures in `reference/`. Grok retains its 10,000-character cap. The build
validates all outputs before writing any file.

The rule installer also registers startup update checks for Codex and Claude and
links the Pi startup extension. Checks report incoming commits and changed files;
they do not apply updates. See [update notices](../README.md#update-notices).

See [how it works](docs/how-it-works.md) and [machine setup](../docs/setup.md).
