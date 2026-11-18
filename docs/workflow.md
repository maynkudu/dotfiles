# Workflow commands

The shared setup now includes local commands for private handoffs, server ownership and workflow contract checks. These are used by Codex, Claude and Pi without another agent framework or an automatic learning service.

## Commands

| Command | Purpose |
| --- | --- |
| `dotfiles-cli COMMAND ...` | Run a selected CLI with the recorded Node runtime without changing app PATH |
| `dotfiles-health` | Check known runtime/configuration files and distinguish missing, failed and unknown checks |
| `agent-workflow-check` | Check local workflow skills, references, links and startup integration |
| `agent-checkpoint` | Save/search necessary private context for an explicit source session and exact worktree |
| `agent-server` | Inventory routes/listeners, reuse and supervise one app, release current ownership |
| `agent-workflow-eval` | Run deterministic sanitized workflow contract fixtures |

Install with the normal `python3 bin/setup --tools --skills --rules` flow. Review `--dry-run` first. Public skills remain pinned; local skills and commands link to this checkout. Existing unrelated commands, providers and hooks are preserved.

## Handoffs

Use `private-checkpoint` before an agent switch or compaction with unfinished work, then `context-recall` to resume. Select the exact source session, link existing plans and evidence, and recheck their current state. Stored observations remain private and unreviewed, never permission or policy. See [private checkpoints](../skills/reference/private-checkpoints.md).

`reviewed-reflection` proposes durable lessons from current work. It does not launch fixed model panels or change standing rules without approval. Legacy `recall` and `reflect` retain their upstream bodies with a declared additive adapter directing this setup to the local procedures.

## Servers

Run `agent-server inventory` before creating a server. Start a single app with an actual session and stable harness PID. The helper keeps Portless's assigned ports/names, locks duplicate launches, verifies a listener and records ownership. Finalize at task closeout. Other active owners and explicitly kept previews survive. Older untracked servers are never killed automatically.

Pi's real session shutdown finalizes ownership except reload. Codex and Claude require explicit task finalization because no thread-completion event is verified here. Owner-process death provides a second cleanup path. This is Linux process supervision, not a global process cleaner. See [server lifecycle](../skills/reference/server-lifecycle.md).

## Commits and verification

When committing is authorized, group each coherent feature or fix with its tests and docs. Stage scoped files/hunks and inspect/check the staged group. Do not combine unrelated completed work into one catch-all commit. A requested review still happens before commit and push.

Run `agent-workflow-eval`, `agent-workflow-check --repo-only` and the focused Python tests after workflow changes. Fixture success establishes checker contracts, not model reliability or performance. Live checks and their limits must be reported separately.

Compatibility procedures and lifecycle limits are in [host support](../skills/reference/workflow-hosts.md). The new workflow checks do not certify every third-party skill or custom MCP server.
