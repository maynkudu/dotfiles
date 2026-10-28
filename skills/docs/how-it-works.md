# How the setup works

`setup.toml` selects agents, missing CLI tools, and bundled skills. The public skill
lock file selects upstream paths and exact source commits. The installer reads these
files; it does not reconstruct the original author's machine from historical audits.

## Rules

`rules/tiers.toml` chooses rules for each supported agent. `bin/build` renders them
into `build/`. Claude gets separate Markdown files. Other agents get an `AGENTS.md`.
`bin/install` installs only the selected agents, Codex and Claude by default.

Global defaults live in `~/.codex/AGENTS.md` and `~/.claude/rules/`. The next agent
session reads them. Editing generated files or live copies loses changes at the next
build, so edit sources and rebuild. Detailed writing and verification procedures
are linked from short rules to keep the always-loaded guidance compact.

## Skills

`../bin/setup --skills`, run from this directory's parent, installs public skills
through the bundled Codex skill installer. Existing copies are retained. New skills
live in `~/.agents/skills`, where Codex discovers them. Claude receives individual
symlinks into the same collection. Bundled skills are symlinks into this repository.

The original private 129-skill design pack is not included. Its catalog is retained
for reference. The self-contained motion recipes and writing examples are available.
Upstream skill names that no longer exist are recorded in `sources.lock.json`.

## Machine tools

From the repository root, `python3 bin/setup` installs missing CLI tools, document
libraries, skills, agent rules, shell includes, and Argent and Agentation MCP registration. Use
phase flags to repeat only the needed work. `--dry-run` prints proposed actions.
The setup retains the login shell and existing provider settings, and backs up
configuration files before changing them.

`python3 bin/doctor` checks tools and installed rules and skills.
`python3 skills/bin/check --repo-only` works before installation.
