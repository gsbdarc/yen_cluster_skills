#!/usr/bin/env bash
# Link skills from this clone into the user-wide skill directories for Claude Code
# (~/.claude/skills) and Codex (~/.agents/skills).
#
#   ./install.sh                 # every skill (for Claude Code, except those in a plugin)
#   ./install.sh yen-slurm       # just the named skills, in a plugin or not
#   ./install.sh --dry-run ...   # show what would happen
#
# Skills in a plugin (.claude-plugin/marketplace.json) reach Claude Code through the
# plugin, as /<plugin>:<skill>, so a full run does not also link them into
# ~/.claude/skills. Codex has no plugin route for them and gets every skill.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_TARGET="$HOME/.claude/skills"
TARGETS=("$CLAUDE_TARGET" "$HOME/.agents/skills")
MARKETPLACE="$ROOT/.claude-plugin/marketplace.json"
DRY=0; PICKED=()

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY=1 ;;
    -h|--help) sed -n '2,11p' "$0"; exit 0 ;;
    --*) echo "unknown option: $arg" >&2; exit 2 ;;
    *) PICKED+=("$arg") ;;
  esac
done

picked() { local s; for s in "${PICKED[@]+"${PICKED[@]}"}"; do [[ "$s" == "$1" ]] && return 0; done; return 1; }

# One "<skill> <plugin>@<marketplace>" line per skill that ships in a plugin.
PLUGIN_OF=""
if [[ -f "$MARKETPLACE" ]]; then
  if command -v python3 >/dev/null; then
    PLUGIN_OF="$(python3 -c '
import json, sys
m = json.load(open(sys.argv[1]))
for p in m.get("plugins", []):
    for s in p.get("skills", []):
        print(s[2:] if s.startswith("./") else s, p["name"] + "@" + m["name"])
' "$MARKETPLACE")" || { echo "WARN   could not read $MARKETPLACE; linking plugin skills individually" >&2; PLUGIN_OF=""; }
  else
    echo "WARN   python3 not found; linking plugin skills individually" >&2
  fi
fi
plugin_of() { awk -v s="$1" '$1 == s { print $2 }' <<<"$PLUGIN_OF"; }

for dir in "$ROOT"/skills/*/; do
  name="$(basename "$dir")"
  [[ -f "$dir/SKILL.md" ]] || continue
  if (( ${#PICKED[@]} )) && ! picked "$name"; then
    continue
  fi

  plugin="$(plugin_of "$name")"

  for target in "${TARGETS[@]}"; do
    link="$target/$name"
    if [[ -n "$plugin" && "$target" == "$CLAUDE_TARGET" ]] && (( ! ${#PICKED[@]} )); then
      echo "skip   $link (part of ${plugin%@*}: claude plugin install $plugin)"
    elif [[ -L "$link" && "$(readlink -f "$link")" == "$(readlink -f "$dir")" ]]; then
      echo "ok     $link"
    elif [[ -e "$link" || -L "$link" ]]; then
      echo "WARN   $link exists and is not this skill; leaving it alone" >&2
    elif (( DRY )); then
      echo "would  ln -s $dir -> $link"
    else
      mkdir -p "$target"
      ln -s "${dir%/}" "$link"
      echo "linked $link"
    fi
  done
done

echo "Restart Claude Code / Codex if a newly linked skill does not appear."
