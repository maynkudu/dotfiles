# VPS and headless hosts

Apply this when the user identifies a VPS or the target has no interactive desktop.
Check the target itself when running commands remotely. SSH alone does not establish
which capabilities are available. These rules override workstation prerequisites
and automatic installation fallbacks elsewhere in the dotfiles.

- Check the target's OS, architecture, package manager, permissions, available tools,
  memory and disk before setup or a large build. The Arch workstation's paths,
  installed packages and verification records do not describe another machine.
- Install only dependencies needed for the current task and supported by the host.
  Reuse existing runtimes, package managers and project environments. Prefer scoped,
  user-level installs. Do not install the workstation's full tool list, replace
  system runtimes or add global packages merely because a skill mentions them.
- Choose only the requested dotfiles setup phases. `python3 bin/setup --rules`
  installs rules without the tools phase. The default setup, `--tools` and `--mcp`
  are not VPS profiles and can add unnecessary packages or integrations. Inspect
  their actions before using them. Installing a skill does not require installing
  all the executables it documents. Leave existing packages intact unless removal
  is part of the task.
- Skip native desktop automation, local GUI apps, simulators and emulators when
  the target lacks their required session, platform or hardware. Do not add a
  desktop environment, Xvfb, VNC, GPU stack, browser download or mobile SDK just to
  satisfy a workstation workflow. A supported headless browser or document renderer
  remains useful when the task needs it. Check existing capabilities first and
  install a missing dependency only within the task's authorized scope.
- When a workflow cannot run here, report the missing capability once and continue
  with supported checks. Do not repeatedly retry or propose installing an
  inapplicable tool. Mark the specific verification gap. If Plannotator cannot be
  used, present the concrete plan or diff in chat and obtain any required approval
  there. Skipping the tool does not waive an approval requirement.
- Keep development previews on loopback. Reuse a working Portless route when
  available. If unavailable or unreachable from the user's machine, use an existing
  authenticated preview route or SSH tunnel and report the client-accessible URL.
  A VPS's `.localhost` name resolves on each client separately. Do not expose a
  public listener or change firewall, DNS or certificate trust just for a preview.
- Bound build parallelism, browser sessions, recordings and downloads to available
  CPU, memory and disk. Run only relevant checks. Reuse caches and remove only
  task-owned temporary files. Do not add background services or containers for
  optional tooling, or terminate another workload to free resources.
- Preserve SSH access, running services, reverse proxies, databases and mounted
  storage. Change their configuration, restart them, reboot or upgrade system
  packages only when the user's task authorizes that operation. Use credentials
  already provisioned for the target. Do not copy workstation secrets to a VPS
  merely to reproduce the local setup.
