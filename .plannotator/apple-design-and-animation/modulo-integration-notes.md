# Modulo integration decision

Add three independent registry components, each backed by its own private source repository. Keep the platform-independent skill and recipes in the planned `apple-design-and-animation-system` project. Modulo gets React demonstrations of those mechanisms. Reuse its existing catalog, page shell, private source sync and mint-key installation flow.

This is a revised implementation plan, not authorization to commit, push, publish or deploy. No Modulo files were changed during this inspection.

## Independent modules

| Registry slug | Private repository | Minimum installable files | Contract |
| --- | --- | --- | --- |
| `elastic-slider` | `maynkudu/modulo-elastic-slider` | `ElasticSlider.tsx`, `create-elastic-slider.ts`, `elastic-slider.css` | Horizontal or vertical bounded slider. `min`, `max`, `step`, controlled or uncontrolled value, change and commit callbacks, label and disabled state. Only the shell stretches beyond bounds. Content remains outside its transform. |
| `snap-rail` | `maynkudu/modulo-snap-rail` | `SnapRail.tsx`, `create-snap-rail.ts`, `snap-rail.css` | Ordered labeled detents, current selection and selection callback. Release selects the nearest detent to the projected endpoint. Re-grab preserves the offset. A new destination retargets from current position and velocity. |
| `liquid-cluster` | `maynkudu/modulo-liquid-cluster` | `LiquidCluster.tsx`, `create-liquid-cluster.ts`, `liquid-cluster.css` | Labeled items with stable IDs and independent native button targets. A decorative proximity mask merges the shapes behind those targets. Labels and hit regions retain their shape. |

Each module owns its small math and lifecycle helpers. Use relative internal imports and scoped CSS. No cross-module registry dependency or import from Modulo's app utilities is needed. React is the host prerequisite. The proposed implementation needs no additional animation, Canvas or gesture package. Any icon dependency must be declared if used inside an installable component. Demo-only icons can use Modulo's existing Rune Icons.

Use client entry points for the React controls and a DOM runtime with `update`, `snapshot` and `destroy` behind each wrapper. Infer controller types from the factory. Keep source files independent of Next.js, Modulo's sound store, page CSS and catalog. Controlled and uncontrolled props should be an explicit union rather than an ambiguous optional value bag. Require sorted finite detents and finite slider bounds at the public boundary.

Count slider steps from `min`, not from zero. Use the same normalized bounded value for the fill, semantic attributes and callbacks. Define continuous change separately from one successful user commit. Pointer cancellation must end capture and settle geometry without committing a selection. Disabled controls must reject pointer, keyboard and assistive input. On re-grab, measure or read current presentation once, retain the grab offset and cache static geometry until resize.

Adapt the original [mechanism proof](/home/maynkudu/dotfiles/.plannotator/apple-motion/lab.html). Preserve seconds and px/s in the runtime, stale-sample rejection, pointer capture/cancel/lost capture, latent raw overshoot through the capped rubberband map, current-position re-grab and motion-preference hot changes. The proof's `omega = 20 rad/s`, `zeta = 0.85` and projection decay `8/s` are example tuning, not Apple constants.

The proof's LiquidCluster panel is insufficient by itself. It has decorative A/B labels and one separation range. The module must add independent native click targets and a real selection action. Start with geometric smooth-union Canvas masking and optional CSS translucency. Describe it as a geometric or glass adaptation. It does not implement Apple's glass renderer, refraction, physical surface tension or a fluid simulation. A renderer failure must leave the native buttons usable.

## Public integration

Affected tracked paths in Modulo:

- `.gitignore`. Add `/src/registry/elastic-slider/`, `/src/registry/snap-rail/` and `/src/registry/liquid-cluster/` before any implementation file is copied there. Preserve the existing private-manifest, public registry and environment ignores.
- `components.lock.json`. Add three private repository entries only when real published revisions exist. Each needs a full lowercase 40-character SHA and a SHA-256 checksum for every source file and required build asset.
- `src/lib/catalog.ts`. Add three `RegistryItem` definitions, `catalogItems` entries, usage snippets and API rows. Map `src/registry/<slug>/<file>` to `components/<slug>/<file>`. Use `registry:component` for entry points, `registry:lib` for runtimes and `registry:file` for CSS. Declare dependencies and registry dependencies explicitly, even when empty.
- `src/app/components/elastic-slider/page.tsx`, `src/app/components/snap-rail/page.tsx` and `src/app/components/liquid-cluster/page.tsx`. Follow Nilkamal's server page with metadata, structured data, breadcrumbs, Preview, Installation, API, `InstallCommand`, `ComponentMediaLinks` and `ComponentSource`.
- `src/components/elastic-slider-demo.tsx`, `src/components/snap-rail-demo.tsx` and `src/components/liquid-cluster-demo.tsx`, plus corresponding demo CSS modules where necessary. These contain public controls and examples, not original implementation files. Use the existing page and control shell. Keep the shell's type and layout conventions while giving the component its own scoped styling.
- `src/components/full-view.tsx`. Add three imports and views. Its exhaustive `Record<ComponentName, () => ReactNode>` derives its keys from the catalog. Omitting these entries breaks typechecking and the existing View full action. Add scoped full-view layout styling only if the current wrapper requires it.
- `scripts/component-media-preview.tsx` and `scripts/build-component-media.ts`. Add deterministic mount/replay cases and capture specifications for each control. The current capture script imports every module and applies full-scene dimensions. Put control demonstrations in a capture wrapper rather than stretching the actual slider to the viewport.
- `public/media/<slug>.jpg`, `.gif` and `.mp4` for each component. Generate only the selected new component, using the existing `--component` option, so unrelated media stays intact.
- `registry.json`. Regenerate its metadata and paths after source and media are ready. It must not contain source `content` fields. Add brief README installation entries if needed.

No new source route, auth table, token type, package manager migration or access framework is needed. Gallery, component index, sitemap, metadata helpers and `/r/[name]` allowlisting already derive from `catalogItems`. `next.config.ts` already includes ignored private manifests in `/r/*` tracing.

## Local preparation and publication boundary

After revised plan approval, prepare the source in separate local module directories outside the public app, with no commits or remotes required. Add the ignore rules before copying matching local files into Modulo for preview. Prepare component pages, catalog changes, capture cases, checksums and a clearly marked lock-entry draft in task artifacts. Do not put fake revisions or uncommitted hashes in the production lockfile.

Local preview checks can use the ignored local implementation. The existing sync script checks only lock entries, so a locally successful build before the new entries are pinned does not prove fresh-checkout reproducibility. Keep that gap explicit. Do not redesign sync or bypass its checksum checks to hide it.

The final publication approval must explicitly cover creating the three named private GitHub repositories and committing and pushing the reviewed source to them. Verify repository visibility, then use each actual `git rev-parse HEAD` and file checksums to finalize the three lock entries. Give the existing `MODULO_COMPONENTS_TOKEN` read-only Contents access to those repositories if it uses selected-repository scope. Change the existing Vercel Production and Preview secret only if the token itself changes. Never retain or print credentials.

Once the private pins exist, run normal source sync and verify a fresh checkout can build. A public Modulo commit, push or deployment also needs the user's explicit instruction. Plan approval alone does not authorize those publication actions.

## Necessary checks

1. Verify source paths are ignored with `git check-ignore`, and `git ls-files -- src/registry/<slug>/ .private-registry/ public/r/` returns no implementation or manifest files. Verify each new remote remains private. Check the final lock has valid full SHAs, complete file lists and matching checksums.
2. Exercise slider bounds and step rounding in both orientations, pointer hold before release, capture cancellation, keyboard changes and a controlled value change during interaction. Exercise snap velocity projection, detent edges, re-grab, retarget, cancel, resize and one-detent input. Exercise LiquidCluster's separate click targets, keyboard activation, merging and separating geometry, labels and renderer fallback.
3. Check preference changes while mounted, inactive frame-loop stoppage, hidden and offscreen states, unmount/remount cleanup and two simultaneous instances. Each component owns and cleans up its own frames, listeners, captures, observers and finite replay timers.
4. Generate and inspect each new JPG, GIF and MP4. Run `bun run components:sync`, selected `bun run media:build --component <slug> --dry-run` and generation, `bun run registry:build`, `bun run lint`, `bun run typecheck`, `bun run verify:access` and `bun run build`. The registry builder requires all listed media files to exist before it writes manifests. Report pre-existing failures separately from the new modules.
5. Operate the anonymous public preview on desktop and mobile, keyboard and reduced motion. Verify anonymous source denial, active-key browser unlock and a real `@modulo/<slug>` Shadcn install into a disposable consumer for each module. Confirm all targets and relative imports work outside Modulo. Revoke verification keys and confirm the next source request is denied. The existing access script covers download checks for every catalog item but its browser-session and revocation examples target Nilkamal, so perform those focused checks for the new modules without changing access infrastructure.
6. After private publication, verify authenticated source sync and production build from a fresh checkout. Review the final public diff for source leakage and unrelated edits before any authorized public publication.

## Verified state and source references

The initial status contained unrelated changes to `components.lock.json`, `registry.json`, `src/lib/catalog.ts`, `src/app/components/2048/page.tsx` and the three 2048 media files. A later read-only status was clean. This agent made no Modulo changes. Recheck status at implementation start and preserve the user's current work. No tracked files were found under `src/registry/`, `.private-registry/` or `public/r/`. The three proposed slugs are absent from the inspected catalog and lock. Their proposed local directories do not yet exist. Remote slug availability, token permissions and deployed behavior were not checked.

- [Module workflow](/home/maynkudu/Code/Projects/modulo/AGENTS.md:11). Private original sources, ignore-before-copy, pinned revisions, public previews and required install checks.
- [Lock schema and sync](/home/maynkudu/Code/Projects/modulo/scripts/sync-components.ts:14). Full SHA validation, file hashes, modified-file refusal and existing token/gh access.
- [Nilkamal page](/home/maynkudu/Code/Projects/modulo/src/app/components/nilkamal/page.tsx:1), [demo wrapper](/home/maynkudu/Code/Projects/modulo/src/components/nilkamal-demo.tsx:1) and [independent entry point](/home/maynkudu/Code/Projects/modulo/src/registry/nilkamal/Nilkamal.tsx:1). Server page, public controls, relative runtime imports and owned cleanup.
- [Catalog definitions](/home/maynkudu/Code/Projects/modulo/src/lib/catalog.ts:66) and [catalog entries](/home/maynkudu/Code/Projects/modulo/src/lib/catalog.ts:157). Registry file targets, media requirements and derived surfaces.
- [Full-view map](/home/maynkudu/Code/Projects/modulo/src/components/full-view.tsx:19). Additional integration requirement beyond the module checklist.
- [Registry builder](/home/maynkudu/Code/Projects/modulo/scripts/build-registry.ts:9), [source route](/home/maynkudu/Code/Projects/modulo/src/app/r/[name]/route.ts:8) and [source gate](/home/maynkudu/Code/Projects/modulo/src/components/component-source.tsx:1). Existing private manifests, live authorization and client-only source loading.
- [Media specifications](/home/maynkudu/Code/Projects/modulo/scripts/build-component-media.ts:51) and [capture entry point](/home/maynkudu/Code/Projects/modulo/scripts/component-media-preview.tsx:1). Selected-component generation and interactive capture cases.
- [Access verification](/home/maynkudu/Code/Projects/modulo/scripts/verify-access.ts:65). Catalog-wide source checks and the separate Nilkamal session/revocation path.
- [Installed route guide](/home/maynkudu/Code/Projects/modulo/node_modules/next/dist/docs/01-app/01-getting-started/15-route-handlers.md:1), [page convention](/home/maynkudu/Code/Projects/modulo/node_modules/next/dist/docs/01-app/03-api-reference/03-file-conventions/page.md:1), [client boundary guidance](/home/maynkudu/Code/Projects/modulo/node_modules/next/dist/docs/01-app/01-getting-started/05-server-and-client-components.md:140) and [metadata boundary](/home/maynkudu/Code/Projects/modulo/node_modules/next/dist/docs/01-app/03-api-reference/04-functions/generate-metadata.md:116). Read before recommending the server page/client control split and retaining request-time source authorization. Only the relevant sections of the longer client and metadata guides were read.

## Individual implementation inspection

Nuxt UI's requested `main` raw URL returned 404. GitHub reports the current default branch as `v4`. Its [DashboardSidebar source](https://github.com/nuxt/ui/blob/f4f284c6c6d5c4c3087f76b7bfb4b0bb3621cdd7/src/runtime/components/DashboardSidebar.vue) and [useResizable implementation](https://github.com/nuxt/ui/blob/f4f284c6c6d5c4c3087f76b7bfb4b0bb3621cdd7/src/runtime/composables/useResizable.ts) were read end to end. The sidebar keeps collapsed state, presented size and its mobile overlay separate. The resize implementation reads current element width on press, caches the rem conversion for the gesture, handles side and RTL sign, clamps semantic size and restores the previous expanded size. Adopt current-presentation sampling and explicit axis/sign mapping. Keep this plan's Pointer Events capture and owned cleanup instead of copying its document mouse/touch listeners. Reject persistence, collapse thresholds and mobile overlays for these small controls. They serve a sidebar, not the module contracts here. No installed Nuxt dependency is proposed.

The old GPUI Component repository now redirects to `longbridge/gpui-kit`. The [unstyled slider implementation](https://github.com/longbridge/gpui-kit/blob/f45cfeede9aac977cd8896fd63448f86e6a655c0/crates/base/src/slider.rs), including its tests, and the [styled component](https://github.com/longbridge/gpui-kit/blob/f45cfeede9aac977cd8896fd63448f86e6a655c0/crates/component/src/slider.rs) were read end to end. Behavior and visual chrome are separate. Values snap on the grid counted from `min`; the thumb percentage recomputes from the stepped value. Disabled pointer and accessibility paths stay inert. Gesture identity prevents another drag from taking an active thumb. A release event requires an actual interaction. The styled layer uses `hovered || pressed` for its spring-driven ring, avoiding a hover flicker while dragging. Adopt the semantic/visual step agreement, separate change/commit paths, disabled-input checks, gesture ownership and separation of behavior from styling. Do not add range or logarithmic modes merely because that slider supports them. Do not infer Apple spring tuning from its theme token or claim its native interaction has been operated here.

These reads changed the proposed slider contract and checks. Step rounding must be relative to a nonzero minimum, all outputs must share the bounded stepped value, and cancellation must be distinguished from a successful commit. A pressed state may retain feedback after hover is lost. They reinforce the independent runtime boundary already proposed. The public page shell remains Modulo's existing design.

Pinned source evidence:

| Local artifact | Revision | SHA-256 |
| --- | --- | --- |
| `nuxt-source.vue` | `f4f284c6c6d5c4c3087f76b7bfb4b0bb3621cdd7` | `fd1c400ab4791fbb4b933032f7631b1ef8a70f824829f04dec8895b97e6d9b35` |
| `nuxt-source-resizable.ts` | `f4f284c6c6d5c4c3087f76b7bfb4b0bb3621cdd7` | `1ca301458e4069a5836bdc035fbda4d9f4f19eddd0d8b5acedeb4e5858723246` |
| `gpui-source.rs` | `f45cfeede9aac977cd8896fd63448f86e6a655c0` | `c243ec7cefdb1d5749a916a74f68d1083212102acc5d93dd668b783afb68110a` |
| `gpui-source-component.rs` | `f45cfeede9aac977cd8896fd63448f86e6a655c0` | `16ef911bd5001f68a52fe8d7d899baf9b589548cce50d96f37f36beaf9f9e5f1` |

Artifacts are next to these notes. This inspection verifies source content and mechanism, not browser or native operation. Context7 Nuxt UI results are in `nuxt-ui-ctx7.txt`. No broad additional catalog search or Modulo mutation was performed.
