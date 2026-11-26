# Design principles in use

Source 3 in [source notes](source-notes.md) presents these as design laws. Use them
as hypotheses for a specific interface, not universal causal claims. A polished
appearance does not prove usability, and an approximate 80/20 relationship is not
analytics for the current product. Validate a material behavior change with the
project's evidence and appropriate user research when available.

| Principle | Apply when | Implementation and check |
| --- | --- | --- |
| Aesthetic-usability effect | Establishing trust in an interface | Make hierarchy, typography and feedback coherent, then test task completion independently of visual preference. |
| Proximity | Grouping related content or controls | Keep related items closer than unrelated ones. Check the grouping after responsive reflow. |
| Von Restorff effect | Distinguishing a primary action or exceptional state | Reserve emphasis for meaningful differences. Verify that several equally loud controls do not compete. |
| Zeigarnik effect | Resuming real unfinished work | Preserve progress and show an honest resumable task. Avoid nagging, fake incompleteness or pressure to finish unwanted work. |
| Tesler's law | Handling unavoidable complexity | Let the system carry formatting, calculation and known context. Keep important consequences visible and errors recoverable. |
| Pragnanz | Simplifying a graphic or dense arrangement | Use clear structure and simpler geometry without removing necessary meaning. Check that simplification preserves distinctions. |
| Serial position effect | Ordering navigation or a short set of choices | Place meaningful high-priority choices where users can find them. Do not bury mandatory information or destructive consequences. |
| Progressive disclosure | Offering advanced configuration | Show essential controls first and keep advanced controls discoverable, keyboard reachable and stable when revealed. |
| Common region | Identifying a group | Use spacing, alignment and typography first. A compatible surface fill can support a real group; the user's border prohibition still applies. |
| Goal-gradient effect | Showing a real multi-step process | Show actual completed and remaining work. Reconcile validation, retries and back navigation without fake progress or hidden new steps. |
| Similarity | Repeating related controls | Give equivalent actions consistent appearance and behavior. Keep different interaction types distinguishable. |
| Recognition over recall | Choosing, searching or resuming | Expose useful options, examples, recent items or context. Do not reveal private history to the wrong viewer. |
| Pareto principle | Prioritizing frequent work | Use actual task evidence to prioritize common actions. Keep less frequent necessary actions available. Never assert a measured usage ratio without data. |
| Occam's razor | Choosing between equally capable designs | Prefer fewer concepts and controls when outcomes and recovery remain clear. Do not remove necessary explanations or safeguards merely to shorten the screen. |
| Parkinson's law | Reducing time and effort to complete a task | Remove avoidable steps, preserve input and offer valid defaults. Do not manufacture deadlines, countdowns or pressure. |
| Uniform connectedness | Explaining an actual relationship or sequence | Use structure, ordering and interaction to make the relationship clear. Avoid decorative connectors or frames added merely to force grouping. Meaningful explanatory diagrams retain their approved drawing idiom. |
| Active-user paradox | Teaching a feature | Put brief help at the point of action and allow recovery. Keep required instructions accessible; avoid forcing a tutorial before a simple task. |
| Cognitive load | Reducing competing information | Remove redundant controls and repeated explanation, chunk related information and prioritize the active task. Preserve the facts needed for a decision. |
| Default effect | Selecting initial settings | Use a reasonable, visible and reversible default. Make costs, privacy implications and irreversible consequences clear. Avoid deceptive opt-ins. |
| Peak-end rule | Completing a meaningful workflow | Make completion and recovery accurate, useful and clear about what happens next. Do not celebrate a result before the server confirms it. |

Use the smallest set of principles that explains the actual decision. Do not add
UI to demonstrate every named principle or claim that a heuristic makes a page
accessible, secure or high-converting by itself.
