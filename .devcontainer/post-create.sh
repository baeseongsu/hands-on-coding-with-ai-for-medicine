#!/usr/bin/env bash
#
# Runs once after the container is created.
#
# Confirms that the pre-installed environment survived into this container and
# makes it the default for interactive shells. Installation belongs in
# on-create.sh, which is the step Codespaces prebuilds.
#
set -euo pipefail

WORKSHOP_VENV="$HOME/.virtualenvs/hands-on-medai"

if [ ! -x "$WORKSHOP_VENV/bin/python" ]; then
  cat >&2 <<'TEXT'
환경 준비가 완료되지 않았습니다: 사전 설치된 Python 가상환경을 찾을 수 없습니다.

수강생: 설정을 직접 바꾸지 마시고, 이 메시지를 진행자나 조교에게 보여주세요.

진행자: 이 Codespace의 onCreateCommand 출력이나 해당 브랜치의 Codespaces
prebuild 결과를 확인하세요. 설치는 .devcontainer/on-create.sh에서 실행됩니다.
TEXT
  exit 1
fi

export VIRTUAL_ENV="$WORKSHOP_VENV"
export PATH="$WORKSHOP_VENV/bin:$PATH"

PROFILE_MARKER="hands-on-coding-with-ai-for-medicine environment"
PROFILE_SNIPPET="$(
  cat <<'TEXT'

# hands-on-coding-with-ai-for-medicine environment
WORKSHOP_VENV="$HOME/.virtualenvs/hands-on-medai"
if [ -d "$WORKSHOP_VENV/bin" ]; then
  export VIRTUAL_ENV="$WORKSHOP_VENV"
  export PATH="$WORKSHOP_VENV/bin:$PATH"
fi

# Workshop API key, if one was stored with .devcontainer/set-api-key.sh.
# The file lives outside the repository and is never committed.
WORKSHOP_KEY_FILE="$HOME/.config/hands-on-medai/env"
if [ -f "$WORKSHOP_KEY_FILE" ]; then
  . "$WORKSHOP_KEY_FILE"
fi
TEXT
)"

for profile in "$HOME/.bashrc" "$HOME/.zshrc"; do
  touch "$profile"
  if ! grep -qF "$PROFILE_MARKER" "$profile"; then
    printf '%s\n' "$PROFILE_SNIPPET" >>"$profile"
  fi
done

node --version
npm --version
python3 --version
python3 -m pip --version
codex --version
