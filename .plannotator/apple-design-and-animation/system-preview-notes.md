# Integrated system preview

The isolated [system-preview.html](system-preview.html) is a small Motion library interface. It demonstrates the proposed skill's combination of product hierarchy, adaptable layout, independent semantic controls, and existing motion mechanisms. It is an original portable adaptation, not an Apple reproduction or production application.

Open the self-contained HTML as a local file. No server, dependencies, Apple assets, remote requests, or installation are required. The original `../apple-motion/lab.html` remains unchanged.

## Design decisions

- The sidebar provides library and favorites navigation. The toolbar provides local search and a distinct export action. Presets, selected preview, and settings remain separate content regions.
- The sidebar becomes horizontal navigation when space narrows. The inspector moves below the preview. Selection and values remain in the same state objects.
- Grid and List are native single-choice radio controls. Favorite is an independent toggle button. Save and Restore are ordinary actions and are disabled until a value changes.
- Material is confined to the functional sidebar, toolbar, and view-choice controls. Content previews use flat fills. The view-choice container uses a 14 px radius, a 4 px inset, and 10 px inner radii.
- System fonts resolve on the host. The preview distributes no Apple fonts, symbols, or other assets. Plain labels avoid an icon dependency and all prohibited northeast arrows.
- The default preview is elastic brightness. The other two fixture entries reuse the existing predicted-snap and smooth-union examples. Only one selected mechanism appears at a time. No new motion model was added.

## Motion mechanism

Dragging brightness past either endpoint stretches its shell along the vertical axis around the opposite fixed edge. The shell contracts horizontally by the reciprocal scale. The stored brightness value remains clamped to 0 through 100. Release preserves the input velocity and springs the overshoot back to zero. A new drag interrupts the current spring.

The mechanism code comes from the fully read existing lab. Its exact underdamped step, rubberband function, velocity sampling, pointer capture, keyboard controls, resize handling, reduced-motion handling, and suspension behavior remain the source for this preview. Example tuning is omega 20 radians per second and damping ratio 0.85. These are portable example parameters, not measured Apple values.

## Evidence

- [Desktop screenshot](system-preview-desktop.png), 1360 by 1000 viewport.
- [Narrow screenshot](system-preview-narrow.png), 390 px viewport width. The inspector stacks below the preview. Computed document width equals viewport width, with no horizontal overflow.
- The narrow Export preset label initially wrapped. The action now refuses to shrink or wrap, while search uses the remaining width. The recaptured button is 40 px high and stays on one line.
- Agent Browser loaded the local file successfully. No JavaScript errors were reported by the browser error command during the initial focused pass.
- Keyboard ArrowUp changed brightness from 65 to 70. The preview slider, inspector slider, and numeric field all reflected 70. Save became available. Keyboard Enter on Save committed 70 to the session's saved preset state and displayed Saved.
- A real pointer drag past the upper brightness endpoint kept the value at 100, produced rendered overshoot of about -31.88 px and reciprocal shell scale of about 0.837 by 1.194. On release, overshoot and velocity returned to zero, dragging ended, and no animation frame remained pending. This checks the existing stretch and settle path, not high-speed fling behavior.
- Changing the browser's system reduced-motion preference while mounted activated the alternate path. The same pointer drag kept shell scale at 1 by 1 and rendered overshoot at zero, with no pending animation frame. The local Reduce motion checkbox also stopped pending animation work.
- Export preset opened the native dialog. Escape dismissed it and focus returned to the export trigger. The download action is implemented, but the downloaded file was not inspected during this pass.
- Keyboard Space selected List. The selected brightness preset and its current value survived the layout change.
- No JavaScript errors were reported after these interaction checks.

Source inspection and these focused checks do not establish Apple visual fidelity, a complete accessibility audit, frame-rate performance, high-speed fling or interruption timing, native-platform behavior, or offline-video export. Other fixture entries remain the previously verified mechanism examples from the original lab; this pass focused on integrated elastic brightness.

## Scope

Saved values and favorites live in this page session. Reloading restores the initial fixture. JSON export creates a local settings file. The preview does not render an offline movie, persist accounts or collections, synchronize data, implement a full application router, or provide a complete component library. These are deliberate preview boundaries.

Sources that changed the design are the existing lab, Apple HIG Layout and Toolbars, and WWDC25 sessions 356 and 323. Their evidence and portable interpretations are in `../apple-motion/research/design-patterns.md` and `../apple-motion/research/design-foundations.md`.
