# maynkudu's dotfiles

My Arch Linux development setup for websites, apps, and documents. Forked from
[kiritocode1/dotfiles](https://github.com/kiritocode1/dotfiles), keeping Aryan's
writing and design taste while adapting the tools and profile for my own use.

Codex is the primary agent; Claude Code is the second. Existing Bash configuration
is preserved and extended. Zsh gets the same aliases plus completion, suggestions,
and syntax highlighting. The login shell is not changed.

## Setup

```bash
git clone git@github.com:maynkudu/dotfiles.git ~/dotfiles
cd ~/dotfiles
python3 skills/bin/build
python3 bin/setup --dry-run
python3 bin/setup
python3 bin/doctor
```

Setup expects Python 3.11+, Node 24+, npm, Cargo, Git, uv, and the selected agents.
The current machine already has these, plus pnpm, Bun, Starship, Zoxide, Chromium,
FFmpeg, Agent Browser, Agent Desktop, Portless, and Plannotator. See [setup notes](docs/setup.md)
for system prerequisites, verification, backups, and optional integrations.

Choose agents and CLI packages in [setup.toml](setup.toml). Run only selected phases:

```bash
python3 bin/setup --tools --skills
python3 bin/setup --rules --shell
python3 bin/setup --mcp
```

The installer reuses existing tools, installs missing npm tools under `~/.local`,
and backs up configuration before replacing it. It never configures accounts or
changes the existing model/provider selection. Skills become available on the
next turn; start a new agent session to reload global rules and MCP integrations.

BLANK registry and inspiration access use the `blank` command and shared
`blank-direction` skill. See [BLANK access](docs/blank.md) for credential handling,
source inspection, project configuration, and browser login.

## What lives here

| Path | Purpose |
| --- | --- |
| `setup.toml`, `bin/setup`, `bin/doctor` | Selected tools, installation, health checks |
| `skills/rules/` | Source for shared agent behavior and personal preferences |
| `skills/reference/` | Detailed procedures loaded when needed |
| `skills/build/` | Generated rules; edit the sources instead |
| `skills/skills/` | Bundled motion, writing, and workflow skills |
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

## Verify a checkout

```bash
python3 skills/bin/check --repo-only
python3 -m unittest discover -s tests -v
bash -n shell/common.sh shell/bash.sh pi/restore.sh
zsh -n zshrc
```
