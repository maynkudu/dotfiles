# Compatible with Bash and Zsh. Keep standard commands available under their names.
for dotfiles_bin in "$HOME/.local/bin" "$HOME/.bun/bin" "$HOME/.cargo/bin" "$HOME/.elan/bin" "$HOME/.local/share/fnm"; do
  [ -d "$dotfiles_bin" ] || continue
  case ":$PATH:" in
    *":$dotfiles_bin:"*) ;;
    *) export PATH="$dotfiles_bin:$PATH" ;;
  esac
done
unset dotfiles_bin

command -v nvim >/dev/null 2>&1 && export EDITOR=nvim
export VISUAL="${EDITOR:-vi}"

alias pn='pnpm'
alias pni='pnpm install'
alias pnd='pnpm dev'
alias pnb='pnpm build'
alias pnl='pnpm lint'
alias pnt='pnpm test'
alias pns='pnpm start'
alias buni='bun install'
alias bunr='bun run'
alias bund='bun dev'
alias bunb='bun run build'
alias gst='git status --short'
alias gd='git diff'
alias gpl='git pull'
alias gplr='git pull --rebase'
alias gp='git push'
alias gc='git commit'
if command -v eza >/dev/null 2>&1; then
  alias ll='eza -lah --git'
  alias lt='eza --tree --level=2'
else
  alias ll='ls -lah'
fi

# Do not alias codex, cd, cat, grep or find: scripts and CLI flags depend on them.
