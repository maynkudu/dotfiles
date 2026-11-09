# Apple design foundations research

Retrieved on 2026-11-09. This is research for an agent skill usable across Apple apps, other apps, websites, and motion graphics. It records official guidance and proposed adaptations separately. No app, browser, simulator, or rendered implementation was operated in this research task.

## Recommendation

Build a decision system around content hierarchy, adaptive layout, semantic roles, legible typography, coherent shapes, and purposeful interaction. Route to the relevant platform before choosing fonts, controls, materials, or motion. Apple's current design language is a useful source for those decisions, but its operating-system behavior, supplied artwork, and licenses do not automatically transfer to other platforms.

Keep the primary skill short. Load foundations for typography, layout, color, shapes, iconography, accessibility, and platform adaptation. Load pattern references for actual navigation and component decisions. Load motion references for transitions, direct manipulation, spring behavior, and material effects. Require evidence appropriate to each medium before claiming that an implementation works.

## Typography

Official guidance comes from [HIG Typography](https://developer.apple.com/design/human-interface-guidelines/typography), particularly Ensuring legibility, Conveying hierarchy, Using system fonts, Using custom fonts, Supporting Dynamic Type, and Platform considerations. The latest listed change is 2025-12-16.

Use size, weight, and color to express information hierarchy. Preserve that hierarchy when text size changes. Prefer readable weights for small text, and use few typefaces. Apple supports custom fonts, provided they remain legible and implement the relevant text-size and accessibility behaviors.

Apple's current system fonts use continuous optical sizing. The Using system fonts section says, "With dynamic optical sizes, you don't need to use discrete optical sizes unless you're working with a design tool that doesn't support all the features of the variable font format." The source uses typographic apostrophes in the original. Do not prescribe a universal SF Text/SF Display cutoff or one tracking table for every runtime. It also says, "In a running app, the system font dynamically adjusts tracking at every point size."

Use platform font APIs for Apple's built-in fonts. The same section explicitly says, "don't embed system fonts in your app or game." Downloaded font files are not webfont assets. The [Apple fonts page](https://developer.apple.com/fonts/) contains San Francisco and San Francisco Compact license overlays. Section 2.B says, "You may not embed the Apple Font in any software programs or other products." It also restricts non-Apple UI mockups and artwork or website content beyond its stated grant. Those displayed licenses have narrow Apple-platform mockup permissions. The license bundled with each current downloadable font package was not inspected, so do not infer a broader permission for SF Pro or New York packages.

Portable adaptation. Use the incumbent or appropriate licensed font for the product. A browser system-font stack can use the user's installed system font without distributing Apple's files. On non-Apple systems it will resolve differently. If a chosen licensed variable font supports optical sizing, use its actual capabilities and inspect the result. Do not assume that its metrics, tracking, or optical designs match SF.

Dynamic Type is Apple's text-size mechanism for iOS, iPadOS, tvOS, visionOS, and watchOS. The macOS section says, "macOS doesn't support Dynamic Type." Built-in text styles provide Apple-specific hierarchy and scaling behavior. Custom implementations must handle their platform's text enlargement and bold-text preferences explicitly.

At large text sizes, stack constrained inline content, reduce columns, grow rows, scale meaningful icons, and minimize truncation. A successful font change requires rendered or computed evidence, including overrides. The published Apple point-size tables are platform references. They are not universal CSS pixel tokens.

## Layout and spatial hierarchy

[HIG Layout](https://developer.apple.com/design/human-interface-guidelines/layout) has sections Visual hierarchy, Adaptability, Size classes, Guides and safe areas, and Platform considerations. Its latest listed change is 2026-09-09.

Place important content early in the reading order, using leading and trailing directions for localization. Alignment implies relation. Indentation implies subordination. Group related content with space, container shapes, or separators, and use progressive disclosure when secondary choices make the main task harder to find. Preserve the same information grouping as layouts expand or contract.

The Size classes section says, "Determine layout based on size classes, not device type or orientation." The portable decision is to use actual available space, text size, input mode, and platform conventions. Width alone does not describe every layout constraint. Preserve functionality while changing what is immediately visible, such as exposing secondary actions on larger windows.

Respect safe areas for critical content and controls. Artwork can extend beneath functional bars where the platform supports that treatment. Do not let decorative background extension distort foreground text or controls. Preview the smallest and largest relevant layouts, enlarged text, long localization, and right-to-left layout.

No universal Apple 8-point grid or fixed 16-point margin was established by these sources. Use the actual platform component or approved reference values. On web and other platforms, establish spacing from content relationships and the incumbent system rather than calling invented values Apple tokens.

## Shapes and concentric corners

[WWDC25 session 356, Get to know the new design system](https://developer.apple.com/videos/play/wwdc2025/356/) provides the mechanism at 03:21 to 04:44. At 03:27 it says, "By aligning radii and margins around a shared center, shapes can comfortably nest within each other." At 03:42 to 03:59 it distinguishes fixed radii, capsules, and concentric shapes. "Capsules use a radius that's half the height of the container." "And concentric shapes calculate their radius by subtracting padding from the parent's." The original transcript uses typographic apostrophes.

For a simple uniform inset, the portable geometric relation is inner radius = outer radius minus inset. This is a geometry relation, not a complete description of Apple's continuous corner rendering. Nonuniform padding, minimum valid radii, variable shapes, and optical offsets need explicit treatment. The session says views are mathematically centered when appropriate and subtly offset when optical balance requires it.

The same session gives capsules a strong role in touch layouts but limits them in dense desktop environments. At 04:15 to 04:32, capsules are for standout actions on desktop, while macOS Mini, Small, and Medium controls retain rounded rectangles for compact layouts. Do not make every control a capsule or derive a universal corner radius from a phone screenshot.

Apple's runtime concentric shape API and fallback radius are implementation options on supported platforms. A CSS or SVG implementation needs its own explicit geometry and rendered checks. No proprietary curve, corner algorithm, or pixel equivalence was established here.

## Semantic color and contrast

[HIG Color](https://developer.apple.com/design/human-interface-guidelines/color) covers Best practices, Inclusive color, System colors, Liquid Glass color, and platform-specific roles. Its latest listed change is 2025-12-16.

Give each color role a consistent meaning. Status, interactivity, and decoration must remain distinguishable. Use labels, shapes, or other cues alongside color. For Apple apps, prefer semantic system colors and respect their intended roles. The System colors section says, "Avoid hard-coding system color values in your app." Published RGB values can change with releases and environment. A separator color is not a text color, and a secondary label color is not a background.

The Best practices section says, "Make sure all your app's colors work well in light, dark, and increased contrast contexts." It also directs Liquid Glass apps to provide light and dark variants even when the app otherwise ships in a single appearance. Apple's system colors and native material behavior handle adaptations that a static web palette does not.

Portable adaptation. Define semantic roles for primary and secondary text, backgrounds, grouping, separators, interactive accents, status, and selection. Resolve them for the supported themes and contrast preferences. Test the actual foreground/background combinations, including moving or colorful content beneath translucent controls. Do not paste Apple's system-color RGB tables into a portable palette and claim automatic adaptation.

[HIG Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), Vision, says to strive for minimum contrast standards and discusses WCAG and APCA. Its Accessibility Inspector table is Apple-specific guidance and is not a replacement for the accepted web standard. Use the applicable text-size and weight thresholds, including nontext controls, rather than simplifying this to one universal ratio or borrowing Apple's point-size table as CSS pixels.

## Materials and Liquid Glass

[HIG Materials](https://developer.apple.com/design/human-interface-guidelines/materials), Liquid Glass and Standard materials, is the current decision source. Its latest listed change is 2025-09-09. [WWDC25 session 219, Meet Liquid Glass](https://developer.apple.com/videos/play/wwdc2025/219/), explains the visual and behavioral system with timed demonstrations.

Use Liquid Glass to distinguish functional controls and navigation from content. The HIG says, "Don't use Liquid Glass in the content layer." Standard materials can separate content within that layer. The documented exception is a transient interactive element in a control such as a slider or toggle. Use custom glass effects sparingly. WWDC25-219 at 13:24 also says, "always avoid glass on glass." Use fills and vibrancy for elements inside the same material rather than stacking independent glass effects.

Regular glass is the broadly applicable variant. It adjusts background blur and luminosity for foreground legibility. Clear glass is for visually rich media backgrounds. Current HIG guidance is conditional. "If the underlying content is bright, consider adding a dark dimming layer of 35% opacity." "If the underlying content is sufficiently dark, or if you use standard media playback controls from AVKit that provide their own dimming layer, you don't need to apply a dimming layer." The original uses a typographic apostrophe.

This updates the simpler WWDC25-219 guidance at 14:27 to 15:04, which describes clear glass as needing dimming and lists three conditions. Prefer the newer HIG condition over an unconditional 35% overlay. The HIG's 35% value is guidance for that material and context, not proof that a portable glass approximation passes contrast checks.

Liquid Glass is a runtime system of adaptive layers, lensing, shadow changes, materialization, tint, and interaction behavior. A blurred translucent CSS rectangle reproduces only some visible properties. On platforms with Apple's material APIs, use the supported system components and verify their native behavior. Elsewhere, label custom effects as adaptations and implement only what helps the task, with a legible fallback. No proprietary shader or exact material implementation was recovered.

Use tint to emphasize primary actions or meaningful status, rather than coloring every control. Preserve monochromatic controls over busy colorful content where that improves contrast. Standard material thickness also has a semantic tradeoff, with more opacity supporting finer text and less opacity preserving background context.

## Iconography and rights

[HIG Icons](https://developer.apple.com/design/human-interface-guidelines/icons), Best practices, says, "Maintain visual consistency across all interface icons in your app." Match size, detail, stroke or weight, and perspective. Match adjacent text weight where appropriate. Optically center asymmetric icons with small asset or layout adjustments. Use labels when a symbol's action is ambiguous. Provide accessible names. Keep meaning consistent across platforms while respecting localization and reading direction.

[HIG SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) documents symbol availability, rendering modes, weights and scales, variants, animation, and custom symbols. Availability depends on the target operating-system version. SF Symbols' three scales relate to the cap height of SF. That is not evidence that arbitrary SVG icons align with arbitrary fonts automatically.

The HIG prohibits symbols or confusingly similar images in app icons, logos, and other trademarked use. Its Custom symbols section says, "Don't design replicas of Apple products." Symbols depicting Apple products and features can have individual restrictions and cannot be customized. Inspect those restrictions rather than assuming every symbol is interchangeable.

The additional [official SF Symbols page](https://developer.apple.com/sf-symbols/) describes vector export and editing but does not publish a cross-platform license grant in its page content. Its download points to a macOS DMG. The package and its bundled license were not downloaded or inspected. Technical export capability is not evidence of permission to distribute symbols in web products, non-Apple apps, or motion graphics.

Task-specific choice. Use Rune Icons by default for new apps, preserve an existing icon system for narrow changes, and never use the northeast or up-right arrow in text, SVG, libraries, CSS, images, or rotated forms. These are user constraints, not claims about Apple's HIG. Map established action meanings to the permitted icon set, and use plain labels when needed. Distribute no Apple font or symbol files in the skill.

## Accessibility and platform adaptation

The latest listed HIG Accessibility change is 2025-06-09. Its Vision, Mobility, Speech, Cognitive, and visionOS sections require text enlargement, alternatives to color and sound, accessible descriptions, keyboard access, alternatives to gestures, playback control, and support for relevant assistive technologies. The Vision section recommends allowing at least 200% text enlargement, or 140% in watchOS. Layout and typography must grow with the text.

The Mobility table explicitly separates default and minimum control sizes. For iOS and iPadOS it lists 44x44 pt as the default and 28x28 pt as the minimum. For macOS it lists 28x28 pt and 20x20 pt. For tvOS it lists 66x66 pt and 56x56 pt. For visionOS it lists 60x60 pt and 28x28 pt. For watchOS it lists 44x44 pt and 28x28 pt. Therefore 44 pt is not Apple's universal minimum, and these values do not automatically become CSS pixel targets. Prefer the comfortable recommended target for the input mode and include spacing, rather than selecting the smallest published minimum.

Reduce Motion needs an actual alternate behavior. HIG Accessibility, Cognitive, recommends reducing repetitive motion, tightening springs, tracking movement directly with gestures, avoiding animated depth changes, replacing spatial transitions with fades, and avoiding animated blur changes. WWDC25-219 at 18:22 to 18:48 says native Liquid Glass automatically responds to Reduced Transparency, Increased Contrast, and Reduced Motion. Reduced Motion disables its elastic properties. Portable implementations must explicitly implement and verify equivalent preference handling where available.

Keep the app's task, grouping, selection state, and core behavior consistent across platforms. Change presentation to suit the platform. WWDC25-356 at 16:35 to 17:22 describes shared component anatomy and core interactions across components with different forms. Examples include navigation presented as a tab bar or sidebar and selection menus with a common indicator, icon, label, and accessory anatomy. Preserve that meaning without imposing phone reachability rules on desktop, desktop density on touch, or immersive depth on ordinary reading content.

For motion graphics, apply these principles to hierarchy, readability at the final export size, pacing, semantic transitions, safe areas, and color management. Native accessibility APIs are not capabilities of a video file. Provide appropriate captions or descriptive alternatives, avoid unnecessary flashing and peripheral motion, and inspect the exported frames and playback. Do not use downloaded Apple fonts or icons as general-purpose graphics assets without a verified grant.

## Evidence and limits

Raw Apple DocC JSON, flattened source text, URLs, retrieval timestamps, and SHA-256 hashes are in `design-foundation-sources/`. Existing WWDC HTML and timed transcripts remain in `apple-primary-sources/`. `design-foundation-sources/selected-excerpts.json` records decisive original quotations, section names, and exact source paths. `design-foundation-sources/manifest.json` records dates and provenance.

Context7 resolved Apple HIG and returned relevant official excerpts. The first dedicated SF Symbols lookup instead matched a third-party wrapper. Recovery through Apple HIG succeeded. No quota failure occurred. BLANK returned no registry match for the foundations query, and discovery reported unavailable reranking. Parent research already inspected relevant third-party animation sources. Those sources are not evidence for Apple's fonts, licenses, platform metrics, or native material behavior.

Official text and source relationships were read. Proposed portable adaptations were not implemented or visually verified. The private corner renderer, optical interpolation algorithm, adaptive material thresholds, and shader implementation remain unknown. SF Symbols cross-platform distribution rights and current downloadable font-package licenses remain unverified. The skill should preserve these boundaries rather than converting guesses into fixed rules.
