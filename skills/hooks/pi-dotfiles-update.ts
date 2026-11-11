import { realpathSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const CHECKER = join(dirname(realpathSync(fileURLToPath(import.meta.url))), "../../bin/dotfiles-update");

/** Show available dotfiles updates before the first request in a Pi session. */
export default function (pi: ExtensionAPI) {
  pi.on("session_start", async () => {
    try {
      const result = await pi.exec("python3", [CHECKER, "--startup"], { timeout: 35_000 });
      const message = result.stdout.trim();
      if (message) {
        pi.sendMessage({ customType: "dotfiles-update", content: message, display: true }, { triggerTurn: false });
      }
    } catch {
      // An unavailable checker must let the session start.
    }
  });
}
