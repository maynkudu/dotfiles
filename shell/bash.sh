[[ $- == *i* ]] || return
source "${DOTFILES_ROOT:-$HOME/dotfiles}/shell/common.sh"
HISTSIZE=50000
HISTFILESIZE=100000
HISTCONTROL=ignoreboth
shopt -s histappend
command -v fnm >/dev/null 2>&1 && eval "$(fnm env --use-on-cd --shell bash)"
command -v starship >/dev/null 2>&1 && eval "$(starship init bash)"
command -v zoxide >/dev/null 2>&1 && eval "$(zoxide init bash)"
[[ -r "$HOME/.bashrc.local" ]] && source "$HOME/.bashrc.local"
true
