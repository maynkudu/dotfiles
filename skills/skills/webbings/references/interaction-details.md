# Interaction details

Source 6 in [source notes](source-notes.md) names 20 techniques. Choose only those
that fit the actual component. The reel does not establish implementation code,
browser support or the behavior of the named companies' products. Check current
platform documentation when selecting an API and use a working fallback.

| Technique | Use when | Implementation and verification |
| --- | --- | --- |
| Skeleton loading | Content shape is predictable during a meaningful wait | Reserve space, preserve layout and communicate loading accessibly. Avoid a placeholder flash for already available content or endless decorative shimmer. |
| Optimistic updates | A mutation is safe to anticipate and recover | Track pending and failure, reconcile server results and roll back without losing a newer action. Payment or authorization success must not be invented optimistically. |
| Command menu | Frequent tasks benefit from search or keyboard access | Keep primary tasks available elsewhere. Check focus, Escape, search, empty results and return to the trigger. |
| Shortcut hints | Supported actions have useful shortcuts | Display accurate platform hints and keep ordinary input editing and assistive navigation intact. |
| Undo feedback | A real reversible operation benefits from recovery | Implement actual reversal and handle expiry or failure. Keep the action keyboard reachable and feedback perceivable; a toast alone does not make deletion reversible. |
| Stale-while-revalidate | Existing data can remain useful while refreshing | Communicate stale/error states when material, scope caches to the correct account and reconcile updates without erasing newer work. |
| Pre-rendering | A stable page or route can be prepared safely | Use the project's rendering strategy. Check freshness, hydration and privacy. Prefetch only justified routes and assets; avoid wasteful download of everything. |
| BlurHash or image placeholders | A dominant image has noticeable load time | Reserve the image's dimensions, provide a useful fallback and keep decoding/rendering cost bounded. A simple existing placeholder may be sufficient. |
| View transitions | A navigation or layout change benefits from continuity | Keep stable identity, focus, history, reduced-motion behavior and a static fallback. Verify support in the actual target. |
| Swipe-to-dismiss sheets | Touch dismissal is appropriate for a sheet | Handle distance, velocity, cancellation and scroll conflict. Provide a visible or keyboard-accessible dismissal path and preserve focus handling. |
| Interruptible animations | Input can change before motion settles | Follow motion-and-feedback.md and test repeated input and reversal. |
| Predictive back | The target platform supports a meaningful back preview | Preserve normal browser/platform history and cancellation. Do not imitate a native platform gesture by hijacking ordinary web navigation. |
| Hit slop | A small visible control needs a usable target | Expand the effective target without overlapping neighboring controls. Check pointer, touch and focus independently. |
| Safe area insets | Viewport cutouts or system controls affect fixed content | Account for the target's safe areas and viewport behavior. Test orientation, browser chrome and the onscreen keyboard where relevant. |
| One-time-code autofill | A supported authentication flow accepts a code | Use appropriate semantics and allow paste/autofill without blocking manual entry. Server expiry, attempt bounds and replay protection remain required. |
| Tabular numbers | Comparable numbers need stable columns | Apply the numeric-alignment guidance in ui-polish.md and inspect the actual font and localized values. |
| Balanced headlines | A short display heading wraps awkwardly | Tune wrapping with real content and supported CSS. Check narrow widths, zoom and localization; do not add brittle manual breaks across all viewports. |
| Continuous corners | An approved shape system uses them | Preserve component consistency, clipping and fallback rendering. Do not introduce a package or change the whole design merely to replace ordinary rounded corners. |
| Idempotency keys | Retried requests could duplicate an important operation | Enforce the same logical request on the server and reject inconsistent reuse. A disabled submit button is not a substitute. Test an applicable duplicate/retry path. |
| Safe pointer triangle | A cascading hover menu needs forgiving pointer travel | Keep a submenu open while the pointer moves toward it without making other items feel stuck. Verify keyboard, touch, Escape and focus behavior separately. |

Waiting, cancellation, retry, undo and confirmed completion are part of the
component. Implement the relevant states together and operate them before calling
the interaction complete. These are optional techniques with conditional checks,
not a requirement to add every feature to every site.
