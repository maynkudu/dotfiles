# About me

I use the handle maynkudu and build websites, apps, and documents on Arch Linux.
Codex is my primary agent; I also use Claude Code.

This setup is adapted from Aryan's dotfiles. I chose to keep his writing and design
taste, practical communication, and preference for simple, well-verified work.
His biography, clients, private resources, and historical prompt statistics are
not facts about me. Do not sign messages as Aryan or invent personal details.

I wanted to share some of my preferences here so we can be more aligned as we work together.

## Coding preferences

- Keep things simple. Channel "yagni" energy unless told otherwise.
- Typesafety is useful, take advantage of it.
- Don't be scared to propose bold ideas if they can meaningfully benefit our work.
- Be careful with destructive actions that are not explicitly requested by the user.
- Tests are good! Endless smoke tests, "regression tests" for feature deletions, etc, much less good.
  Tests should be focused, not slop.
- Comments are a great way to clarify functionality and how code is used. Don't comment every line,
  but feel free to describe (concisely) how functions are used above function definitions, classes,
  etc.
- Keep comments up to date! When making changes, it's important to keep things in sync.

## Coding preferences (TypeScript focused)

- `any` is the enemy. Inferred types are our friend. Our systems should adapt to changes, instead of
  requiring changes everywhere.
- If your TS code looks like a Python dev wrote it, it is bad TS code.
- Avoid one-line functions that are just casting wrappers.
- Write TypeScript in ways that Matt Pocock and Theo would be proud of.
- If not already specified in project, I generally like to use the following tech: Convex, Tailwind,
  React, Vite, pnpm.
- When building more complex web and react native apps, I like to pull in Zustand, React Query,
  Tanstack Start, Clerk (or better-auth if selfhosting), and ArkType (or zod if perf isn't an issue).

I really respect good Effect code, specifically useful when mixed with patterns from
https://www.effect.website/ and https://www.effect.solutions/.

## Design preferences

- Use [Rune Icons](https://www.runeicons.com/) as the default icon library when building apps.
  Prefer it to Lucide and other icon libraries. Keep an existing project's icon system for narrow
  changes unless I ask for a migration.
- Never use the northeast/up-right arrow, U+2197, anywhere in my design work. This includes
  buttons, links, cards, CTAs, external-link indicators and decorative graphics, across all projects.
  Do not recreate the same shape with SVGs, icon libraries, CSS, images or rotated arrows.
  Use plain labels instead, even when a reference design uses this arrow.

## Agent workflow preferences

Operate the real product and verify the result. Keep checks focused on the change.
For substantial app verification infrastructure, read
`~/dotfiles/skills/reference/verification-infrastructure.md`: it covers reproducible
setup, app-specific control CLIs, feature maps, runtime evidence, and performance
measurement. These are tools for the task, not mandatory scaffolding for every edit.

## Questions are read-only

- A question is a request for an answer, not for changes. If the message opens with "how hard would
  it be", "what are your thoughts", "why does", "should we", "is it possible", "can X do Y", or
  otherwise asks rather than instructs: answer it, and do not edit files.
- If the answer is obvious and the change is trivial, still answer first and offer the change. Ask
  before making it.

## Match ceremony to the task

- Do not spawn subagents or a multi-agent panel for work a single agent finishes in one pass.
  Delegation is for breadth or adversarial review, not for ordinary tasks.
- When several agents do work in parallel, state file ownership up front so they do not collide.
