# Modulo installation and access verification

All 76 checks passed against the actual Modulo route handlers and locally built protected manifests. The installed Shadcn 4.23.0 CLI installed `@modulo/elastic-slider`, `@modulo/snap-rail` and `@modulo/liquid-cluster` into separate temporary consumers.

| Component | Installed files | Download and installation hashes | Strict TypeScript | Anonymous denial | Revoked bearer and session denial |
| --- | --- | --- | --- | --- | --- |
| Elastic slider | 4 | Exact | Pass | 401 | 401 on next request |
| Snap rail | 4 | Exact | Pass | 401 | 401 on next request |
| Liquid cluster | 3 | Exact | Pass | 401 | 401 on next request |

Each component used a separately minted verification key. Active bearer requests and source sessions downloaded the protected manifest. Sessions reported unlocked. An invalid explicit bearer could not fall back to an active session. Revocation through the real mint handler denied the next bearer and existing-session requests, reported a locked session, and denied a new unlock attempt.

All 11 downloaded files exactly equaled their current local implementations. All installed files exactly equaled their downloads. Internal imports were relative or React imports. Each installed consumer passed strict TypeScript with DOM iterable types.

The consumer registry used `@modulo`, its named local origin, and the literal `Bearer ${MODULO_CHECK_KEY}` header placeholder. The actual key was supplied only in the CLI child environment. Passphrase, keys and cookie values stayed in memory. Logs contain no raw credentials.

`results.json` contains each assertion and all SHA-256 comparisons. The three `*-install.txt` files contain CLI output. `consumer-components.json` records the configuration with its environment placeholder. `server.ts` records the small harness and imports the real registry, mint and source-access handlers unchanged.

The Bun harness ran with Modulo as its working directory so `.private-registry` resolved to the real locally built manifests. The database and three consumers were created under this evidence directory. All three keys were revoked, the store was closed, and the temporary runtime directory was removed. The owned server stopped. No browser session was needed. The shared Modulo app and live database were unchanged.

The server reused the existing portless HTTP fallback at `http://modulo-install-check.localhost:1355`. The stop request lost its response because the server stopped immediately. Portless then returned 502 and Bun printed a directory-mismatch diagnostic during exit. The test response and saved results had already confirmed successful key revocation and runtime removal. A follow-up process check confirmed the owned command had exited.

This verifies local HTTP route-handler behavior and actual namespaced installation. The temporary consumers reused existing Modulo dependencies through a symlink. It does not establish fresh dependency resolution, remote private-repository access, published full-SHA pins, a fresh remote checkout, Next server rendering, or HTTPS cookie transport.

▶ http://modulo-install-check.localhost:1355 — modulo-install-check · Bun route handlers · portless HTTP fallback · stopped
