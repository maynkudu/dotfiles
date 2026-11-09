# Apple design patterns for a portable design and animation system

Research completed on 2026-11-09. This note covers product structure, control meaning, state, and presentation. It complements the typography, color, accessibility, materials, and motion research in this folder.

Use Apple as a documented design reference. Preserve the target product's audience, information model, brand, and platform conventions. A portable system should define what an interaction means, then let a platform adapter decide its placement, appearance, input handling, and implementation.

## Evidence and limits

`Documented` below means the cited Apple text states the behavior. `Adaptation` means a proposed portable rule derived from that behavior. Neither label means the behavior has been operated or visually verified in a prototype.

Eight HIG pages were retrieved as Apple's JSON document bytes and read. Two previously captured WWDC transcripts were read in full. The layout page was reused from the foundation research. Context7 resolved the official HIG collection and returned guidance before these requests. No quota or source-access failure occurred. BLANK registry search returned no installable for `adaptive navigation controls`; discovery for `adaptive navigation interaction design` reported unavailable reranking. Its returned general references did not change this primary-source investigation. No product was edited, component installed, browser operated, or animation rendered.

All durations, dimensions, platform API names, and visual behavior in Apple sources remain Apple-specific unless explicitly adapted. Current HIG text can be newer than the 2025 sessions. For example, the captured sheets page includes a March 2026 button-placement update. Check the relevant platform and SDK before implementing a native adapter.

| ID | Primary source and section | Brief evidence | Decision changed |
| --- | --- | --- | --- |
| D1 | [HIG Layout](https://developer.apple.com/design/human-interface-guidelines/layout), Visual hierarchy and Adaptability > Size classes | "Determine layout based on size classes, not device type or orientation." "Keep functionality the same as size classes change." | Resize by available space while preserving tasks and state. Do not use device names as the product model. |
| D2 | [WWDC25 Get to know the new design system](https://developer.apple.com/videos/play/wwdc2025/356/), 13:43-17:22 | "When content is intentionally grouped, it should stay together, even as the layout adapts." "Components should always support the same set of core interactions." | Define shared content relationships, anatomy, and behavior. Adapt the presentation. |
| D3 | [WWDC25 Build a SwiftUI app with the new design](https://developer.apple.com/videos/play/wwdc2025/323/), 03:25-04:53 and 11:18-13:56 | "TabViews provide persistent, top-level navigation." "Maintaining context within each section." | Separate top-level destinations, hierarchical browsing, and search scope. Apple search placement varies across platforms. |
| D4 | [HIG Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons), Best practices, Style, Content, Role | "Always include a press state for a custom button." "Don't assign the primary role to a button that performs a destructive action." | Buttons are actions with explicit roles and feedback. Action hierarchy must avoid accidental destructive confirmation. |
| D5 | [HIG Sliders](https://developer.apple.com/design/human-interface-guidelines/sliders), Best practices and macOS | "Consider supplementing a slider with a corresponding text field and stepper." "Consider giving live feedback as the value of a slider changes." | Continuous adjustment and exact entry are different needs. Provide both when precision matters. |
| D6 | [HIG Toggles](https://developer.apple.com/design/human-interface-guidelines/toggles), Best practices and Platform considerations | "A toggle always lets people manage the state of something." "Avoid relying solely on different colors to communicate state." | Treat a toggle as a state control. Support clear off, on, and applicable mixed states. |
| D7 | [HIG Segmented controls](https://developer.apple.com/design/human-interface-guidelines/segmented-controls), introduction and Best practices | "A segmented control can function as a set of buttons that perform actions without showing a selection state." "Keep control types consistent within a single segmented control." | A segmented appearance does not determine its semantics. Select an action group, single choice, multiple choice, or related-panel switch deliberately. |
| D8 | [HIG Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars), Actions and Item groupings | "Group toolbar items logically by function and frequency of use." "Keep actions with text labels separate." | Grouping can express related actions, but each action must remain distinguishable. |
| D9 | [HIG Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets), Anatomy and Best practices | "For complex or prolonged user flows, consider alternatives to sheets." "Display only one sheet at a time from the main interface." | Use a short sheet for a bounded task. Use a workspace, page, panel, or window for ongoing work. |
| D10 | [HIG Popovers](https://developer.apple.com/design/human-interface-guidelines/popovers), Best practices and iOS, iPadOS | "Always save work when automatically closing a nonmodal popover." "Avoid displaying popovers in compact views." | Preserve temporary work and source context. Narrow layouts can need a different presentation. |
| D11 | [HIG Progress indicators](https://developer.apple.com/design/human-interface-guidelines/progress-indicators), Best practices | "Be as accurate as possible when reporting advancement in a determinate progress indicator." "If a process stalls for some reason, provide feedback." | Loading is an operation state with truthful progress, cancellation policy, and a recovery path. |

HIG source bytes and SHA-256 metadata are in [design-pattern-sources](design-pattern-sources/). WWDC bytes and transcripts are in [apple-primary-sources](apple-primary-sources/). The reused layout capture is in [design-foundation-sources](design-foundation-sources/).

## Product structure decisions

Start with the audience's work, then name destinations, content objects, commands, and temporary tasks. This prevents every screen from becoming a collection of decorative glass controls.

| Need | Documented Apple pattern | Portable adaptation | Platform boundary |
| --- | --- | --- | --- |
| Switch between independent main areas | Persistent tabs maintain each section's context. D3, 04:40-04:53. | Model a stable destination and its own history, filters, and scroll position. Choose visible navigation according to frequency and available space. | Do not force a bottom tab bar onto desktop, websites, or Android apps with an established navigation system. Web destinations should retain URL and browser-history behavior. |
| Browse categories, collections, and details | A split view supports a defined hierarchy with possibly many root categories. D3, 03:25-03:33. | Define category, collection, selected object, and detail separately. Show more columns when the content fits. In a narrow view, retain the selection while displaying one step at a time. | A collapsed hierarchy needs a reliable return path. Desktop can keep list and detail visible. A phone presentation does not determine the data model. |
| Search | Toolbar search and a dedicated search destination are separate patterns. D3, 11:18-13:56. | Declare what search covers. Place it where that scope is clear. Preserve query and results as the layout changes. | Bottom search on iPhone and top-trailing search on iPad and Mac are Apple adapter choices. Global website search and local table search need their own placements. |
| Act on the current view or object | Toolbars contain title, navigation, and actions; tab bars navigate app areas. D8, introduction. | Distinguish global commands, view commands, and selected-object commands. Keep a small set of frequent actions visible and place secondary actions in a clear menu. | Native Apple overflow is system-managed. A web or other-platform adapter may need its own accessible overflow implementation. Do not mistake that implementation for a native API requirement. |
| Edit while observing results | Apple recommends a nonmodal view for supplementary tools, with panel or split-view alternatives. D9, Best practices and macOS. | Use an inspector or adjacent panel for repeated edits and live preview. Keep its selected object explicit. | A formatting tool can be a nonmodal sheet on iOS and iPadOS, a panel on macOS, or an adjacent region on the web. The tool's task stays the same. |
| Complete a short interruption | Sheets request specific information before return to a parent. D9, introduction. | Name the parent, draft, commit action, and cancel action. Return to the same parent state. | Apple sheet modality and dismissal placement vary by platform. Other platforms may use a dialog or route. Long editing sessions need a full workspace. |
| Show a few temporary related choices | A popover exposes a small amount of functionality and points to its source. D10, Best practices. | Keep a source relationship and a bounded task. Avoid obscuring essential context. Preserve changes on implicit dismissal when the task applies changes live. | On narrow layouts use a sheet, dialog, or page if an anchored popup cannot fit. Do not copy a popover's visual geometry at the expense of usable space. |

Adaptation should depend on available width and height, text scale, input capabilities, and the platform's established idiom. A narrow desktop window can need fewer columns while retaining desktop navigation, menus, and keyboard conventions. D1 explicitly separates size class from platform idiom.

Keep intentional content groups together as they reflow. Keep the same object's title, preview, metadata, and commands associated. Reflowing a group is preferable to detaching its commands into an unrelated region.

## Control contracts

Choose the semantic contract before a visual recipe or animation.

| Control | Contract | Design rule | Source and limitation |
| --- | --- | --- | --- |
| Button | Performs one named action. Has normal, primary, cancel, or destructive intent. | Give it a clear label or familiar icon, distinguish its press state, and reserve prominent style for the most likely safe action. Keep related choices the same size and distinguish importance through style. | D4, Style and Role. Apple suggests one or two prominent buttons per view; its toolbar guidance specifies one primary toolbar action. These counts apply to different contexts. |
| Navigation item | Changes destination or hierarchy level. | Display current location separately from pointer hover and keyboard focus. On the web, preserve link semantics for destinations. | D3 and D8 support the navigation/action distinction. The web link rule is an adaptation, not an Apple API claim. |
| Slider | Adjusts a value over a defined range or repeating domain. | Show its label, units, range, and current value when needed. Preview results during adjustment when safe. Add exact entry when the task requires precision. Define when changes preview and when they commit. | D5. Apple defines leading-to-trailing minimum-to-maximum for horizontal sliders. Respect the target platform's bidirectional conventions. Exact entry and commit policy are product decisions. |
| Switch or toggle button | Changes a named state between opposing values. | Make state clear through thumb position, checkmark, fill, or another cue in addition to color. Keep the label stable so it names the setting rather than alternately naming an action. | D6. Apple currently specifies switches only in list rows on iOS and iPadOS and different toggle styles elsewhere. That restriction belongs to those adapters. |
| Checkbox | Selects an independent option and can represent a mixed aggregate state. | Let subordinate selections remain understandable. An aggregate checkbox must reflect mixed values accurately. Use label alignment and indentation to show dependencies. | D6, macOS > Checkboxes. Mixed-state semantics may be portable; the visual treatment remains platform-specific. |
| Segmented single choice | Selects one closely related option, state, or view variant. | Use comparable labels and maintain one selection. Keep action-only segments out of this control. Use a panel-tab contract only when the segments actually select associated panels. | D7. The adapter might use radio choices, tabs, or a picker according to the actual task. A pill-shaped group is insufficient evidence for choosing an accessibility role. |
| Segmented multiple choice or action group | Toggles several independent attributes, or provides several related momentary actions. | Choose one of these meanings for the whole group. Preserve each segment's independent state or action. | D7 documents both on macOS. Do not generalize multiple-choice support to every platform's native segmented control. |
| Toolbar group | Groups independently operable commands by function and frequency. | Retain each command's own name, role, bounds, press state, focus target, and activation. Separate a text action from neighboring icon actions when the shared background suggests one combined button. | D8, Item groupings; D2, 09:33-09:50. A shared background describes association. It does not combine commands. |

A glass sampling container, visual group, or morphing shape must not become a single semantic control merely because its children share material. D3, 19:51-20:29 documents shared sampling for visual correctness. It does not authorize merging accessibility targets, click regions, command identity, or selection state.

Apply a custom control's material to the control's outer shape, with its label and icon inside. D2, 07:15-07:22 specifies applying material directly to the control rather than its inner views. This avoids treating each visual fragment as an independent glass object.

## Presentation and identity

| Relationship | Documented behavior | Portable recommendation | Required check |
| --- | --- | --- | --- |
| Action to short presentation | Action sheets extend from the tapped source. D2, 06:54-07:10. Sheets can morph from their presenting buttons when source and destination are marked for a zoom transition. D3, 07:05-07:35. | Store the actual invoking element or source object, presentation kind, and destination identity. Animate from that source when the renderer supports it and the connection remains legible. | The animation begins at the correct source after scrolling, resizing, or reopening from another trigger. Never imply that unrelated content is the same object. |
| Modal task | A sheet interrupts interaction with its parent and uses dimming to indicate focus. D9, Anatomy; D2, 07:35-07:48. | Restrict parent interaction for a truly modal task. Keep the task's draft and cancel policy explicit. A web dialog needs suitable focus handling and a return target. | Test keyboard entry, dismissal, background interaction, unsaved work, and return focus. The keyboard rules are portable implementation recommendations, not behavior verified here. |
| Parallel tool | A nonmodal view affects its parent while the main task continues. D9, Best practices. | Preserve access to the content under edit and avoid a blocking scrim. An inspector, panel, or nonmodal sheet should show which object it affects. | The user can operate the parent. Selection changes update the tool without losing drafts unexpectedly. |
| Small anchored popup | A popover should remain connected to its revealing element, avoid essential content, and preserve work on automatic dismissal. D10, Best practices. | Record anchor geometry, a collision rule, and a logical source identity. Reposition the same popup as space changes. If it becomes a larger presentation, carry its task state into that presentation. | Open near viewport edges, scroll the source, resize, click outside, press Escape if applicable, and reopen. Verify that dismissal and selection semantics match the task. |
| Same content in a new layout | Grouped content and common component anatomy persist across devices. D2, 15:06-17:22. | Keep stable object IDs through list-to-detail, inspector changes, and resize. A shared-element transition is optional and requires real identity continuity. | Focus, selected object, draft, and current value survive layout changes. Verify interrupted transitions using the motion contract. |

Back, Cancel, Close, and Done need distinct behavior. D9 says Back changes a step or hierarchy level and is not a sheet-dismiss command. Cancel or Close can dismiss without saving. Done completes or explicitly saves the task. Those actions must be defined before assigning animation or styling.

Do not copy the popover's pointer geometry when doing so would violate the user's prohibited northeast arrow shape. Use a source-relative position, origin animation, and plain label if needed. The relationship matters more than reproducing a particular indicator.

## State and feedback

This table is a portable state specification. Its Apple evidence supports the stated design purpose. The exact keyboard events, accessibility mapping, error policy, and operation lifecycle still require the target platform's authoritative guidance and product verification.

| State or event | What the interface must communicate | Portable behavior | Evidence status |
| --- | --- | --- | --- |
| Idle | The control's purpose and current stored value. | Keep the target distinguishable from content. Do not rely on hover to reveal essential labels or commands. | D4, Content and Best practices. No-hover dependency is an adaptation. |
| Hover | Pointer presence or available action. | Show a reversible local cue. Do not change stored selection merely because the pointer passed over it. Tooltips can explain an icon but cannot replace its accessible name. | D4 documents tooltips for macOS and visionOS. Selection policy and naming are adaptations. |
| Focus | Which element receives keyboard, remote, or assistive input. | Give focus its own observable cue. Keep focus separate from selected and pressed state. Route input through the platform adapter. | Adaptation. Apple tvOS segmented controls explicitly select when focus moves, D7 > tvOS. Preserve that native exception rather than claiming every platform activates only on click. |
| Press or active touch | The user has engaged the control. | Give immediate local press feedback without delaying activation for a finishing animation. Track press, release, cancellation, and pointer exit according to platform convention. | D4 requires a custom press state. D3, 01:09-01:20 describes toggles, segmented pickers, and sliders changing material during interaction. Exact event sequencing is an adaptation. |
| Selected, checked, or mixed | The current persisted or previewed state. | Use a visible indicator beyond color. Expose the correct role and value. Keep selection legible without hover or animation. | D6 documents non-color state cues and mixed checkbox state. Role mapping is an adaptation. |
| Disabled | The action is currently unavailable. | Block activation through every input path. Keep the label readable. Provide a reason or prerequisite in context when users need it. Do not let glass animation suggest an available command. | Adaptation. A complete disabled-state behavior was not established by the ten main source reads. |
| Loading or saving | A named operation is running and its result is not yet confirmed. | Use local feedback near the initiating action. Show determinate progress only when measured progress exists. Prevent duplicate irreversible submissions. Permit cancel or pause when the operation can safely support them. | D4, iOS and iPadOS documents a button activity indicator with an optional changed label. D11 documents truthful progress and safe interruption. Duplicate-submission policy is an adaptation. |
| Error or stalled operation | What failed, what work remains, and what the user can do. | Preserve input. Replace indefinite busy feedback with a specific error and a suitable retry, edit, cancel, or recovery action. Keep errors near the affected task. | D11 documents stalled-process feedback. Exact error placement, retry policy, and draft preservation are adaptations. They were not separately verified against HIG Alerts or error-message guidance here. |
| Completion | The requested operation succeeded and the resulting state is available. | End transient progress, update the actual content, and keep any confirmation proportional to uncertainty. A bounce or checkmark does not substitute for committed state. | D11 states that progress indicators disappear after completion. Remaining rules are adaptations. |

Appearance and behavior are separate concerns. A spring, gloss change, or haptic cue can reinforce a state transition, but the value, role, and available action must remain understandable with that effect disabled. Reduced-motion, reduced-transparency, contrast, text-scale, and screen-reader details belong with the foundation and motion references.

## Whole-interface visual hierarchy

Use these decisions before detailing materials and animation.

1. Order content by task importance and reading direction. Align related content, and use indentation only for actual hierarchy. D1, Visual hierarchy.
2. Separate primary content, navigation, view commands, and selected-object tools. Use layout and functional grouping to express hierarchy. D2, 08:55-09:41.
3. Show the small set of choices needed now and disclose secondary commands when useful. Overflow cannot hide the only safe exit or recovery path. D1 supports progressive disclosure; the exit rule is an adaptation.
4. Reserve visual prominence for the relevant primary action. A destructive action cannot inherit a default-confirm role just because it is frequent. D4, Role.
5. Use materials to distinguish controls from content while preserving legibility. Decorative blur on every card adds no documented functional hierarchy. D1 and D2, 06:24-06:37 and 11:02-11:39.
6. Keep symbolic meaning stable across layouts, and use a text label when an icon has no clear shorthand. D2, 15:12-15:32. For this user, select Rune Icons by default and keep an existing project's icon system for narrow changes.
7. Match shape and density to the setting. Apple uses capsules for touch-friendly layouts and standout desktop actions, while small and medium macOS controls retain rounded rectangles. D2, 04:15-04:44; D3, 14:25-15:22. A portable design should not make every desktop inspector control a large capsule.
8. Keep critical text and controls inside usable regions. Background imagery can extend beyond those regions. D1, Guides and safe areas; D2, 12:49-13:07. Respect the target platform's system UI and keyboard rather than copying Apple safe-area values into every renderer.

Apple brand assets, SF fonts, and SF Symbols are not prerequisites for these rules. Their licensing must be checked independently. Do not package Apple UI kits or symbols as a general cross-platform icon library. The user's prohibition on every northeast or up-right arrow representation takes priority over any Apple reference, icon suggestion, or pointer treatment.

## Representative forward-test brief

This is an unimplemented proposal for testing whether a skill guides a whole product rather than producing isolated effects. It is not an Apple sample, an approved product brief, or evidence of a rendered result.

Build a small media-library editor for someone selecting photographs, making a few reversible adjustments, and exporting a collection. Use a local fixture with named collections and a dozen original or licensed sample images. Network accounts, real payments, and backend deployment are outside this test.

| Region or task | Required content and behavior | What it tests |
| --- | --- | --- |
| Top-level navigation | Two destinations, `Library` and `Exports`. Preserve the current collection and selected photograph when switching away and back. | Destination identity and task continuity. |
| Library hierarchy | Collection navigation, photograph list or grid, and selected-photo detail. On a wide layout, show collection, content, and inspector as space permits. On a narrow layout, show one main step with a clear return path. | Adaptive anatomy without changing available functionality. |
| Toolbar | Collection title, `Search photos`, `Add photos`, `More`, and a separate `Export` action. The search scope is the library. Keep secondary commands in More. | Titles, search scope, command hierarchy, overflow, and semantic grouping. |
| View choice | A single-choice segmented control with `Grid` and `List`. It changes layout presentation, not the selected collection. | A choice contract that is separate from top-level navigation. |
| Selection | A selected photograph has a stable ID, visible selection cue, detail, and associated inspector. A `Favorite` toggle changes its state. | Selected, focus, and toggle state remain distinct. |
| Inspector | `Exposure`, a bounded slider with a value field, and `Auto-adjust`, a named binary setting. Show the selected image's preview. Provide a reversible reset. | Continuous adjustment, exact entry, live preview, and state consistency. |
| Temporary choices | Open collection sorting from its source control. Use a compact anchored presentation on a wide layout and a suitable larger presentation when narrow. Preserve its selected choice across adaptation. | Source anchoring, collision behavior, dismissal, and responsive task continuity. |
| Export sheet or dialog | Title `Export collection`, a small set of settings, `Cancel`, and `Export`. The action exports the selected collection. Keep draft settings if export fails. | Bounded task, cancel versus commit, source identity, and loading. |
| Export outcome | While running, show truthful local progress. A deterministic fixture can fail with `Export failed. Your settings are saved.` and `Try again`. On success, show the resulting export entry in Exports. | Error recovery and real resulting state. The failure message is fixture copy and needs a behavior check before use. |

Use at least one source-connected presentation transition, one interruption-safe value adjustment, and one optional proximity or shared-material effect for a logically related control group. Effects must preserve the controls' identities and labels. Do not add an effect only to make the test look animated.

For an offline motion demonstration, render a scripted subset of the same interface states. Show collection selection, photograph selection, adjustment, presentation, and export outcome. Keep the same object identity and hierarchy in the render specification. Represent the input sequence explicitly in the recording specification. A rendered video has no live hit testing, accessibility tree, or actual asynchronous export, so it must not be reported as verification of those behaviors.

Acceptance checks for an implemented forward test:

- Resize between a narrow phone-like viewport, a tablet-sized window, and a wide desktop window. Preserve collection, selection, query, scroll context, values, and drafts wherever the layout changes.
- Verify touch, pointer, and keyboard behavior supported by the target platform. Confirm that hover, focus, press, selected, and disabled states are distinguishable.
- Trigger a presentation from different source positions and resize it while open. Confirm a correct source relationship and an accessible exit.
- Cancel a press, interrupt a slider animation with a new adjustment, reopen a presentation, and change selection while an inspector is visible.
- Trigger loading, a stalled or failed operation, retry, cancel where safe, and completion. Verify the resulting data state separately from its animation.
- Test increased text size, RTL where supported, reduced motion, reduced transparency or the equivalent fallback, light and dark appearance, and contrast using the target platform's guidance.
- Inspect each grouped command's independent role, name, bounds, focus target, and activation. A visually connected group must not activate as one command.
- Save runtime evidence for the rendered product. Save export dimensions, frame rate, encoding, and playback evidence for offline motion. An implementation check or source read is insufficient for either claim.

## Scope boundaries for the eventual skill

Include a decision workflow, a small set of control and presentation contracts, state definitions, platform adapters, motion recipes, and verification guidance. Let the target project supply its product-specific tokens, assets, component system, and information architecture.

Do not turn the skill into a full catalog of Apple widgets, a branding preset, a universal Apple navigation mandate, or a dependency that every project must install. Do not promise a 1:1 Apple visual or physical match from public transcripts. Exact reproduction requires a pinned source and comparison evidence under the user's fidelity procedure.

Keep documented Apple behavior, recommended adaptation, implementation examples, and measured results distinct. Native SwiftUI APIs can be examples in a versioned Apple adapter. Portable equations and renderer mechanisms need their own evidence. Unbuilt examples must remain explicitly unverified.
