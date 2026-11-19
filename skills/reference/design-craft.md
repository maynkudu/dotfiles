# Design craft

Use this for UI planning, generation, editing and review. Fixed personal constraints remain shared. Keep each project's design tokens, composition, assets and accepted decisions in its own references and approved brief.

## Build the component, not an isolated screenshot

Aim for the design and motion standard of the approved Kitse booking-completion example. This means deliberate hierarchy, proportions, typography and state transitions, not copying a green panel onto every page or calling arbitrary motion award-winning.

Before expanding production, develop the hardest representative component. Define its default, loading, empty, error, selected and disabled states. Name which element moves, what drives it, where it starts and ends, and how new input interrupts it. Keep ordinary input immediate. Use the existing motion system and reduced-motion preference handling.

Fields need aligned visible labels, consistent control heights, readable fills, and width suited to their contents. Reserve icon and chevron space independently of the text. Inspect long names and translated text. Keep errors and recovery actions usable. A polished successful state does not excuse a broken selection or checkout path.

## Proportions and SVG

Inspect [Calculus of Interfaces](https://calculus-of-interfaces.vercel.app/) for layout reasoning. Measure allocated content width, padding, gaps, minimum readable control/card width, text wrapping and the amount of relevant content above the fold. Choose reflow from those constraints rather than the viewport alone. Its illustrative math is not proof of an unrelated layout; measure the actual render.

Load `plotter` for explanatory construction SVGs and their animation. Follow its relationship-first composition, editable vectors and motion workflow. Keep its transparent monochrome grammar. Ordinary Rune icons, existing ticket SVGs and other established illustrations retain their own idiom. Use `animation-fundamentals` for interface motion, not Plotter as a substitute for all animation.

## Finish

Operate the real product at representative desktop, tablet and phone widths, in both themes where applicable. Check the full transition, keyboard/focus behavior, interruption and reduced motion. Compare the result to the approved example and brief. Fix demonstrated defects within scope, then inspect again. Proposed improvements outside the brief need approval. Keep sources, decisions and verification evidence in task artifacts.

Builds, authored previews and test counts establish only their specific checks. State unverified visual, live-data and provider paths directly. Do not claim agency quality, fidelity or functional success without the corresponding evidence.
