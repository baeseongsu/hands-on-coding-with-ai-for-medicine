#!/usr/bin/env bash
#
# Runs every time a participant connects to the Codespace.
#
# Keep this fast. Anything slow placed here runs again on every reconnect,
# including after a browser refresh.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSHOP_VENV="$HOME/.virtualenvs/hands-on-medai"
KEY_FILE="$HOME/.config/hands-on-medai/env"

if [ -d "$WORKSHOP_VENV/bin" ]; then
  export VIRTUAL_ENV="$WORKSHOP_VENV"
  export PATH="$WORKSHOP_VENV/bin:$PATH"
fi

# Pick up instructor fixes published during the session, but never at the cost
# of a participant's uncommitted work.
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  current_branch="$(git branch --show-current || true)"
  if [ "$current_branch" = "main" ] && git remote get-url origin >/dev/null 2>&1; then
    git fetch origin main --quiet || true
    local_commit="$(git rev-parse HEAD || true)"
    remote_commit="$(git rev-parse origin/main || true)"

    if [ -n "$local_commit" ] && [ -n "$remote_commit" ] && [ "$local_commit" != "$remote_commit" ]; then
      if [ -z "$(git status --porcelain)" ]; then
        git pull --ff-only origin main --quiet || true
      else
        cat <<'TEXT'
저장소가 최신 main보다 뒤처져 있지만, 커밋하지 않은 변경이 있어 자동 업데이트를
건너뛰었습니다. 작업 내용은 그대로 남아 있습니다.
정리가 끝난 뒤 직접 `git pull origin main`을 실행하세요.
TEXT
      fi
    fi
  fi
fi

printf '\n실습 환경이 준비되었습니다.\n\n'

if [ -f "$KEY_FILE" ]; then
  cat <<'TEXT'
아래 명령으로 coding agent를 실행하세요.

  codex

TEXT
elif [ -f "$SCRIPT_DIR/workshop-key.enc" ]; then
  cat <<'TEXT'
한 단계 남았습니다. 진행자가 알려준 passphrase로 API key를 해제하세요.

  bash .devcontainer/unlock-key.sh

그다음 새 터미널을 열고 coding agent를 실행하세요.

  codex

TEXT
else
  cat <<'TEXT'
한 단계 남았습니다. 진행자가 준 API key를 저장하세요.

  bash .devcontainer/set-api-key.sh

그다음 새 터미널을 열고 coding agent를 실행하세요.

  codex

TEXT
fi
