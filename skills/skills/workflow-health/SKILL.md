---
name: workflow-health
description: Inspect bounded local workflow configuration when agent tooling, managed launchers, hooks or installed skills are missing or inconsistent.
---

# workflow health

Read [host support](../../reference/workflow-hosts.md). Run agent-workflow-check and python3 ~/dotfiles/bin/doctor. Distinguish failed, missing and unknown checks. Follow the actual runtime/registration path before proposing repairs. Preserve provider settings, external binaries and unrelated hooks. Startup warning is not proof that live MCP or app behavior works.
