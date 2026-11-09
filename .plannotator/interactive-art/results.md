# Interactive art implementation

The standalone page is at `/home/maynkudu/Code/UI/interactive-art` and runs at
[interactive-art.localhost:1355](https://interactive-art.localhost:1355).
It stays local until the user creates a Components and UI repository. The Git
change contains the skill, reusable scene source, setup registration, and skill
catalog entry.

The [implementation review](review-decision.json) was approved with no changes
requested. Commit
[`384240a`](https://github.com/maynkudu/dotfiles/commit/384240af7908fe9972235d79e466d92142cfbe79)
was pushed to `origin/main`. The page remains local. This evidence directory is now included in the dotfiles publication.

The garden has growing lotus flowers, repeating day/night lighting, hover
bending, bounded dragging, spring return, keyboard actions, pause, time controls,
and PNG exports. The runtime separates scene time from fixed-step physics and
stops continuous work when paused, hidden, offscreen, or under reduced motion.

## Verified implementation

- [Desktop daylight](page-day.png), [night](page-night.png), and
  [held flower](page-pull.png), captured at 1200 by 1100 CSS pixels.
- [Mobile layout](page-mobile.png), captured at 390 by 844 CSS pixels with 2x
  device scale.
- [Downloaded artwork](exported-from-page.png), 1000 by 680 pixels.
- [Transparent plants](exports/plants.png), [full export](exports/whole.png),
  [reconstructed layers](exports/reconstructed.png), and
  [reconstruction difference](exports/difference.png).

The [supplied reference sheet](reference-sheet.png) informed the pointed,
overlapping petals, visible veins, dark contours, and ivory/violet palette.
This is original procedural artwork. Exact visual reproduction was not the
acceptance criterion and has not been established.

## Checks

The production build and strict TypeScript checks passed. The five existing
setup tests, repository and installed skill checks, and skill metadata validator
passed. The copy helper passed with and without the React example and refused
to overwrite an existing destination. The seven copied assets in the local page
matched the skill source.

[Page checks](page-checks.json) cover real mouse hover, extreme dragging, release,
keyboard activation, pause during dragging, growth/reset, repeating lighting,
independent physics speed, offscreen suspension, and live reduced motion.
[Cancellation evidence](cancellation.json) verifies the pointer-cancel handler
releases an actual captured pointer.

[Integration checks](integration-checks.json) cover visible keyboard targets on
mobile, independent instances, cleanup, saved-state restoration, repeated
mounting, hidden-tab suspension, and layer exports. The ten exported layers
reconstruct the full export with a maximum channel difference of 3 out of 255,
within the original tolerance. Plant-only exports contain transparent pixels.

[Startup checks](startup-checks.json) verify reduced motion starts without a
running frame loop and the still fallback loads. The final
[accessibility audit](accessibility.json) reports zero violations and zero
incomplete checks. [Browser errors](browser-errors.txt) is empty.

Physical touch dragging and scrolling remain unverified. Agent Browser's device
mode generated mouse input and reported zero touch points. Mobile layout and
keyboard checks do not establish touch behavior.

## Skill use

Invoke `$interactive-art` with the subject, visual references, host project, and
desired behavior. The skill guides artwork construction and uses the bundled
garden as a working example. Its helper copies editable TypeScript modules into
the host project. The runtime handles scheduling, input, resize, visibility,
export, and cleanup. Scene code owns geometry, growth, painting, and response.
The installed skill is available to Codex and Claude. A running scene needs no
AI service.
