import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { loadDotfilesRules } from "./dotfiles-rules-loader.ts";

/** Refresh dotfiles rules before each Pi run, including resumed sessions. */
export default function (pi: ExtensionAPI) {
  pi.on("before_agent_start", async (event) => {
    const prompt = event.messageType === "user" ? event.prompt : "";
    const rules = loadDotfilesRules("pi", prompt);
    if (rules) return { systemPrompt: event.systemPrompt + "\n\n" + rules };
  });
}
