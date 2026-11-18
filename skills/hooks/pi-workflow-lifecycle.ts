import { realpathSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";

const BIN = join(dirname(realpathSync(fileURLToPath(import.meta.url))), "../../bin");

/** Check known configuration and release only this real session's owned resources. */
export default function (pi: ExtensionAPI) {
  const finalize = async (ctx: ExtensionContext, keep = false) => {
    const args = [join(BIN, "agent-server"), "--worktree", ctx.cwd,
      "--session", ctx.sessionManager.getSessionId(), "--owner-pid", String(process.pid),
      "finalize", "--no-wait", ...(keep ? ["--keep"] : [])];
    const result = await pi.exec("python3", args, { timeout: 5_000, maxBuffer: 16_384 });
    if (result.code !== 0 && ctx.hasUI) {
      ctx.ui.notify("Server finalization was not verified. Inspect agent-server status.", "warning");
    }
  };

  pi.on("session_start", async (_event, ctx) => {
    for (const [command, flag] of [["dotfiles-health", "--hook"], ["agent-workflow-check", "--startup"]]) {
      try {
        const result = await pi.exec("python3", [join(BIN, command), flag], { timeout: 5_000, maxBuffer: 16_384 });
        if ((result.code !== 0 || result.stdout.trim() || result.stderr.trim()) && ctx.hasUI) {
          ctx.ui.notify("Workflow configuration needs review. Run dotfiles-health and agent-workflow-check.", "warning");
        }
      } catch {
        if (ctx.hasUI) ctx.ui.notify("Workflow configuration check unavailable.", "warning");
      }
    }
    pi.sendMessage({ customType: "workflow-session", display: false,
      content: `Managed workflow session is ${ctx.sessionManager.getSessionId()}. ` +
        `For agent-server use owner PID ${process.pid} and exact worktree ${ctx.cwd}. ` +
        "Finalize owned resources when the authorized task is complete. Ordinary assistant idle is not thread completion." },
      { triggerTurn: false });
  });

  pi.on("session_shutdown", async (event, ctx) => {
    if (event.reason === "reload") return;
    try { await finalize(ctx); } catch { /* Owner-death recovery remains available. */ }
  });

  pi.registerCommand("workflow-finalize", {
    description: "Release this session's managed servers; pass keep to retain a requested preview",
    handler: async (args, ctx) => {
      if (args.trim() && args.trim() !== "keep") {
        ctx.ui.notify("Usage: /workflow-finalize [keep]", "warning");
        return;
      }
      await finalize(ctx, args.trim() === "keep");
    },
  });
}
