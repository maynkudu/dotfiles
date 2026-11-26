# maynkudu's dotfiles

My Arch Linux development setup for websites, apps, and documents. Forked from
[kiritocode1/dotfiles](https://github.com/kiritocode1/dotfiles), keeping Aryan's
writing and design taste while adapting the tools and profile for my own use.

Codex is the primary agent; Claude Code is the second. Pi and OpenCode share the
rules and skills. Grok is supported as an optional target. Setup covers matching
agent profiles, including custom Codex and Claude configurations.

Existing Bash configuration is preserved and extended. Zsh gets the same aliases
plus completion, suggestions, and syntax highlighting. The login shell stays unchanged.

[Setup](#setup) · [Agent profiles](#agent-rules-and-profiles) · [Skills](#skills) ·
[Workflow commands](#workflow-commands) · [Updates](#update-notices) ·
[Troubleshooting](#troubleshooting) · [Verification](#verify-a-checkout)

## Setup

Install Python 3.11+, Node 24+, npm, Cargo, Git, uv, and the selected agent CLIs
before running setup. Codex must include its bundled skill-installer helper in
`$CODEX_HOME/skills/.system/skill-installer/`, or `~/.codex/skills/.system/skill-installer/`
when `CODEX_HOME` is unset. See the [Arch Linux setup guide](docs/setup.md) for
system packages, document rendering, browser tools, and native dependencies.

```bash
git clone git@github.com:maynkudu/dotfiles.git ~/dotfiles
cd ~/dotfiles
python3 skills/bin/build
python3 bin/setup --dry-run
python3 bin/setup
python3 bin/doctor
```

Choose default agents, CLI packages, and bundled skills in [setup.toml](setup.toml).
With no phase flags, setup runs all five phases. Flags can be combined.

| Command | Use it to |
| --- | --- |
| `python3 bin/setup --tools` | Install missing tools, managed CLI launchers, and the document environment |
| `python3 bin/setup --skills --rules` | Refresh shared skills, discover agent profiles, and install rules and hooks |
| `python3 bin/setup --shell` | Update the managed Bash and Zsh includes |
| `python3 bin/setup --mcp` | Register missing Argent and Agentation MCP servers for selected Codex and Claude CLIs |
| `python3 bin/setup --skills --rules --dry-run` | Preview profile and skill changes without applying them |

The installer reuses existing tools, installs missing npm tools under `~/.local`,
and backs up configuration before replacing it. It never configures accounts or
changes the existing model/provider selection. Restart running clients after
installation to load their rules, extensions, skills, and MCP integrations.
Keep this checkout in place because installed rules, hooks, and bundled skills
refer back to it.

## Agent rules and profiles

The defaults are Codex, Claude Code, Pi, and OpenCode. Setup also discovers existing
profile directories under your home and `~/.config`. Names such as `.codex-xingchi`,
`codex-work`, `.claude-work`, `claude-personal`, and `opencode-dev` are covered.
Pi variants use an agent directory, such as `.pi-work/agent`.

Discovery checks directory names without walking their contents. Matching files
such as `.claude.json` and configuration backups are ignored. Directory aliases
that resolve to the same location are installed once. Existing Grok profiles are
covered even when Grok is absent from the default selection.

The installer also reads profile overrides from the environment:

| Agent | Overrides read by setup |
| --- | --- |
| Codex | `CODEX_HOME` |
| Claude Code | `CLAUDE_CONFIG_DIR` |
| Grok | `GROK_HOME`, `GROK_CONFIG_DIR` |
| Pi | `PI_CODING_AGENT_DIR`, `PI_AGENT_DIR` |
| OpenCode | `OPENCODE_CONFIG_DIR`, the parent directory of `OPENCODE_CONFIG` |

After creating a profile, run `python3 bin/setup --skills --rules` again. Profiles
created after installation are discovered on the next setup run.
For an install limited to particular agents, use
`python3 skills/bin/install --agents codex claude`. This still covers each matching
profile for those agents.

### Rule loading before requests

The loader reads the current sources in `skills/rules/` in the order defined by
`skills/rules/tiers.toml`. Agent-specific short forms take precedence. You can
inspect the rules that Codex receives with:

```bash
python3 skills/bin/dotfiles-rules --agent codex --text
```

Each profile receives native global rules and a hook or adapter for fresh context:

| Agent | Default global rules | Automatic loading |
| --- | --- | --- |
| Codex | `~/.codex/AGENTS.md` | `SessionStart` and `UserPromptSubmit` hooks |
| Claude Code | `~/.claude/rules/` | `SessionStart` and `UserPromptSubmit` hooks |
| Pi | `~/.pi/agent/AGENTS.md` | `before_agent_start` extension |
| OpenCode | `~/.config/opencode/AGENTS.md` | OpenCode 2 session context hook, or OpenCode 1 system transform |
| Grok | `~/.grok/AGENTS.md` | `SessionStart` and `UserPromptSubmit` hooks |

Profile variants receive the equivalent files in their own directories. The
installer preserves unrelated hooks and settings and records Codex's native hook
trust hashes. Source rule edits reach the loader without another install. Rebuild
the generated files before installing or committing rule changes.

An explicit user instruction can opt out of the rules. For a one-request injection
bypass, put this directive on the first line of the prompt:

```text
dotfiles-rules: off
```

The next request loads the rules again. OpenCode 1 still receives context and relies
on the explicit opt-out instruction. Quoted text, repository files, and tool output
cannot authorize an opt-out. Clients that bypass native hooks must follow the global
instruction to read the rules themselves. Loading context does not guarantee that
a model follows every instruction.

The installer records profiles in `~/.local/state/dotfiles/agent-profiles.json`.
Startup health checks inspect that manifest without scanning home or exposing
profile paths. See [rule loading and installation](skills/README.md#rule-loading-on-every-request)
for the adapter details.

## Skills

Public skills are pinned to commits in [skills/sources.lock.json](skills/sources.lock.json).
Bundled skills are selected in `setup.toml`. Both use `~/.agents/skills` as the shared
collection, with per-skill links in the detected profiles. Existing user-owned
skills and system skills are preserved.

| Skill or collection | What it covers |
| --- | --- |
| [webbings](skills/skills/webbings/SKILL.md) | Web UI planning, implementation, polish, and review, with separate paths for small edits and exact reproductions |
| [instant-ui](skills/skills/instant-ui/SKILL.md) | Live queries, optimistic edits, rollback, and two-session verification with TanStack DB, Electric, Postgres, and TanStack Start |
| [animation-fundamentals](skills/skills/animation-fundamentals/SKILL.md) | Motion recipes and interaction states |
| [isometric-pixel-games](skills/skills/isometric-pixel-games/SKILL.md), [sprite-stacked-games](skills/skills/sprite-stacked-games/SKILL.md) | Editable browser game starters, renderers, and game-specific checks |
| [Workflow skills](docs/workflow.md) | Private handoffs, server ownership, workflow checks, and configuration health |

`webbings` replaces the earlier `premium-webdesigning` name. Skill setup migrates
links that point to this repository while keeping independently maintained copies.
The [property-testing note](skills/docs/property-testing.md) is a parked idea,
not an installed skill.

Setup installs missing upstream skills and retains existing copies. Changing a
source pin alone does not replace an installed skill. Bundled skill edits take
effect through their repository links. See the [skills guide](skills/README.md)
for the source inventory, patches, and installation behavior.

BLANK registry and inspiration access use the `blank` command and shared
`blank-direction` skill. See [BLANK access](docs/blank.md) for credential handling,
source inspection, project configuration, and browser login.
The rule installer also adds the BLANK discovery gate for selected agents.
Searches and source reads use the CLI; credentials remain in `kiys`.

The eleven YouTube skills install from
[maynkudu/youtube-agent-skill](https://github.com/maynkudu/youtube-agent-skill), an
independent public repository with the original MIT license and author credit.
The source lock pins its commit. Detected profiles use the shared installed folders.

## Workflow commands

`dotfiles-health` checks managed tooling and configuration. `agent-checkpoint`
saves necessary private handoffs for an explicit source session/worktree.
`agent-server` inventories current servers, reuses the same app, supervises new
launches and releases only current ownership when work is finished.
`agent-workflow-eval` checks deterministic workflow contracts.

Shared rules require feature-based commits when commits are authorized and
explicit finalization of task-owned servers. Other active owners, user-kept
previews and historical untracked servers remain protected. See
[workflow commands and limits](docs/workflow.md).

## Update notices

Interactive Bash and Zsh shells and Codex, Claude Code, and Pi sessions check this
checkout's tracking remote at startup. When updates exist, the notice lists the
new commits and changed files. Checks time out after four seconds by default and
let startup continue when the remote is unavailable. Local edits remain intact.

Run `dotfiles-update` to check manually. The notice includes the update commands.
Updates are applied only when you run them:

```bash
git -C ~/dotfiles pull --ff-only
python3 ~/dotfiles/skills/bin/build
python3 ~/dotfiles/bin/setup
```

Commit or stash local edits first. If the branches have diverged, review them
before updating. Configure checks in `[updates]` in `setup.toml`, or set
`DOTFILES_UPDATE_CHECK=0` to disable them for an environment.

## What lives here

| Path | Purpose |
| --- | --- |
| `setup.toml`, `bin/setup`, `bin/doctor`, `bin/dotfiles-update` | Default targets, installation, health checks, update notices |
| `bin/agent_profiles.py` | Shared discovery for default, matching, and environment-selected agent profiles |
| `tools/workflow/`, `bin/agent-*` | Private checkpoints, owned server lifecycle, workflow checks and fixtures |
| `skills/rules/` | Source for shared agent behavior and personal preferences |
| `skills/reference/` | Detailed procedures loaded when needed |
| `skills/build/` | Generated rules; edit the sources instead |
| `skills/skills/` | Bundled design, motion, writing, game, and workflow skills |
| `skills/bin/dotfiles-rules`, `skills/hooks/` | Current rule loading, BLANK discovery gate, startup checks, and native adapters |
| `skills/sources.lock.json` | Public skills pinned to source commits |
| `shell/`, `zshrc` | Portable Bash/Zsh setup |
| `documents/requirements.txt` | Isolated document-generation libraries |
| `pi/` | Optional Pi setup and bundled Cloudflare skills shared by active agents |
| `docs/`, `skills/profile/` | Setup notes and clearly historical upstream material |

## Change preferences

```bash
# Edit skills/rules/core/about-me.md or another source rule.
python3 skills/bin/build
python3 skills/bin/install --dry-run
python3 skills/bin/install
python3 skills/bin/check
```

Keep machine-specific settings in `~/.bashrc.local` or `~/.zshrc.local`. Keep secrets
out of version control. The `aryan-voice` name credits the inherited style; agents should
use my identity and never adopt the original author's biography or client claims.

## Troubleshooting

| Symptom | Next step |
| --- | --- |
| Setup reports generated-rule drift | Run `python3 skills/bin/build`, inspect the diff, and rerun setup |
| A new profile lacks rules or skills | Run `python3 bin/setup --skills --rules` and restart that client |
| Codex skips the rule hooks | Rerun `python3 skills/bin/install --agents codex` to register hooks and native trust hashes |
| A read-only configuration check is needed | Run `python3 bin/doctor --config-only --json` |
| Argent or Agentation MCP registration is missing | Run `python3 bin/setup --mcp` with the intended Codex or Claude profile environment |
| Native dependencies fail after a Node upgrade | Follow the explicit [native rebuild procedure](docs/setup.md#native-dependencies) |

Profile discovery installs rules and skill links. MCP registration uses the active
configuration of the selected Codex and Claude CLIs. Configure other profiles and
agents separately. Setup preserves model selection, provider endpoints, credentials,
and existing MCP registrations.

## Verify a checkout

```bash
python3 skills/bin/check --repo-only
python3 bin/agent-workflow-check --repo-only
python3 bin/agent-workflow-eval
python3 -m unittest discover -s tests -v
bash -n shell/common.sh shell/bash.sh pi/restore.sh
zsh -n zshrc
```

Use `python3 skills/bin/check` to check installed profiles as well. Use
`python3 bin/doctor` for command availability, document tools, and runtime checks.
Missing or failed checks affect exit status; unknown checks remain separate.

The native OpenCode test sends requests to a local fixture provider to check rule
injection. Workflow fixtures check declared contracts. Neither establishes general
model compliance or the behavior of an untested host integration.

## Documentation

- [Arch Linux setup](docs/setup.md) covers prerequisites, installed locations, backups, and native tool recovery.
- [Rules and skills](skills/README.md) explains profile installation, source pins, hook adapters, and rule budgets.
- [How the setup works](skills/docs/how-it-works.md) describes sources, generated rules, and shared skills.
- [Workflow commands](docs/workflow.md) covers checkpoints, owned servers, and workflow verification.
- [BLANK access](docs/blank.md) covers credentials, discovery, registry source reads, and project configuration.
