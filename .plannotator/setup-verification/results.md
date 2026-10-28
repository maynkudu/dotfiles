# Setup verification

Checked on 2026-10-28 on Arch Linux with Node 26.12.1, npm 12.2.1, and
LibreOffice 26.8.1.1.
The selected agents are Codex and Claude Code. The installed profile uses
maynkudu's identity and preserves the inherited writing and design preferences.

| Check | Result | Evidence |
| --- | --- | --- |
| Generated and installed rules, public skills | Passed | [Doctor output](doctor.log), [repository checks](repo-check.log) |
| Installer backups, dry run, repeated installation, shell preservation, version-specific tool patch | Four tests passed | [Tests](../../tests/test_setup.py), `python3 -m unittest discover -s tests -v` |
| Bash and Zsh startup | Passed | Both interactive shells loaded `pn`, `gst`, fnm, and doc-python with the configured history size; both syntax checks passed |
| Native dependencies | Passed | SQLite query, JavaScript parsing, PTY module loading, and Sharp PNG encoding |
| Agent Browser interaction | Passed | The test button changed from `Run check` to `Passed`; [screenshot](browser.png) |
| Webreel recording | Passed | [MP4](videos/setup-check.mp4), [config](webreel.config.json), [before](video-before.png), [after](video-after.png) |
| Video decoding and playback | Passed | H.264, 800 by 600, 233 frames, 3.883333 seconds; FFmpeg decoded without errors and browser playback reached `ended: true` |
| Document generation and extraction | Passed | [DOCX text](anydoc-docx.md), [PPTX text](anydoc-pptx.md), [XLSX cells](anydoc-xlsx.md), [PDF text](anydoc-pdf.md); Pandoc also exported a DOCX |
| PDF rendering | Passed | [Rendered page](pdf-preview.png) inspected |
| DOCX and PPTX rendering | Passed | One page each with the expected text; [Word preview](office/docx/preview-1.png), [slide preview](office/pptx/preview-1.png), [page and content checks](office/checks.json) |
| XLSX formula recalculation | Passed | Three formulas cached `13`, `42`, and `55` with no errors; [helper result](office/recalc.json), [value assertions](office/formula-values.json), [workbook](office/formulas.xlsx) |
| XLSX rendering | Passed | Both sheets inspected; [inputs](office/xlsx/preview-1.png), [results](office/xlsx/preview-2.png) |
| Argent MCP | Passed for discovery | Returned an empty running-device list and the available `Pixel_8` AVD |
| Agentation MCP and HTTP connection | Passed in a fresh process | Initialization followed by `agentation_list_sessions`; [result](agentation-check.json) |
| Portless proxy and HTTPS trust | Passed | [Diagnostics](portless-doctor.log), [TLS request](portless-tls.json); system certificate validation passed on the existing proxy at port 1355 |
| Implementation review | Approved | Plannotator returned [`decision: approved`](review-decision.json) with no changes requested |

The browser page and documents are small local test fixtures. They contain no
accounts, user documents, or external services. This verifies the installed
commands and their basic runtime paths.

Office exports used isolated temporary LibreOffice profiles. `anydoc` extracted
the expected text from each PDF, and all four rendered pages were inspected at
120 DPI. The spreadsheet check covered cross-sheet references and a dependent
formula. Reopening it with `openpyxl` and `data_only=True` returned the expected
cached values; a separate read confirmed the formulas remained intact.

The HTTPS request used the system trust store with curl configuration and CA
environment overrides disabled. The proxy returned its expected HTTP 404 for
the unregistered `dotfiles.localhost` hostname, with `ssl_verify_result: 0`.
This checks the existing proxy and certificate without starting an app server.

## Fixes included in the installer

npm 12 skipped the native dependency scripts in the earlier installation. The
installer now allows the required package scripts listed in `setup.toml`, with
Sharp using its bundled libvips. Existing native modules were rebuilt and checked.

Webreel 0.1.4 enabled manual browser frame control without issuing `beginFrame`.
Its screenshot request stalled, so FFmpeg received no images. An isolated copy
produced a recording after removing that flag. The installer now applies this
change only to the local `@webreel/core` 0.1.4, retaining a timestamped backup.
The installed CLI then produced the video linked above. The version guard,
dry-run behavior, and repeated application are covered by the installer test.

The fixture now uses the `videos` object documented in
[Webreel's configuration](https://webreel.dev/configuration), with a named flow
and a wait for the changed button text. Outputs live in this checkout because
Webreel 0.1.4 cannot rename its temporary video across filesystems.

The document launcher executes the environment's own Python binary, preserving
Python's virtual-environment detection. The setup guide records these fixes and
the commands needed to repeat installation.

## Remaining limits

- Portless reports four warnings about existing stale or inactive app routes.
- No device was booted or operated. Argent's device interaction and profiling
  remain unverified for a particular app.
- Agentation's per-app toolbar sync is unverified because this setup does not
  mount a toolbar in an application. Restart the agents to load the repaired
  native modules and fresh MCP processes.
- Ten historical skill names and the original private integrations are outside
  the installed public selection. Details are in the
  [setup guide](../../docs/setup.md).

The temporary Webreel copy, debug wrapper, and raw recording cache were removed.
The Agent Browser session and temporary Agentation process were closed.
No commit or push was made.

Plannotator returned `decision: approved` with no changes requested. The review
session and its isolated proxy were closed after approval.
