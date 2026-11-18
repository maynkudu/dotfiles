# Workflow contract evaluation

`agent-workflow-eval` runs small, sanitized event fixtures. It does not launch models, tools, servers or network requests and does not import private transcripts.

```bash
agent-workflow-eval
agent-workflow-eval --fixtures /path/to/explicit/fixtures
```

The bundled cases exercise questions staying read-only, narrow file scope, unavailable sources staying explicit, exact checkpoint bindings, stale context, lesson approval and commit authorization. Each case declares the expected violations, so both valid and invalid paths are tested.

Use these cases when changing rules, skill routing or event adapters. Add a focused case for a demonstrated failure rather than broad speculative suites. Maintain expected outcomes deliberately; do not change them just to pass a failing implementation.

The result is deterministic contract/checker evidence only. It does not establish live agent reliability, pass rates, token savings, cost or latency. Measuring those needs separately authorized representative runs with fixed tasks, capture conditions and human or independent graders.
