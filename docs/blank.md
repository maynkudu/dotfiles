# BLANK access

The `blank` command connects this setup to the registry and inspiration directory
at https://ui.aryank.space. The shared `blank-direction` skill documents the same
workflow for Codex and Claude. Setup installs shadcn 4.23.0 and links the helper.

Both credentials supplied in `~/dotfiles/kiys` were verified on 2026-10-28.
The passphrase opened the inspiration directory. The registry token unlocked
component source and returned a catalog containing 368 items.

## Credentials

`kiys` remains the credential source. It is excluded from Git and has mode `600`.
The helper reads its `Registry token` and `Passphrase` entries when needed. It
does not copy their values into agent rules, shell startup files, project files,
or command arguments. Keep the file in place, or set `BLANK_KEYS_FILE` to another
existing file with the same fields and permissions.

The registry token goes to curl through stdin or to the shadcn child process
through `BLANK_REGISTRY_TOKEN`. The inspiration passphrase goes to the browser
through stdin. Browser cookies and state are not exported by the helper.

## Find references and inspect source

```bash
blank registry-search 'scroll text' --section components
blank search 'scroll driven gallery'
blank catalog
blank source cell-portrait
```

`registry-search` uses two to four task keywords and searches `components`, `pages`,
`backend`, or `all` through `/registry/search`. `search` uses a short task phrase
with `/direction/discover` for joint registry and inspiration discovery.
Catalog and source authenticate with
the supplied registry token. The source command returns the registry item's JSON,
including its source files, without creating a project or installing a component.

## Add the registry to an app

In an app with an existing shadcn `components.json`:

```bash
blank configure .
blank shadcn view @compronents/cell-portrait
blank shadcn add @compronents/cell-portrait
```

`blank configure` merges the following entry alongside the app's existing
registries and leaves unrelated values intact:

```json
{
  "@compronents": {
    "url": "https://ui.aryank.space/r/{name}.json",
    "headers": {
      "Authorization": "Bearer ${BLANK_REGISTRY_TOKEN}"
    }
  }
}
```

The placeholder is intentional. `blank shadcn` supplies its value for that
invocation. An existing conflicting `@compronents` entry is reported for review.
Use the normal shadcn initialization workflow if the app has no `components.json`.
There is no reason to initialize shadcn in this dotfiles repository.

The [registry's setup guide](https://ui.aryank.space/docs) and
[shadcn's authentication documentation](https://ui.shadcn.com/docs/registry/authentication)
describe the named registry and environment-variable mechanism. The source URL
alone does not attach shadcn's authorization header.

## Search enforcement

`skills/bin/install` adds the BLANK gate to agents selected in `setup.toml`.
Codex and Claude are the default targets. Grok, Pi and OpenCode adapters are
available when selected. The gate requires a search before supported edits,
installs and browser opens. UI edits also require inspecting matching components
and installing a fit, or inspecting returned inspiration sources when none fits.
Server edits require a backend search and source inspection.

Search failures count as attempts. Failed source reads and installs do not count
as success. The gate allows bounded recovery when repeated searches return no
references. See the [skill](../skills/skills/blank-direction/SKILL.md) for commands
and recovery. Runtime progress contains counts and source identifiers, without
credentials or raw responses. Tokens remain in the user-managed `kiys` file.

## Open the inspiration directory

```bash
blank inspiration --session blank-manual --headed
```

This opens a visible browser, submits the passphrase through the normal form,
and waits for the unlocked page. Agents should use their own session name and
can omit `--headed`. Further commands use the same session:

```bash
agent-browser --session blank-manual snapshot -i
agent-browser --session blank-manual close
```

Close the session when finished. The helper can authenticate a fresh session on
the next visit without saving browser state.

## Limits and verification

Python's default HTTP client received Cloudflare error 1010 because the site
blocked its browser signature. That response did not invalidate the token.
The normal browser and curl paths authenticated successfully. The helper uses
those verified paths and does not retry the blocked client.

The public recommendation endpoint has also reported unavailable reranking while
still returning ranked matches. Authentication does not repair that remote feature.

This integration supplies live BLANK discovery, source access, and browser login.
It does not include the original separate 129-skill design pack or historical
BLANK MCP servers. See the [verification record](../.plannotator/blank-access/results.md)
for the installed commands and checks.
The [gate verification record](../.plannotator/blank-direction-d4f2eeb/results.md)
covers the enforced workflow and installed hooks. Start a new Codex or Claude
session to load the updated global rules and hooks.
