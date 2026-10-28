# BLANK access verification

Checked on 2026-10-28 using the user-provided `kiys` file. Credential values are
not included in this record.

| Check | Result |
| --- | --- |
| Inspiration passphrase | Opened the normal inspiration directory and its search control |
| Registry token in the browser | Unlocked `cell-portrait.tsx` on the component page |
| Installed helper catalog command | `blank catalog` returned 368 authenticated registry items |
| Installed helper source command | `blank source cell-portrait` returned one source file containing 24,337 characters |
| Installed helper search command | `blank search 'scroll animation'` returned registry picks |
| Fresh-session login | `blank inspiration --session dotfiles-blank-verify` opened and unlocked a new browser session; the heading and search control were present |
| shadcn installation | Version 4.23.0 installed under the user's local npm prefix |
| Project configuration | `blank configure` preserved unrelated values, wrote an environment-variable placeholder, and made no changes on its second run |
| Official CLI authentication | `blank shadcn view @compronents/cell-portrait --cwd <temporary-project>` returned the item and its source file |
| Credential files in the project fixture | No `.env` file was created |
| Credential source | `kiys` is Git-ignored and has mode `600` |
| Helper installation | `~/.local/bin/blank` resolves to this checkout's `bin/blank` |
| Skill installation | Both shared and Claude `blank-direction` links resolve to the bundled skill |
| Agent rules | The rebuilt Codex profile matches its installed copy and contains 24,017 characters under its 24,576-character cap |
| Unit tests | Eight passed, including four BLANK checks for credential transport, file permissions, configuration preservation, and conflicting namespaces |
| Setup health | `python3 bin/doctor` passed, including installed rules, skills, commands, and native dependencies |

The temporary project was removed after checking registry resolution. This check
did not exercise a rendered component inside a user application.

The initial Python HTTP requests received Cloudflare error 1010 because the site
blocked that client's browser signature. That was not a token-validation result.
The site's normal browser form and curl authenticated successfully. The installed
helper uses those paths and does not retry the blocked client.

The public recommendation endpoint can still report unavailable reranking.
The original separate 129-skill design pack and historical BLANK MCP servers
remain outside this integration.

Source and usage are documented in [BLANK access](../../docs/blank.md),
the [helper](../../bin/blank), and the
[shared skill](../../skills/skills/blank-direction/SKILL.md).
