# Portable workflow hosts

## Skill compatibility

`agent-workflow-check` validates this workflow's local skills, commands, references and installed links. It checks host-only executable substitutions and the additive adapter patches for legacy `recall` and `reflect` copies. It does not claim every upstream skill has been made portable.

```bash
agent-workflow-check --repo-only
agent-workflow-check
python3 ~/dotfiles/bin/doctor
```

Repair source skills or declared vendored patches, then run setup. Never edit generated agent rules or installed skill copies as the source of truth. Unknown capabilities remain explicit. New skill bodies should use available host tools and named local helpers rather than Cursor-specific transcript paths, model names or Task APIs.

## Session identity

Checkpoint recall selects an explicit source session. This lets a recipient use the same bound source record across Codex, Claude and Pi without scanning their transcript collections. Inspect linked repo state before trusting a saved observation.

Server ownership uses the current session and a stable current ancestor process. Pi's extension exposes its actual session ID and process PID. Other hosts must supply their own actual session values, or use an explicit ID for the current task and an actual harness ancestor. Never use another thread's session or a common application PID in place of thread ownership.

## Lifecycle events

Startup checks read bounded known configuration and reference files. They issue a warning and let the session start. They never inspect transcripts, run a process inventory, start MCPs, invoke models or stop servers.

Pi runs these checks on `session_start`. Its `session_shutdown` finalizes owned servers on quit, new, resume and fork. Reload preserves ownership. No `turn_end`, `agent_end` or idle event triggers cleanup. The explicit `/workflow-finalize` command can release resources when a task is done while the session remains open.

Codex and Claude get bounded SessionStart health hooks. Their thread-end lifecycle is not verified here; the shared rule requires an explicit `agent-server finalize` at task closeout. Verified owner death is a second cleanup path. This avoids confusing an assistant answer or a temporary review pause with completion.
