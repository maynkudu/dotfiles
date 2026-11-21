# Named local servers

Before starting or exposing a long-running local server, read `~/dotfiles/skills/reference/portless.md`. It owns availability, deterministic naming, shared-process safety, announcement format and fallbacks.

Always operate local web apps through Portless at `https://<name>.localhost/`, with configured names taking precedence. Reuse the requested app's existing route and exact URL when it is already live. Do not use a direct localhost port, choose a random port, override Portless's assigned app port, or stop another process to free one. Announce the exact URL when ready and at closeout.

Prefer an existing Portless proxy and user-level commands. If Portless is unavailable, try its user-level invocation before installing globally. If the default HTTPS proxy cannot bind without elevation, try the documented unprivileged Portless fallback first and disclose its URL. Request the user's password through the host's secure credential prompt only when no unprivileged Portless option works and sudo is necessary. Never ask for a password in ordinary chat or expose it in command arguments, environment variables, or logs.
