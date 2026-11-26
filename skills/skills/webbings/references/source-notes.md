# Sources and interpretation

These notes document the seven Instagram reels supplied by the user. The skill is
an original synthesis of observed advice and local constraints. It is not a copy
of the creators' advertised downloadable skill files.

Public metadata and video files were retrieved with the existing `yt-dlp`, without
browser cookies or account access. Video inspection used timestamped frames,
on-screen demonstrations and burned-in subtitles. Audio was not independently
transcribed. A sampled frame can establish its visible content, not the exact
wording of speech between frames or a usability research result.

## Coverage

| Source | Creator | Topic | Inspection |
| --- | --- | --- | --- |
| [1. DgIYTG0xNrM](https://www.instagram.com/reel/DgIYTG0xNrM/) | Charles Liu, `charles.unemployed` | Practical interface polish | Metadata, final complete list and demonstrations sampled across 62.44 seconds. |
| [2. DgF9OjDxYKD](https://www.instagram.com/reel/DgF9OjDxYKD/) | Charles Liu, `charles.unemployed` | Recurring generic AI design choices | Metadata, completed list and demonstrations sampled across 26.51 seconds. |
| [3. DgDL0qsR_uD](https://www.instagram.com/reel/DgDL0qsR_uD/) | Charles Liu, `charles.unemployed` | Design psychology | Full explanatory caption, final list and demonstrations sampled across 28.33 seconds. |
| [4. DgEnfQmuViz](https://www.instagram.com/reel/DgEnfQmuViz/) | Ryan Naghibzadeh, `ryannaghib` | Security failures in generated apps | Metadata, one-second samples of illustrated examples and burned-in subtitles across 29.58 seconds. |
| [5. Df7ehKURrLy](https://www.instagram.com/reel/Df7ehKURrLy/) | `bendoescareer` | UX and animation principles | Full explanatory caption, one-second samples and complete final list across 21.10 seconds. |
| [6. De7aochhik3](https://www.instagram.com/reel/De7aochhik3/) | Aidan Murphy, `murphmaxxing` | Twenty interaction details | Metadata, one-second samples and complete final list across 24.52 seconds. |
| [7. DfsWbkrB6vN](https://www.instagram.com/reel/DfsWbkrB6vN/) | Aidan Murphy, `murphmaxxing` | Twenty security topics | Metadata, one-second samples, visible source labels and complete final list across 40.19 seconds. |

## Source 1, practical polish

The completed list and demonstrations cover paragraph alignment, label-to-button
proportions, regular body weight, coordinated neutrals, separation of destructive
actions, display leading, layered elevation, sentence case, foreground color on
tinted surfaces, baseline alignment, persistent labels, coherent chart hues,
horizontal padding, specific action wording, heading spacing, dark-theme color,
numeric alignment, value/label spacing, useful empty states and primary-action
prominence. These are developed in [UI polish](ui-polish.md).

Approximate demonstration groups are typography and control hierarchy at 0 to
18 seconds, depth/color/alignment at 18 to 30 seconds, labels/color/padding/action
wording at 30 to 42 seconds, and heading/theme/numeric/empty/action details at
42 to 60 seconds. The caption credits Dan Liu's text-layout and color threads and
Emil Kowalski; their original articles were not independently inspected here.

Local interpretation keeps the relationships while rejecting mandatory blue
neutrals, a universal button ratio, fixed spacing numbers or elevation that
recreates prohibited outlines. Contrast, writing direction, accessibility and the
incumbent design system still determine the implementation.

## Source 2, generic design patterns

The video combines a cumulative list with examples at roughly one-second intervals.
The caption says that individual patterns can be appropriate and criticizes
stacking many defaults. [Generic patterns](generic-patterns.md) preserves this
qualification across decoration, typography, repeated cards, fabricated proof,
status indicators and scroll reveals.

This skill does not turn Instrument Serif, a cream background, an italic word or
dithering into an automatic failure. It does preserve the user's existing strict
rules for northeast arrows, unrequested borders and filler labels. Numbers shown
inside this critique are not adopted as measured prevalence statistics.

## Source 3, design psychology

The explanatory caption names and describes 20 principles. The video illustrates
hierarchy near 1.5 seconds, emphasis near 4.5, simplified visual structure near
7.5, advanced settings near 10.5, visible progress near 13.5, prioritization near
16.5, relationship cues near 19.5 and cognitive load near 22.5.

[Design principles](design-principles.md) translates all 20 into conditional
decisions and checks. These are heuristics. The skill adds safeguards against
fake progress, manufactured urgency, deceptive defaults, universal usage ratios,
and assuming that a better-looking screen proves task usability.

## Source 4, product trust

Near 2 to 7 seconds, illustrated examples show direct privileged-route access,
record identifier changes and privileged keys in browser source. Near 7 to 14,
they show client-controlled pricing/quantity, forged payment state, repeated
discount use, client-supplied privileges and repeated login-code guesses. Near
14 to 21, they show unauthorized AI actions, executable user content, disguised
uploads, exposed environment configuration and unsafe database input.

[Product trust](product-trust.md) provides conditional defensive controls for
these features. Price and quantity validation share one row. Payment-provider
verification, atomic redemption and other engineering details are local defensive
interpretations of the illustrated failure, not verbatim creator instructions.
A static design change does not trigger a full security audit.

## Source 5, motion and feedback

The caption explains all 19 named principles. The video illustrates amplified
feedback, origin, stagger, deformation and overscroll near 0 to 4 seconds;
response, anticipation, targeting, easing and choice reduction near 5 to 9;
follow-through, arcs, emphasis and interruption near 10 to 14; and secondary
motion, depth, use frequency and completion near 15 to 18.

[Motion and feedback](motion-and-feedback.md) covers all 19. The reel's caption
suggests a response within 400 ms and ordinary animations under 300 ms. These are
creator recommendations, not universal constraints or benchmark findings.
Input acknowledgement, backend latency and animation duration are different
measurements. The existing animation skill still owns implementation recipes
and timing chosen for the actual mechanism.

## Source 6, interaction details

The complete list covers skeletons, optimistic updates, command menus, shortcut
hints, undo, stale-while-revalidate, pre-rendering, image placeholders, view
transitions, dismissible sheets, interruptible motion, predictive back, expanded
hit targets, safe areas, code autofill, aligned numeric glyphs, headline wrapping,
continuous corners, idempotency and a forgiving pointer path into a submenu.
The terms appear in sequence near 0 to 20 seconds, with a complete list near 21.

[Interaction details](interaction-details.md) supplies conditional decisions and
checks for all 20. Failure recovery, privacy-safe caching, platform support,
keyboard behavior and static fallbacks are local engineering additions. The reel
names techniques but does not prove those implementations. Its caption's company
references do not establish access to the companies' source code.

## Source 7, security topics

The completed list and visible source labels cover HTTP/2 Rapid Reset near 3 to 4
seconds, identity-provider examples near 5 to 9, GraphQL aliases near 10 to 12,
authentication replay near 13, regex cost near 14 to 15, JWT validation near 16 to
17, request framing near 18, cache poisoning near 19 to 20, trusted IP headers near
21, database views/policies near 22 to 23, token randomness near 24 to 25, timing
leaks near 26 to 27, encryption-oracle risks near 28 to 29, object pollution near
30 to 31, template injection near 32, XML entities near 33 to 34, WebSocket
handshakes near 35 and Unicode identity handling near 36 to 37.

[Security topics](security-topics.md) records all 20 as applicability questions.
The creator displays advisory/documentation labels; those original advisories,
historical attack figures and affected versions were not independently inspected.
Specific remediation requires checking the actual stack against current primary
documentation. This skill does not claim that every application has these issues
or that a static checklist is a penetration test.

## Existing constraints and limits

The no-border/no-filler/no-northeast-arrow rules, preferred icon library, copy
voice, exact-copy process, approval workflow, scoped changes, motion workflow,
runtime verification and VPS exceptions come from the dotfiles. They are not
attributed to the Instagram creators.

No comments or direct messages were sent. No advertised prompt pack or skill file
was fetched. The skill has no executable dependency or requirement to contact a
creator. Original media stays in task-local inspection storage and is not bundled
as a reusable asset. Frame inspection and static packaging checks do not certify
the performance or reliability of future agents using the skill.
