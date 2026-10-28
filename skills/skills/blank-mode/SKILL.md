---
name: blank-mode
description: Workflow preferences inherited by maynkudu. Read when coordinating a substantial development task, and whenever choosing between the installed skills, principles, or routers. Covers which agent is being used for what, the six failure modes that recur here, and which playbook fits the request.
---

# blank mode

This workflow is adapted from Aryan's dotfiles. Codex is the primary agent and Claude
Code is used occasionally. The user builds websites, apps, and documents on Arch Linux.
The original audit in `profile/how-i-work.md` describes Aryan, not the current user.

## Always on, no matter the playbook

Four rules load on every turn and are not optional: `unslop` (writing), `direction-first` (inspect available sources before choosing), `fidelity-first` (1:1 work), `read-before-edit`. Do not restate
them, follow them.

## The six failure modes

These checks preserve useful lessons from the original setup. Use a named skill
only if installed; the check still applies when it is unavailable.

| What goes wrong | Reach for |
|---|---|
| Built something that is not actually 1:1 | `fidelity-first` rule |
| Edited a file that was only partly read | `read-before-edit` rule |
| Rewrote code that was already correct | `principle-subtract-before-you-add` |
| Said done without running it | `principle-prove-it-works` |
| Stopped at a plan instead of finishing | `principle-outcome-oriented-execution` |
| Lost the thread on long work | `principle-guard-the-context-window` |

## Playbooks

**An image plus a few words.** The picture is the spec; the words point at the part that matters.
Ask which element is meant before changing anything across the
page. Verify with `argent-screenshot-diff` or `agent-browser`, chosen by `ui-verification`.

**"Make it 1:1" or reproduce a linked source.** Follow `fidelity-first` exactly: pin the source into
`reference/`, extract real values, name the mechanism in one sentence, diff. Never eyeball.

**Open design or implementation choice.** Follow `direction-first` for discovery triggers and
bypasses. Research the existing wall, registry and component code; good ideas can come from anywhere.
For vague creative briefs, clarify material choices and audience problems. Develop a strong result
through experiments and comparisons, not a large list for the user to sort.

**Something is broken.** `read-before-edit`, then `principle-fix-root-causes`. Reproduce, trace to the
cause, say the cause in one sentence, then fix only that.

**Build a feature.** The `plannotator` rule owns the planning trigger, exceptions and approval.
Use its on-demand procedure; the representative proof replaces duplicate creative approval steps.

**Ship it.** Never commit or push unless asked.
When asked, carry it to a verified end, not to a plan.

**Agent plumbing.** Skills, rules, MCP, hooks, memory. Read `writing-for-agents` when available before authoring it, and rebuild with `bin/build && bin/install` rather than editing installed files.

## Reaching the rest

`router-process` indexes upstream engineering skills. `router-design` preserves the
original design catalog as optional leads. Check installed skills before using any entry.
The private design pack is not bundled. The motion recipes and writing examples are.

## Style

Short answers. Length is not thoroughness.
Show the mechanism, not the feeling: which value, which file, which line. Expect correction mid-flight
and take it plainly, without re-explaining the previous attempt.
