# Motion and feedback

Source 5 in [source notes](source-notes.md) presents 19 UX and animation principles.
Use the relevant ones to define an interaction. `animation-fundamentals` remains
the source for construction recipes, drivers, timing choices and implementation.
The table below maps the reel's vocabulary to a decision and a focused check. For
non-essential animation, follow [WCAG 2.2, Animation from Interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)
and honor [`prefers-reduced-motion`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/prefers-reduced-motion).

| Principle | Decision | Check |
| --- | --- | --- |
| Exaggeration | Amplify feedback only enough to make a meaningful result legible. Prefer local emphasis over shaking an entire screen. | Errors remain readable and correction stays usable. Reduced motion removes unnecessary movement. |
| Origin awareness | Open or transform content from a meaningful trigger or spatial origin. | Resize, scrolling and keyboard activation retain a coherent origin even without a pointer location. |
| Staggering | Sequence related items when their order helps understanding. Bound the total wait. | A long list does not create a long queue before controls become usable. |
| Squash and stretch | Use deformation for a chosen physical or playful idea. Keep readable text and hit targets stable. | Content does not distort or become harder to activate. |
| Rubber banding | Use bounded resistance for direct manipulation when it clarifies an edge. | Release, cancellation and reversal settle correctly without breaking native scrolling. |
| Doherty threshold | Acknowledge input promptly and show honest pending feedback for actual work. | Measure input-to-feedback separately from server latency. The reel's 400 ms figure is not a universal pass condition. |
| Anticipation | Use a brief preparatory cue only when it clarifies a meaningful action. | Ordinary activation is not delayed by a decorative wind-up. |
| Fitts's law | Size and place targets for the actual input and task. | Touch, keyboard focus and nearby controls remain usable; a larger invisible target does not overlap a neighbor. |
| Slow in, slow out | Match easing to the mechanism. Arrival, direct manipulation and constant progress need different behavior. | Do not ease real progress or scroll mapping in a way that misrepresents the input. |
| Hick's law | Prioritize relevant choices and group or disclose the rest. | Necessary options remain findable instead of being removed for a smaller count. |
| Follow-through | Let secondary parts settle after the main action when the physical idea calls for it. | Secondary movement does not delay completion, steal focus or block the next input. |
| Arcs | Choose a curved path when it explains the spatial relationship. | Do not force every control into an arc or introduce travel unrelated to the task. |
| Von Restorff effect | Reserve emphasis for the meaningful distinction. | The primary action remains identifiable among surrounding controls. See design-principles.md for the shared rule. |
| Timing | Adjust duration to size, frequency and purpose. Reuse current motion tokens first. | The reel suggests under 300 ms for ordinary UI, not a limit on an approved authored scene or a reason to slow faster feedback. |
| Interruptible motion | Retarget, reverse or cancel from the current visual state when input changes. | Rapid activation, dismissal during entry and a new target mid-transition produce the latest intended state. |
| Secondary action | Add a supporting detail only when it reinforces the main result. | The detail does not compete, create false success or prevent immediate reuse. |
| Solid drawing | Use coherent depth or material cues for the chosen visual language. | Tilt remains optional, focus/touch paths work, and elevation does not recreate a prohibited outline. |
| Frequency of use | Shorten or remove ornamental motion in repeated actions. | Run the interaction several times, not just once in a demo. |
| Peak-end rule | Finish with truthful confirmation and the next useful action. | Success follows actual completion. Failure and retry remain clear. See design-principles.md for the shared rule. |

For every chosen effect, name the input, state owner, moving element, origin,
direction, driver, completion and interruption. Use the existing motion system.
Keep the static document and reduced-motion path useful. No effect in this list
justifies installing a new animation library on its own. If motion carries
information, preserve that information when reducing or removing the movement.
