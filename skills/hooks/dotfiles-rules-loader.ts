import { execFileSync } from "node:child_process";
import { realpathSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const READER = join(dirname(realpathSync(fileURLToPath(import.meta.url))), "../bin/dotfiles-rules");

/** Read dotfiles rules anew for each request, with the current user's opt-out. */
export function loadDotfilesRules(agent: "pi" | "opencode", prompt = ""): string {
  return execFileSync("python3", [READER, "--agent", agent, "--hook", "--text"], {
    input: JSON.stringify({ prompt }),
    encoding: "utf8",
    timeout: 5000,
    maxBuffer: 1024 * 1024,
  });
}
