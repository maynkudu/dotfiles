# UI polish

Based on source 1 in [source notes](source-notes.md), interpreted against the
project and the user's existing constraints. Use the relationships below as
starting points. Inspect actual font metrics, content, theme and control sizes
before choosing values. Preserve approved exact reproductions.

## Reading and hierarchy

- Give long paragraphs a stable reading edge. In left-to-right content this
  usually means left alignment. Follow the writing direction for other scripts.
  Short centered hero copy can remain centered when it reads well.
- Keep ordinary body copy at a readable regular weight. Reserve stronger weight
  for genuine hierarchy and emphasis. Inspect the actual variable font instead
  of assuming a weight number looks the same in every family.
- Tune display leading more tightly than paragraph leading when the font permits.
  Check wrapped headings, ascenders, descenders and zoom for clipping or collisions.
- Use sentence case for ordinary labels. Preserve names, acronyms and content that
  requires another case. Avoid decorative uppercase labels that repeat a heading.
- Align mixed-size inline text on an appropriate baseline. Optically check icons
  and controls separately rather than assuming geometric centering looks aligned.
- Make space above a heading distinguish it from the previous group. Keep the
  heading closer to the content it introduces. Use actual text wraps to judge gaps.
- Use the smaller text's metrics to judge value/label spacing. The video's example
  ratio is a diagnostic, not a fixed token or a required one-line-height gap.

## Controls and state

- Judge button label width against its shell. Give the label breathing room and
  usually more horizontal than vertical padding. A label occupying about half the
  shell is one example, not a layout requirement. Preserve target size, content-fit
  sizing and long-label behavior; never pad a short label into an arbitrary slab.
- Give the primary landing-page action clear prominence relative to secondary
  controls. Size, placement, wording and contrast should communicate the hierarchy.
- Keep destructive actions apart from routine save/confirm actions. Pair their
  visual distinction with clear consequences and appropriate recovery or confirmation.
- Keep visible field labels after typing. Placeholders can provide examples but
  must not be the only label. Associate labels, instructions and errors with fields.
- Name what an action does. Where it matters, show cost or consequence before the
  action. A disabled or pending control must explain its state when unclear.
- Make empty states useful. Offer the relevant next action when available. Treat
  first use, a filter with no matches, insufficient permission and a failed fetch
  as different states. Do not use a create action to conceal an error.

## Color, depth and data

- Coordinate neutral undertones with the brand and adjacent surfaces. A blue tint
  is an option from the source, not a requirement to recolor every project's grays.
- On a colored surface, harmonize foreground color while retaining measured
  contrast. A harmonious hue is not evidence that muted text is readable.
- Give a chart category a consistent hue across views. Add labels, shape or other
  cues when needed so color is not the sole signal. Preserve established semantics.
- Tune dark-theme lightness and saturation independently. Check text, selected,
  hovered, disabled, error and focus states on the actual dark surfaces.
- Use restrained layered elevation only when it helps explain depth. The user's
  no-border rule includes outlines recreated with shadows. Do not add those.
- Right-align comparable numbers and use tabular numerals where the font supports
  them. Keep units, decimals and currency conventions consistent. Ordinary prose,
  identifiers and labels do not become numeric columns merely because they contain digits.

## Focused delivery check

| Check | Evidence required |
| --- | --- |
| Reading order and hierarchy | Actual text at narrow and wide widths, with readable wrapping and meaningful grouping. |
| Controls | Visible labels, usable targets, relevant state transitions and unambiguous primary/destructive actions. |
| Accessibility | For affected web UI, check keyboard operation, visible and unobscured focus, text enlargement and reflow at 320 CSS px. Assess applicable contrast and target-size criteria in [WCAG 2.2](https://www.w3.org/TR/WCAG22/) and [WAI's reflow guidance](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html). A screenshot cannot establish semantics or keyboard behavior. |
| Color and data | Measured contrast where applicable, consistent category meaning, readable dark-theme states and aligned numeric comparisons. |
| Completeness | Relevant empty, pending, error and recovery paths exercised with representative content. |
| Specificity | Assets, claims and composition fit the product; no invented statistics or unrelated stacked defaults. |
| User constraints | No introduced filler labels, decorative section numbers, unrequested borders or northeast arrows. |

Apply only checks relevant to the change. Use WCAG as a standard, not as a claim
that a focused visual check establishes conformance. Record unavailable evidence
rather than claiming that a build or a single screenshot verifies the whole experience.
