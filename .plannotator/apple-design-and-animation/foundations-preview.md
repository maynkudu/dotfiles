# Design foundations

Read this chapter when establishing or changing hierarchy, typography, layout, shapes, color, materials, or interaction density. Keep the user's product, brand, accepted references, and existing component system as the design inputs. Apply Apple guidance where it improves those decisions.

This chapter draws on Apple HIG pages captured on 2026-11-09 and WWDC25 sessions. Documented guidance describes Apple's platforms. Adaptations below apply that reasoning to other apps, websites, and motion graphics. Examples are proposed applications, not verified implementations. Check current platform documentation when choosing an API or relying on operating-system behavior.

## Establish hierarchy before styling controls

Separate the main content, navigation, commands for the current view, and tools for the selected object. Decide which information and action matter to the current task. Express those relationships through reading order, alignment, grouping, and progressive disclosure before assigning blur, shadows, or animation.

[HIG Layout](https://developer.apple.com/design/human-interface-guidelines/layout), Visual hierarchy, recommends ordering content by importance and grouping related information. Its latest captured change is 2026-09-09. [WWDC25 Get to know the new design system](https://developer.apple.com/videos/play/wwdc2025/356/), 08:55 to 09:50, explains hierarchy through layout and functional grouping. A shared background associates commands while each command remains independently operable.

For example, in a photograph editor, keep collection navigation separate from the selected photograph's exposure controls. Place collection export with collection commands. Give the export action suitable prominence without making every nearby control equally prominent. Keep the photograph title, preview, metadata, and tools associated when the layout reflows.

## Make typography survive content and text-size changes

Choose text roles such as title, body, secondary information, and control label. Distinguish them through size, weight, leading, and color. Test the actual content, including long labels, multiple lines, and enlarged text. Preserve relative importance when text grows. Scale meaningful icons with their labels where needed.

[HIG Typography](https://developer.apple.com/design/human-interface-guidelines/typography), Using system fonts and Supporting Dynamic Type, describes semantic text styles, continuous dynamic optical sizing, and adaptive layouts. Its latest captured change is 2025-12-16. Apple's current system font interpolates optical designs and adjusts tracking with point size. Use the supported font API rather than imposing a universal SF Text/SF Display cutoff or copying mockup tracking values into every renderer.

For other platforms, choose the incumbent or suitable licensed font. Use optical sizing only when that font and renderer support it, then inspect the result. Browser system-font stacks can resolve to different fonts on different operating systems. Font similarity does not establish matching metrics.

Use native text enlargement where available. Dynamic Type applies to iOS, iPadOS, tvOS, visionOS, and watchOS. The HIG explicitly states that macOS does not support Dynamic Type. Other platforms need their own text enlargement behavior. Custom fonts must support the accessibility behaviors relevant to that platform.

For example, an exposure row can show its label, slider, and value inline at ordinary sizes. At larger text sizes, move the label above the controls and let the row grow. Preserve the value and its units instead of shrinking the type to retain the original row height.

Use platform APIs for Apple system fonts. [HIG Typography](https://developer.apple.com/design/human-interface-guidelines/typography) directs apps not to embed system fonts. The [Apple fonts page](https://developer.apple.com/fonts/) includes font licenses restricting embedding and use beyond the stated Apple-platform mockup grant. Use licensed assets for portable output. Ship no Apple font files with this skill or its examples.

## Adapt layout to the available space

Choose layout from available width and height, text scale, input mode, and platform conventions. Respect safe areas for important text and controls. Decorative artwork can extend farther when that helps the composition. Preserve task state and intentional content groups when columns collapse or navigation changes form.

[HIG Layout](https://developer.apple.com/design/human-interface-guidelines/layout), Adaptability and Size classes, says to determine layout by available size classes rather than device type or orientation, and to preserve functionality as space changes. The portable adaptation is to derive breakpoints from where the content and controls fit. A narrow desktop window still needs appropriate desktop behavior.

For example, a wide editor can show collection navigation, photographs, and an inspector together. In a narrow view, show one main step with a clear return path. Retain the selected collection, photograph, query, and edited values. Enlarged text may require this simpler arrangement even when the viewport width has not changed.

Use the project's spacing scale or values extracted from an approved source. These sources establish no universal Apple 8-point grid or fixed 16-point margin. An exact reproduction needs pinned values and comparison evidence.

## Derive nested geometry from its container

[WWDC25 Get to know the new design system](https://developer.apple.com/videos/play/wwdc2025/356/), 03:21 to 04:44, distinguishes fixed shapes, capsules, and concentric shapes. Capsules use half the container height as their radius. Concentric shapes subtract padding from the parent's radius. The session also describes optical adjustments when mathematical centering looks unbalanced.

For a simple uniform inset, derive the inner radius from the outer radius and inset. If a card's padding changes, recalculate its artwork radius. Treat invalid or negative results explicitly. Nonuniform insets and unusual shapes require their own geometry. This relation does not specify Apple's continuous corner renderer.

Use capsules where their touch-friendly shape or prominence helps. Keep compact controls suitable for dense work. The same session retains rounded rectangles for smaller macOS controls and reserves capsules for larger or standout desktop actions. An inspector does not need the proportions of a phone's primary action.

## Assign semantic colors and material roles

Define colors by purpose, including primary and secondary text, backgrounds, grouping, separators, interactive accents, status, and selection. Keep each meaning consistent. Communicate important state through a label, shape, or other cue alongside color.

[HIG Color](https://developer.apple.com/design/human-interface-guidelines/color), System colors, advises using semantic system colors through APIs because literal values can change. Best practices covers light, dark, and increased-contrast variants. Its latest captured change is 2025-12-16. On other platforms, resolve the same roles through the project's theme system and verify the resulting combinations. Apple's RGB tables do not create automatic adaptation in a web palette.

Choose materials according to their role and foreground legibility. [HIG Materials](https://developer.apple.com/design/human-interface-guidelines/materials), Liquid Glass and Standard materials, separates floating functional controls and navigation from the content layer. Its latest captured change is 2025-09-09. Standard materials can organize content. Liquid Glass is used sparingly for functional elements, with a documented transient exception for interactive elements such as a slider thumb. [WWDC25 Meet Liquid Glass](https://developer.apple.com/videos/play/wwdc2025/219/), 13:24 to 13:44, warns against stacking glass on glass.

For example, leave a photograph grid in the content layer. A floating navigation bar can use an appropriate material if labels remain readable over scrolling photographs. Related buttons can share a visual treatment while retaining separate labels, hit regions, and focus targets.

Prefer regular native glass for varied backgrounds or substantial text. Clear glass is for visually rich media backgrounds. Current HIG Materials recommends considering a dark dimming layer of 35% opacity when the underlying content is bright. It says extra dimming is unnecessary when the background is sufficiently dark or standard AVKit controls already provide it. This updates the simpler WWDC25 explanation. Apply the condition rather than an unconditional overlay.

Native Liquid Glass includes adaptive lensing, shadows, tint, and motion. Portable blur and translucency reproduce only selected properties. Use a custom adaptation when it serves the task, verify contrast against relevant background states, and provide a readable opaque or less transparent fallback. Tint should identify meaningful emphasis, such as the primary action, rather than give every control equal emphasis.

## Size targets for the input and preserve accessible meaning

Choose comfortable interaction bounds and spacing for the actual input mode. Visible icon bounds and interaction bounds can differ, provided targets remain unambiguous and independently operable. Use platform guidance instead of transferring one phone dimension to every product.

[HIG Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), Mobility, separates default and minimum control sizes. The captured iOS and iPadOS table lists 44x44 pt as the default and 28x28 pt as the minimum. macOS lists 28x28 pt and 20x20 pt. Those are platform points, not universal CSS pixel targets. The page's latest captured change is 2025-06-09. Prefer the comfortable recommended size over the published minimum when space allows.

Keep names, roles, values, and independent targets understandable when effects are disabled. Provide supported keyboard and assistive input, alternatives to gestures, and discernible focus and state cues. Evaluate text and nontext contrast using the target platform's accepted standard and actual combinations. The HIG's point-size contrast table is not a replacement for web accessibility thresholds.

Honor enlargement, reduced motion, reduced transparency, and contrast preferences where available. Apple's native materials handle several preferences automatically. Portable controls need explicit alternatives. Reduced motion can keep direct manipulation while reducing bounce, automatic repetition, depth travel, and blur transitions. Preserve the same operation and resulting state.

## Keep platform differences intentional

| Context | Preserve | Adapt |
| --- | --- | --- |
| Touch apps | Content relationships, names, current state, and task continuity. | Reachability, comfortable targets, gesture alternatives, native navigation, and text-size behavior. |
| Desktop and web | The same content model and command meaning. | Window resizing, density, pointer and keyboard behavior, platform menus, and browser links and history where applicable. |
| TV and spatial apps | Selection, focus meaning, and readable content. | Viewing distance, focus growth, control spacing, comfortable depth and motion, and the platform's interaction model. |
| Motion graphics | Object identity, information hierarchy, state sequence, and legible labels. | Composition for the export dimensions, pacing, captions or descriptions, and playback. A video has no live targets or accessibility tree. |

Use consistent icon meaning, optical weight, and alignment. [HIG Icons](https://developer.apple.com/design/human-interface-guidelines/icons), Best practices, supports small optical adjustments for asymmetric icons. For this user's work, Rune Icons is the default for new apps. Preserve an existing icon system for narrow changes. Use plain labels when a symbol is ambiguous. The northeast or up-right arrow is prohibited in text, SVG, icon libraries, CSS, images, and rotated forms.

[HIG SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) documents version availability, trademark restrictions, and restrictions on Apple product symbols. Vector export capability does not establish cross-platform distribution rights. Those rights and current downloadable font-package licenses were not verified in this research. Use permitted assets instead of making them prerequisites for Apple-inspired design.

## Verify the chosen foundation

Check the representative composition at the relevant smallest and largest layouts, enlarged text, long content, and supported reading directions. Operate its important controls using the supported input modes. Inspect contrast and material legibility over actual background states. Check accessible names, values, focus, and preference alternatives separately from visual effects.

For a motion export, inspect the final frames and playback at the requested dimensions. Report only the behavior and appearance actually checked. Unimplemented adaptations, proprietary rendering details, and missing comparisons remain unverified.
