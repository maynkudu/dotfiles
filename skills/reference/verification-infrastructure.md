## Agent workflow preferences

- Give agents the tools to close their own verification loop. A task is not done because the code
  compiles. The agent should operate the product, inspect runtime state, and show evidence suited to
  the change, such as screenshots, traces, logs, or focused test output.
- Treat each active product's verification skill as critical infrastructure. Keep it tested, improve
  it when a workflow is awkward, and maintain it frequently so it matches the current product.
- Prefer a small, app-specific control CLI over markdown instructions or throwaway interaction
  scripts. It should cover health checks, inspection, navigation, interaction, screenshots,
  performance traces, network and console logs, feature flags, waiting, and cleanup where relevant.
- Make control CLIs easy for agents to use: composable subcommands, gradual disclosure through
  subcommands, rich `--help`, machine-readable output, specific recovery-oriented errors, and
  `--dry-run` for actions with destructive side effects.
- Make the development environment reproducible. Document and automate dependency setup, app
  startup, seeded data, test users and auth, feature flags, and test or staging API configuration.
- Keep a searchable Feature Map beside the verification skill. Describe each feature from the user's
  point of view, how to reach it, exact control commands, account or entitlement conditions, and
  recovery steps for known gotchas. Link detailed feature files from a short index.
- Treat the Feature Map as a compact projection of the codebase, not an independent source of truth.
  Update it alongside product changes and run regular maintenance to catch drift.
- Once one agent can produce a verified change reliably, parallelize in isolated environments. Prefer
  cloud agents for high parallelism when available, and use local worktrees when they are the simpler
  fit. Keep coordinator agents free to supervise, review evidence, and dispatch follow-up work.
- Measure performance before and after a targeted change. Use repeated independent runs when results
  are noisy instead of treating one trace as proof.
- Reuse mature verification flows in routines and automations. Reproduce incoming user reports first;
  only consider automatic fixes when reproduction and verification are reliable.

