---
name: server-lifecycle
description: Inventory, reuse, supervise and finalize development servers without killing unrelated processes. Use before launching a server and when finished work should release its resources.
---

# server lifecycle

Read [server lifecycle](../../reference/server-lifecycle.md) and [Portless](../../reference/portless.md). Inventory first. Use actual session and stable harness PID, reuse the verified exact app/worktree, supervise new launches and verify the rendered app separately from socket readiness. Finalize only current ownership at task closeout. Preserve shared or explicitly kept resources. Unknown historical servers stay untouched.
