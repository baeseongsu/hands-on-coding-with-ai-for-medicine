#!/usr/bin/env bash
#
# Shared helper for writing the workshop API key.
#
# Sourced by set-api-key.sh and unlock-key.sh so both entry points store the
# key in exactly the same place with the same permissions. Not meant to be run
# directly.
#

WORKSHOP_KEY_DIR="$HOME/.config/hands-on-medai"
WORKSHOP_KEY_FILE="$WORKSHOP_KEY_DIR/env"

store_workshop_key() {
  local key="$1"

  if [ -z "$key" ]; then
    echo "입력된 key가 없습니다. 아무것도 저장하지 않았습니다." >&2
    return 1
  fi

  case "$key" in
  *\'*)
    echo "key에 작은따옴표(')가 들어 있어 안전하게 저장할 수 없습니다." >&2
    echo "이 메시지를 진행자에게 보여주세요." >&2
    return 1
    ;;
  esac

  umask 077
  mkdir -p "$WORKSHOP_KEY_DIR"
  chmod 700 "$WORKSHOP_KEY_DIR"
  printf "export OPENAI_API_KEY='%s'\n" "$key" >"$WORKSHOP_KEY_FILE"
  chmod 600 "$WORKSHOP_KEY_FILE"
}

report_workshop_key_saved() {
  cat <<TEXT

저장했습니다. key는 이 저장소 밖에 보관됩니다.

  $WORKSHOP_KEY_FILE

새 터미널을 열면 바로 적용됩니다. 지금 이 터미널에서 쓰려면:

  . "$WORKSHOP_KEY_FILE"

그다음 coding agent를 실행하세요.

  codex

TEXT
}
