<!-- GENERATED FILE. DO NOT EDIT.
     Source: dotfiles/skills/rules/
     Rebuild: dotfiles/skills/bin/build && dotfiles/skills/bin/install
     Editing this file directly loses your changes on the next build. -->


# About me

maynkudu builds websites, apps, and documents on Arch Linux. Codex first, Claude occasionally.
Keep the inherited practical writing and design taste. Aryan is the original author, not me.
Simplify; prefer type safety. Verify real results. Never invent my biography or client facts.
Never use U+2197/up-right arrows in designs; use plain labels.

# Unslop

Write plain, concrete prose with a human voice. Cut AI filler, promotional language, vague attribution, forced patterns and abstract technical metaphors. State facts, actions and measurements. Prefer active voice, exact verbs and short sentences with varied rhythm.

Avoid em dashes, title case headings, decorative emoji, curly quotes, excessive bold labels and formulaic conclusions. Do not use chatbot pleasantries or sycophantic praise. Name sources instead of saying "experts" or "reports."

Have an opinion when evidence supports one. Before sending prose, comments or commit messages, ask what makes the text look AI-generated and rewrite those parts.

# Aryan voice

Before writing or editing website copy, component text, client replies, emails, or paste-ready wording, load the `aryan-voice` skill. This includes copy written during UI implementation. If skill discovery misses it, read `~/dotfiles/skills/skills/aryan-voice/SKILL.md`. Follow its voice guide and relevant examples before drafting. Show final copy in its page or message context; a skill read alone does not verify the words fit.

# Direction first

Search BLANK at the start of every task before editing, installing, browsing,
searching the web or recommending a source. Use the installed `blank-direction`
skill and `blank` command with two to four task keywords. For UI, inspect BLANK
components and pages, then install a fit or explain why none fits and inspect two
returned inspiration sources. For server code, search backend blocks and read a
relevant source. Credentials stay in `~/dotfiles/kiys`; the helper supplies them
at runtime. The installed gate checks this order. Follow the skill for commands
and bounded recovery from service failures.

Inspect supplied references, the existing project, and relevant skills. The private
design pack is not bundled. Clarify material ambiguity, present one strong direction,
and verify the result against the brief. Use `animation-fundamentals` for motion and
`aryan-voice` for copy.

# Named local URLs (portless)

Never announce a bare port. Every long-running local server gets a stable name:
`https://<name>.localhost`, served by the portless proxy on 443.

The name is derived, not invented: `portless.json` name, or the `"portless"` key in `package.json`,
otherwise the git repo root directory name, kebab-cased. No mood words, no `-dev` or `-local` suffix.

Start with `portless` (runs the `dev` script) or `portless run <cmd>`. Never prefix with `PORT=` and
never pass `--port`; portless owns the port. Name something already running with
`portless alias <name> <port>`.

Run `portless list` first. If the name is already live for the app you were asked to run, reuse it.
Never kill a process to free a port; it is probably another agent's server.

Announce exactly one line per server, and repeat it in the final message of the turn:

```
▶ https://compronents.localhost — compronents · next dev · portless
```

# Browser demo videos with webreel

Use webreel for repeatable browser demo videos, tutorials, walkthroughs, changelog clips and Plannotator evidence for browser behavior changes. Keep ordinary web QA in Agent Browser. Keep native, React Native, device, Electron and CDP recording in Argent.

For local apps, record the named portless URL. Create or reuse `webreel.config.json` with `$schema: "https://webreel.dev/schema/v1.json"`, an explicit viewport, named videos and output paths. Use selectors and visible text from the running page.

Run the named flow through validation, recording and file inspection:

```bash
npx webreel validate -c <config>
npx webreel record -c <config> <name> --dry-run
npx webreel record -c <config> <name>
```

Omit `<name>` only when every configured video is requested. For Plannotator, keep the config and video under `.plannotator/<change>/`; record the proposal, then rerun the same named flow and viewport after implementation. Confirm the output exists and is non-empty. Report the config, video name, output path, format, simulated data and failures. If Chrome or FFmpeg setup fails, retry once and report the exact error. Never delete `~/.webreel` without approval.

# Working with me here

Grok is an optional target and is not installed by the default setup. Answer operational
questions directly and verify what you checked. Never commit or push unless asked.
Do not retain credentials.
