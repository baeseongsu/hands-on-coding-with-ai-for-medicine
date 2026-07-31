#!/usr/bin/env bash
#
# Stores the workshop API key for this Codespace, typed in directly.
#
# Use this when the instructor hands out the key itself. If the instructor
# announces a passphrase instead, use unlock-key.sh.
#
# The key is written outside the repository, readable only by the current user.
# It is never echoed and never enters shell history, which is why this exists
# instead of a plain `export` command.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source-path=SCRIPTDIR
# shellcheck source=./store-key.sh
. "$SCRIPT_DIR/store-key.sh"

printf '진행자가 알려준 API key를 붙여넣고 Enter를 누르세요.\n'
printf '입력하는 동안 화면에는 아무것도 표시되지 않습니다.\n\n'
printf 'API key: '
IFS= read -rs api_key
printf '\n'

store_workshop_key "$api_key"
report_workshop_key_saved
