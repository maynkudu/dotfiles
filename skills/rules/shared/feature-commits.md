# Feature-based commits

When commits are authorized, make each commit one coherent feature or fix. Keep its required tests and documentation with it. Stage only that feature's files or hunks, inspect the staged diff and run its focused checks before committing. Use a message that names the feature or fix.

Keep unrelated completed work in separate commits rather than a catch-all commit before push. An inseparable dependency may stay in one commit; do not split working code merely to increase the count. Preserve user changes and leave unrelated files unstaged.

Permission to implement or approve a plan is not permission to commit or push. When the user requests review first, leave changes uncommitted until that review is approved.
