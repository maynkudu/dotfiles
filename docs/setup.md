# Arch Linux setup

This fork configures Codex, Claude Code, and Pi for maynkudu. It keeps Aryan's writing
and design preferences, with maynkudu's identity and Linux paths. It installs the
public tools and skills used by the rules.

## Before installing

Make these commands available first:

| Commands | Used for |
| --- | --- |
| `python3` 3.11+, `git`, `uv` | Configuration, skills, and the document environment |
| `node` 24+, `npm`, `cargo`, `make`, `g++` | CLI tools and their native dependencies |
| `codex`, `claude`, `pi` | The selected agents; Codex and Claude also receive MCP registration |
| `bash`, `zsh` | Shell configuration |
| `pnpm`, `bun`, `starship`, `zoxide`, `rg`, `fd`, `bat`, `eza` | Development commands and shell integrations |
| `chromium`, `ffmpeg`, `pdftoppm`, `plannotator` | Browser checks, recordings, PDF previews, and reviews |
| `at-spi2-core` | Native Linux desktop inspection and input through Agent Desktop |

These commands are present on the current machine. Codex must also have its
bundled skill-installer helper under `~/.codex/skills/.system/skill-installer/`.
The setup uses that helper to install public skills pinned to source commits.

LibreOffice renders Word files and slides and recalculates Excel formulas. On a
new machine, install it through Arch's package manager:

```bash
sudo pacman -S --needed libreoffice-fresh
```

LibreOffice 26.8.1.1 is installed and verified on this machine.

The installer does not run system package upgrades, change the login shell, or
configure accounts and model providers.

## Install or update

Run from the repository root:

```bash
python3 skills/bin/build
python3 bin/setup --dry-run
python3 bin/setup
python3 bin/doctor
```

Start a new agent session after installation to load the rules and MCP
processes. Open a new shell to load the shared aliases and integrations.

Choose agents and npm packages in [`setup.toml`](../setup.toml). The default
agents are `codex`, `claude`, and `pi`. Other generated profiles remain in `skills/build/`.

Use phase flags to repeat selected work:

| Command | What it does |
| --- | --- |
| `python3 bin/setup --tools` | Installs missing CLIs, fnm, Zsh plugins, and document libraries; applies the version-specific Webreel fix |
| `python3 bin/setup --skills` | Installs missing public skills and links shared skills for selected agents |
| `python3 bin/setup --rules` | Checks generated rules, then installs the selected profiles |
| `python3 bin/setup --shell` | Updates one managed block in each shell configuration |
| `python3 bin/setup --mcp` | Registers Argent and Agentation where they are missing |

Flags can be combined. `--home <directory>` supports isolated rules, shell, and
skill installations. MCP registration uses the real home and refuses a different
`--home`.

## Files and backups

| Location | Installed content |
| --- | --- |
| `~/.local/bin`, `~/.local/lib/node_modules` | Missing npm tools and the `doc-python`, `blank`, and `usage` launchers |
| `~/.local/share/dotfiles/documents` | Python 3.13 environment with the pinned document libraries |
| `~/.local/share/dotfiles/zsh` | Zsh suggestions and highlighting plugins |
| `~/.agents/skills` | Shared public and bundled skills |
| `~/.claude/skills`, `~/.pi/agent/skills` | Links to the shared skills |
| `~/.codex/AGENTS.md`, `~/.claude/rules`, `~/.pi/agent/AGENTS.md` | Generated agent rules |
| `~/.bashrc`, `~/.zshrc` | A managed include for this checkout |

Existing tools stay with their current package manager. Existing skills are
retained. Configuration replacements get a timestamped
`.before-dotfiles-<timestamp>` backup beside the original. Repeating rule and shell
installation does not create more backups when the content is unchanged.

Keep local shell settings in `~/.bashrc.local` or `~/.zshrc.local`. Keep this
checkout in place because the installed rules and bundled skills link to it.

Interactive shells and agent sessions check for updates before normal startup.
The notice lists incoming commits and changed files and shows the explicit update
commands. It never pulls automatically. Run `dotfiles-update` for a manual check.
Configure `[updates]` in `setup.toml` or set `DOTFILES_UPDATE_CHECK=0` to disable
checks. The default timeout is four seconds; network failure lets startup continue.

## Native dependencies

npm 12 blocks dependency build scripts unless they are allowed. `npm_allow_scripts`
in `setup.toml` names the dependencies needed by Argent, Agentation, and Webreel.
Setup passes that list for its npm installations. It also selects Sharp's bundled
libvips to avoid compiling against a different system copy.

If a previous installation skipped the builds, or Node was upgraded, repair this
setup's native dependencies with:

```bash
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm rebuild --global --prefix "$HOME/.local" \
  --allow-scripts=better-sqlite3,node-pty,tree-sitter,tree-sitter-javascript,tree-sitter-typescript,sharp \
  better-sqlite3 node-pty tree-sitter tree-sitter-javascript tree-sitter-typescript sharp
python3 bin/doctor
```

Restart the agents after rebuilding. An already running process may still hold
the previous module state.

## Browser and annotation tools

Agent Browser works with the installed browser. Agent Desktop uses the current graphical session
and needs `at-spi2-core`; run `agent-desktop skills get platform` for the X11, Wayland, and desktop
environment limits. Webreel downloads its headless browser on first recording.
`FFMPEG_PATH=/usr/bin/ffmpeg` selects the system encoder.

Webreel 0.1.4 starts its browser with manual frame control, but its recorder never
advances those frames. Setup removes that one flag from the locally installed
`@webreel/core` 0.1.4 and backs up the file. Other versions are left alone. Rerun
`python3 bin/setup --tools` after reinstalling that version of Webreel. Keep
recording outputs on the same filesystem as `~/.webreel`; this version moves its
temporary recording with `rename`, which fails across filesystems.

Portless retains the current proxy settings. This machine uses HTTPS on proxy
port 1355 with a certificate trusted by the system. On a new machine, grant
system trust and check the proxy with:

```bash
portless trust
portless doctor
```

`portless trust` requests sudo when needed. A stopped proxy can start when the
next app runs. Inspect `portless list` before starting apps; keep unrelated routes.

Both agents launch Argent and Agentation through their registered MCP commands.
Agentation's HTTP server and MCP process must stay running while annotating.
Mount the toolbar in a project's development build with the same endpoint as its
MCP server. This dotfiles setup does not add a toolbar to existing applications.

## BLANK access

Setup installs shadcn and the `blank` helper, and shares the `blank-direction`
skill with Codex and Claude. The user-supplied registry token and inspiration
passphrase were verified. They remain in the Git-excluded, owner-only `kiys`
file and are read for each authenticated operation. Setup itself does not copy
credentials or authenticate. See [BLANK access](blank.md) for commands and checks.

## Documents

Use the dedicated environment for document scripts:

```bash
doc-python your-document-script.py
anydoc path/to/document.docx
```

The environment includes python-docx, python-pptx, openpyxl, pypdf, ReportLab,
Pillow, and Pandoc through pypandoc. `anydoc` extracts local files. Python imports
and successful exports do not establish the rendered layout; use LibreOffice
and Poppler for that check. Formula recalculation also needs LibreOffice.

## Verification and limits

```bash
python3 skills/bin/check --repo-only
python3 -m unittest discover -s tests -v
bash -n shell/common.sh shell/bash.sh pi/restore.sh
zsh -n zshrc
python3 bin/doctor
```

Doctor checks command availability, document imports, Pandoc, Agentation's SQLite
binding, and the installed rules and skills. It does not start apps or certify
browser annotation sync.

The [verification record](../.plannotator/setup-verification/results.md) contains
the runtime evidence and its limits. Office rendering, spreadsheet formula
recalculation, and Portless HTTPS certificate validation passed on this machine.

The public selection and exact source commits are recorded in
[`skills/sources.lock.json`](../skills/sources.lock.json). Ten old names are
unavailable in their current upstream sources. The original separate
129-skill design pack, legacy macOS Computer Use, and authenticated CPA pool are not
configured. The live BLANK registry and inspiration directory are available
through the new helper. Bundled motion recipes and writing examples remain available.
