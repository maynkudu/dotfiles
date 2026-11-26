import { loadDotfilesRules } from "./dotfiles-rules-loader.ts";

type TextPart = { type: string; text?: string };
type RuleContext = {
  system: { type: "text"; text: string }[];
  messages: { role: string; content: TextPart[] }[];
};
type RulePluginContext = {
  session: { hook(name: "context", handler: (event: RuleContext) => Promise<void>): Promise<unknown> };
};

/** Refresh dotfiles rules for OpenCode 2, retaining the OpenCode 1 plugin entry. */
export default {
  id: "dotfiles-rules",

  async setup(ctx: RulePluginContext) {
    await ctx.session.hook("context", async (event) => {
      const user = event.messages.findLast((message) => message.role === "user");
      const prompt = user?.content.flatMap((part) =>
        part.type === "text" && typeof part.text === "string" ? [part.text] : [],
      ).join("\n") ?? "";
      const rules = loadDotfilesRules("opencode", prompt);
      if (rules) event.system.push({ type: "text", text: rules });
    });
  },

  async server() {
    return {
      "experimental.chat.system.transform": async (_input: unknown, output: { system: string[] }) => {
        output.system.push(loadDotfilesRules("opencode"));
      },
    };
  },
};
