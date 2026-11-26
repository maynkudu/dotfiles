---
name: webbings
description: Plan, build, refine, or review web UI. Use for new pages, redesigns, responsive work, visual polish, and UI reviews; the workflow adapts to review-only, narrow edits, exact reproductions, and open-ended design.
---

# Webbings

Make the page communicate its purpose clearly and make its controls work well.
Choose typography, proportions, color and interaction from the content and the
accepted direction. This skill supplies decisions and checks, not a fixed style.

## Choose the right path

- **Review only:** Assess the supplied screenshot, code or live page without editing.
  Rank concrete issues by impact and evidence, and separate defects from optional
  opportunities. Use [UI polish](references/ui-polish.md) for relevant checks. A
  still image cannot establish keyboard behavior, responsive reflow, semantics or
  interaction states; state what remains unverified.
- **Small or scoped edit:** Preserve the accepted direction and change only the
  requested area. Do not create a design proposal or fresh concept exploration for
  a tiny obvious fix. Keep any always-on project lookup rules, but do not reopen an
  accepted direction. Run focused checks relevant to that change.
- **Exact reproduction:** Follow `fidelity-first` and use the accepted source as
  the specification. Measure and compare; do not invent alternative directions.
- **New page, redesign or substantial feature:** Use the build path below. Skip
  fresh direction research when the user has already approved the direction and
  the work stays within it.

## Preserve the brief

Read the project's design system and the user's current design constraints first.
Keep exact-copy requirements, accepted references and narrow edit scope intact.
For this dotfiles setup, `~/dotfiles/skills/reference/design-craft.md` and
`~/dotfiles/skills/reference/ui-verification.md` own craft and runtime verification.
Use the VPS rules when the target is headless. An unavailable tool is a named
verification gap, not a reason to install an unrelated workstation stack.

The user's prohibitions on unrequested borders, filler labels, decorative section
numbers and northeast arrows override examples in the source videos. Use spacing,
alignment and typography to group content. Keep useful field labels, instructions,
status, accessible focus indicators and the existing documented exceptions.

## Build or redesign

### Establish the page's job

Identify the audience, the question the page must answer, and the primary next
action. For each section, name the information, evidence or control it contributes.
Use real content and assets when available. When imagery is needed, choose or create
visuals that show the actual product, place, object or person the page is about;
avoid generic atmosphere as a substitute for information. Keep unknown claims
explicit rather than inventing customers, testimonials, partners, availability or
results.

Read an existing component and its state owners before changing it. Separate a
visual defect from a product behavior decision. Ask only when the missing answer
would materially change the work; use the existing project for routine choices.

### Choose a direction from evidence when the direction is open

Follow the installed `direction-first` and `blank-direction` workflows. Inspect
relevant pages and original component implementations, then identify the mechanism
that fits this product: hierarchy, proportion, content structure or interaction.
Catalog descriptions and mood alone are not implementation evidence.

Use one coherent recommendation. Compare the actual composition with
[generic design patterns](references/generic-patterns.md), judging it against the
product. A familiar pattern is not automatically wrong, and a previous project's
palette or hero is not a default for this one. Cite only sources that changed a
decision.

### Prove the difficult part

For nontrivial choices, follow the project's plan-review workflow, which owns
representative proof and approval. Develop the hardest component with real content
before expanding production. Define only relevant states, such as pending, empty,
error, selected or completed. Static pages do not need artificial app states.

Apply [UI polish](references/ui-polish.md) to the representative component.
For navigation, forms, onboarding, settings or dense content, also read
[design principles](references/design-principles.md). Use those principles as
conditional heuristics rather than a promise of conversion or an excuse for
manipulative defaults, fake progress or false urgency.

### Implement and inspect

Use the project's tokens and components. Reflow when the actual content stops
fitting; check long labels, real images, numeric alignment and font metrics. Keep
controls usable with keyboard and touch. Persistent labels and actionable errors
must survive filled, pending and failed states.

Load `animation-fundamentals` when building motion. Name the trigger, moving
element, direction, state owner and interruption behavior. Keep frequent feedback
immediate. Preserve reduced-motion and static paths. Decorative movement needs a
reason beyond filling an otherwise empty section.

For motion decisions, read [motion and feedback](references/motion-and-feedback.md).
For loading, caching, undo, navigation, menus, touch targets or form convenience,
read the relevant rows in [interaction details](references/interaction-details.md).
Choose the techniques the component needs instead of adding every named feature.

Use `aryan-voice` for copy. Name actions and consequences plainly, keep claims
verifiable, and remove filler that repeats the interface. Keep an existing icon
system for narrow edits; use the user's preferred icons for new work.

#### Protect real product flows

When the work changes behavior, authorization, data handling or user-visible
outcomes for accounts, privileged actions, payments, uploads, user content or AI
actions, read [product trust](references/product-trust.md). Enforce permissions and
business rules on the server. Test applicable boundaries with isolated accounts and
disposable data. A visual-only change must keep claims and success states truthful,
but does not by itself trigger backend attack-path tests.

For authorized work involving identity providers, tokens, proxies, caches, database
policies or parsers, also consult [security topics](references/security-topics.md).
Determine applicability from the real stack and current primary documentation.
The reel's named incidents are not evidence that the current app is affected.

A hidden button and a polished success screen prove neither authorization nor a
successful payment.

Use available browser or device tooling under `ui-verification`. Check the changed
interaction and representative narrow, wide and intermediate layouts with real
content. Check keyboard operation, visible focus, reduced motion and relevant
failure/recovery states. When adding substantial images, fonts, video or recurring
motion, inspect resource and layout-shift cost with existing project tooling; use
[field performance data](https://web.dev/articles/defining-core-web-vitals-thresholds)
when available and label lab results as lab results.

Compare the rendered result to the brief and inspected references. Fix demonstrated
defects within scope and inspect again. Keep proposals outside scope separate.
Before delivery, run only relevant checks in [UI polish](references/ui-polish.md)
and remove unrequested borders, redundant labels or invented proof introduced.

Close with the result, compact evidence and material gaps. Distinguish source
inspection, automated checks and observed runtime behavior. Test counts cannot
certify design quality, visual fidelity, accessibility or security on their own.

## Source boundaries

[Source notes](references/source-notes.md) map the guidance to each supplied reel.
They separate observed advice from local adaptations and existing user preferences.
The videos are instructional examples, not a mandated visual template or a full
accessibility, security or research standard. Advertised downloadable skill files
were not obtained or represented as the creator's original files.
