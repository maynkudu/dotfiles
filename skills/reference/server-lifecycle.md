# Managed development servers

Use `agent-server` for development servers started by agents. It inventories current Portless routes and listeners, reuses the same verified app, and supervises newly created app processes. Cleanup is restricted to tracked resources. Older unknown servers stay untouched.

## Before launch

Read `portless.md`. Check current resources before creating another server:

```bash
agent-server inventory
```

The report includes named URLs, current listeners, process identities and RSS without command lines or environment values. A route alias, large memory reading or missing listener is not permission to kill a process. Inspect unknown servers with the user.

Choose the exact app directory within the git worktree. Existing `portless.json` or `package.json` names win; select and name one monorepo package, not every workspace. Portless owns internal port assignment and linked-worktree naming. This helper requires an already running loopback Portless proxy and leaves proxy settings unchanged.

## Start or reuse

Use the actual session ID and a stable ancestor PID, normally the current harness process. Never use a short-lived tool shell, a random PID or the common T3 application process merely to keep resources alive. Pi receives these values through the workflow extension's startup message. Codex and Claude need their real host/session values passed explicitly.

```bash
agent-server --worktree "$WORKTREE" --session "$SESSION" --owner-pid "$HARNESS_PID" \
  start --app-dir "$APP" -- pnpm dev
```

A lock covers acquisition through listener readiness. Repeated starts for the same exact app/worktree and command reuse the running server and add an owner. Conflicting commands, foreign worktrees and occupied unknown aliases fail without replacing the route. An existing verified untracked process can be reused, but never becomes cleanup-owned.

The command returns the actual named URL. Announce that URL using the existing Portless format. A live socket proves transport readiness only. Operate the app and verify its behavior separately. App stdout/stderr is discarded by the supervisor; use project-specific logs or browser evidence for diagnostics, without adding secrets to the registry.

## Finish the work

Release server ownership when the authorized task and its checks are complete. Do this before the final closeout, not merely when an assistant tool turn finishes. Retain a preview only when the user asks or it is still needed for review; report retained servers with their URLs.

```bash
agent-server --worktree "$WORKTREE" --session "$SESSION" --owner-pid "$HARNESS_PID" finalize
```

`release --app-dir "$APP"` releases one app. `release --keep` or `finalize --keep` explicitly preserves a preview. A current owner can `unkeep --app-dir "$APP"` before finalizing later. Other active owners and user-kept resources remain live.

The last owner of a managed app triggers graceful shutdown, then identity-verified cleanup of surviving children. A dedicated Linux subreaper adopts detached descendants. PID, start time, boot ID, UID and pidfd checks protect unrelated or reused PIDs. No process-name kill, global proxy stop or blanket Portless clean runs.

## Interrupted sessions

The supervisor notices verified owner-process death and releases that owner. `recover` operates only on records for the selected exact worktree and uses recorded process starts. It does not infer completion from age, idle time or a normal assistant response.

Pi's genuine session shutdown event finalizes tracked ownership, except reload which preserves it. Codex and Claude have no verified thread-completion hook here, so agents must explicitly finalize at task closeout. A long-lived host process can outlive an individual thread; owner-death cleanup alone does not solve that case. These limits are reported, not hidden behind a Stop hook that would kill active previews after every answer.

## Limits

Initial process supervision is Linux-only and needs `/proc`, pidfd and subreaper support. Unsupported hosts fail before mutations. Saved status needs current validation. Registry limits are 128 servers, 64 owners per server and 512 descendants. Malformed state, incomplete process reads and changed route ownership protect processes and require inspection. This cannot clean up historical untracked servers automatically or guarantee lower memory use for unrelated browser/editor processes.
