# Shared aliases and paths, with optional integrations loaded only when installed.
[[ -o interactive ]] || return
source "${DOTFILES_ROOT:-$HOME/dotfiles}/shell/common.sh"
HISTFILE="$HOME/.zsh_history"
HISTSIZE=50000
SAVEHIST=50000
setopt HIST_IGNORE_DUPS HIST_IGNORE_SPACE SHARE_HISTORY AUTO_CD
autoload -Uz compinit
compinit
bindkey -e
command -v fnm >/dev/null 2>&1 && eval "$(fnm env --use-on-cd --shell zsh)"
if command -v starship >/dev/null 2>&1; then
  eval "$(starship init zsh)"
else
  autoload -Uz colors && colors
  PROMPT='%F{cyan}%n%f %F{blue}%~%f %# '
fi
command -v zoxide >/dev/null 2>&1 && eval "$(zoxide init zsh)"
for plugin in zsh-autosuggestions zsh-syntax-highlighting; do
  plugin_path="$HOME/.local/share/dotfiles/zsh/$plugin/$plugin.zsh"
  [[ -r "$plugin_path" ]] && source "$plugin_path"
done
unset plugin plugin_path
(( $+functions[autosuggest-accept] )) && bindkey '^I^I' autosuggest-accept
# Untracked, machine-specific configuration and secrets belong here.
[[ -r "$HOME/.zshrc.local" ]] && source "$HOME/.zshrc.local"
true
