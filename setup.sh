#!/usr/bin/env bash
# setup.sh - get this workspace ready on a Mac.
#
# Usage:   ./setup.sh
#
# 1. Clones every repo in repos.txt that is not here yet, into the folder name given there.
#    A folder that already exists is only checked, never changed.
# 2. Creates _handoff/.
# 3. Registers the workspace with git bulk as "xzibit" (needs: brew install git-extras).
# 4. Lists what still has to be set up by hand on this machine.
#
# Safe to run again at any time: it never deletes, pulls or changes an existing repo.

set -euo pipefail

WS="$(cd "$(dirname "$0")" && pwd)"
cd "$WS"

echo "Workspace: $WS"
echo

# 1. Clone missing repos
while read -r name url _; do
  case "$name" in ''|'#'*) continue ;; esac

  if [ -d "$name/.git" ]; then
    origin="$(git -C "$name" remote get-url origin 2>/dev/null || echo "none")"
    if [ "$origin" = "$url" ]; then
      echo "OK     $name"
    else
      echo "CHECK  $name: origin is $origin, repos.txt says $url"
    fi
  elif [ -e "$name" ]; then
    echo "CHECK  $name exists but is not a git repo. Left as it is."
  else
    echo "CLONE  $name"
    git clone "$url" "$name" < /dev/null
  fi
done < repos.txt

# 2. Scratch folder (git-ignored)
mkdir -p _handoff

# 3. git bulk
echo
if ! git bulk --listall >/dev/null 2>&1; then
  echo "NOTE   git bulk not found. Run: brew install git-extras, then ./setup.sh again"
elif git config --global --get bulkworkspaces.xzibit >/dev/null 2>&1; then
  echo "OK     git bulk workspace 'xzibit' already registered"
else
  git bulk --addworkspace xzibit "$WS"
  echo "OK     git bulk workspace 'xzibit' registered"
fi

# 4. By hand on this machine
cat <<'EOF'

Still to do by hand on this machine (never in git):
  - WhipIT: scripts/.env and scripts/.env.dev
  - Axis-UI-Testing: npm install, then .env or the Keychain entry (service axis-ui-testing)
  - Axis-UI-Reference: npm install
  - Nightly test run: MacBook only. Never run npm run nightly:on on the Mac mini
EOF