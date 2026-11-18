---
name: skill-host-compat
description: Check local skill references, metadata and host-only executable assumptions before adding or sharing skills across Codex, Claude and Pi.
---

# skill host compat

Read [host support](../../reference/workflow-hosts.md). Run agent-workflow-check --repo-only and inspect the changed skill end to end. Verify its required references and actual available tools for each intended host. Legacy recall/reflect use additive local adapters. Do not claim full upstream compatibility from the local workflow checker.
