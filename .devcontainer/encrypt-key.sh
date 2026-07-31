#!/usr/bin/env bash
#
# Instructor tool. Encrypts the workshop API key into workshop-key.enc so that
# the ciphertext can be committed and participants only need a passphrase.
#
# Run this on your own machine before the session, then commit the .enc file.
# The operating rules and their rationale are printed at the end of a
# successful run, so they reach the instructor at the moment they matter.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENC_FILE="$SCRIPT_DIR/workshop-key.enc"

# Plain reads rather than a helper with a nameref: macOS still ships bash 3.2,
# and `local -n` needs 4.3. This script runs on the instructor's own machine,
# so it has to work there.
printf '배포할 API key를 입력하세요 (화면에 표시되지 않음): '
IFS= read -rs api_key
printf '\n'

if [ -z "$api_key" ]; then
  echo "입력된 key가 없습니다. 아무것도 쓰지 않았습니다." >&2
  exit 1
fi

case "$api_key" in
sk-*) ;;
*)
  echo "OpenAI API key 형식이 아닙니다. 아무것도 쓰지 않았습니다." >&2
  exit 1
  ;;
esac

printf '수업에서 알릴 passphrase를 입력하세요 (화면에 표시되지 않음): '
IFS= read -rs passphrase
printf '\n'
printf 'passphrase 확인: '
IFS= read -rs passphrase_confirm
printf '\n'

if [ -z "$passphrase" ]; then
  echo "passphrase가 비어 있습니다. 아무것도 쓰지 않았습니다." >&2
  exit 1
fi
if [ "$passphrase" != "$passphrase_confirm" ]; then
  echo "두 passphrase가 일치하지 않습니다. 아무것도 쓰지 않았습니다." >&2
  exit 1
fi

printf '%s' "$api_key" | openssl enc -aes-256-cbc -md sha512 -pbkdf2 \
  -iter 600000 -salt -base64 -out "$ENC_FILE" -pass fd:3 3<<<"$passphrase"

# Prove the round trip here rather than in front of a room of participants.
decrypted="$(
  openssl enc -d -aes-256-cbc -md sha512 -pbkdf2 -iter 600000 -salt -base64 \
    -in "$ENC_FILE" -pass fd:3 3<<<"$passphrase"
)"
if [ "$decrypted" != "$api_key" ]; then
  rm -f "$ENC_FILE"
  echo "복호화 왕복 검증에 실패했습니다. 아무것도 쓰지 않았습니다." >&2
  exit 1
fi

cat <<TEXT

$ENC_FILE 를 생성했습니다.
방금 입력한 passphrase로 복호화 왕복까지 검증했습니다.

다음 단계:

  git add .devcontainer/workshop-key.enc
  git commit -m "chore: rotate the workshop key"

지켜야 할 두 가지:

  1. passphrase는 커밋하지 않습니다. 수업에서 구두나 슬라이드로만 알립니다.
     README, 커밋 메시지, issue 어디에도 넣지 않습니다.

  2. 수업이 끝나면 API key를 revoke합니다. 암호문은 공개 저장소 히스토리에
     영구히 남습니다. passphrase는 언젠가 새어나가므로, 그 시점에 key가 이미
     죽어 있어야 무해합니다.

이 방식은 전달 편의를 위한 것이지 보안 장치가 아닙니다. 수강생은 결국 자신의
Codespace에 평문 key를 갖게 됩니다. key를 직접 배포하는 것과 위협 모델이 같습니다.

TEXT
