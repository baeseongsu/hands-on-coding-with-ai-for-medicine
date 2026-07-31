#!/usr/bin/env bash
#
# Unlocks the workshop API key with the passphrase the instructor announces.
#
# The encrypted key ships with this repository; the passphrase never does.
# Decryption happens here in the Codespace and the key is never printed.
#
# If your instructor hands out the key itself instead of a passphrase, use
# set-api-key.sh.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENC_FILE="$SCRIPT_DIR/workshop-key.enc"

# shellcheck source-path=SCRIPTDIR
# shellcheck source=./store-key.sh
. "$SCRIPT_DIR/store-key.sh"

if [ ! -f "$ENC_FILE" ]; then
  cat >&2 <<'TEXT'
이 저장소에는 암호화된 key가 포함되어 있지 않습니다.

진행자에게 key를 직접 받은 뒤 아래를 실행하세요.

  bash .devcontainer/set-api-key.sh
TEXT
  exit 1
fi

printf '진행자가 알려준 passphrase를 입력하고 Enter를 누르세요.\n'
printf '입력하는 동안 화면에는 아무것도 표시되지 않습니다.\n\n'
printf 'Passphrase: '
IFS= read -rs passphrase
printf '\n'

if [ -z "$passphrase" ]; then
  echo "입력된 passphrase가 없습니다. 아무것도 저장하지 않았습니다." >&2
  exit 1
fi

if ! api_key="$(
  openssl enc -d -aes-256-cbc -md sha512 -pbkdf2 -iter 600000 -salt -base64 \
    -in "$ENC_FILE" -pass fd:3 2>/dev/null 3<<<"$passphrase"
)"; then
  echo "passphrase가 맞지 않습니다. 진행자에게 확인한 뒤 다시 시도하세요." >&2
  exit 1
fi

api_key="$(printf '%s' "$api_key" | tr -d '\r\n')"

# A wrong passphrase usually fails the padding check above, but garbage that
# happens to decrypt must not be written out as if it were a key.
case "$api_key" in
sk-*) ;;
*)
  echo "복호화된 값이 API key 형식이 아닙니다." >&2
  echo "이 메시지를 진행자에게 보여주세요." >&2
  exit 1
  ;;
esac

store_workshop_key "$api_key"
report_workshop_key_saved
