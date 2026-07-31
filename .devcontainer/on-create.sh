#!/usr/bin/env bash
#
# Runs once when the container is created.
#
# This is the only lifecycle step that GitHub Codespaces caches into a prebuild
# image, so every slow installation belongs here. Anything added to
# post-create.sh or post-attach.sh runs on the participant's clock instead.
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSHOP_VENV="$HOME/.virtualenvs/hands-on-medai"

run_privileged() {
  if command -v sudo >/dev/null 2>&1; then
    sudo "$@"
  else
    "$@"
  fi
}

# --- Coding agent CLI --------------------------------------------------------
# Installed unauthenticated. Participants supply a key with set-api-key.sh.
if ! command -v codex >/dev/null 2>&1; then
  npm install -g @openai/codex@latest
fi

# --- Python interpreter ------------------------------------------------------
python_bin="python3"
if ! command -v "$python_bin" >/dev/null 2>&1; then
  python_bin="python"
fi

if ! "$python_bin" -c "import ensurepip" >/dev/null 2>&1; then
  run_privileged apt-get update
  run_privileged apt-get install -y python3-venv
fi

# Resolve the interpreter to its real location before creating the virtual
# environment. Later in this script /usr/local/bin/python3 is replaced with a
# link into the virtual environment; if the venv itself pointed back at
# /usr/local/bin/python3 that would form a symlink loop.
python_real="$(readlink -f "$(command -v "$python_bin")")"

# --- Virtual environment -----------------------------------------------------
"$python_real" -m venv "$WORKSHOP_VENV"
# shellcheck disable=SC1091
. "$WORKSHOP_VENV/bin/activate"
python -m pip install --upgrade pip

python -m pip install -r "$REPO_ROOT/.devcontainer/requirements-base.txt"

# Each project declares its own dependencies in its own directory, but they are
# installed into this one shared runtime so participants never have to activate
# anything when moving between projects.
shopt -s nullglob
project_requirements=("$REPO_ROOT"/projects/*/requirements.txt)
shopt -u nullglob

if [ "${#project_requirements[@]}" -eq 0 ]; then
  echo "projects/*/requirements.txt 가 없습니다. 공통 패키지만 설치했습니다."
else
  for requirements_file in "${project_requirements[@]}"; do
    project_name="$(basename "$(dirname "$requirements_file")")"
    echo "$project_name 의 requirements 설치 중"
    python -m pip install -r "$requirements_file"
  done
fi

# --- Interpreter visibility --------------------------------------------------
# VS Code tasks and non-interactive shells do not read shell profiles. Link the
# virtual environment binaries into PATH so the same interpreter is resolved
# from anywhere, whether or not a profile was sourced.
for command_name in python python3 pip pip3; do
  if [ -x "$WORKSHOP_VENV/bin/$command_name" ]; then
    run_privileged ln -sf "$WORKSHOP_VENV/bin/$command_name" "/usr/local/bin/$command_name"
  fi
done

# --- Verification ------------------------------------------------------------
# Fail during the build rather than in front of a participant.
node --version
npm --version
codex --version
command -v python3
python3 --version
python3 -m pip --version

# The symlinks above are the whole point of this step, so confirm that a bare
# python3 really lands inside the virtual environment rather than in system
# Python. This catches a broken link or an overwritten PATH entry.
resolved_prefix="$(python3 -c 'import sys; print(sys.prefix)')"
if [ "$resolved_prefix" != "$WORKSHOP_VENV" ]; then
  echo "python3 가 $resolved_prefix 를 가리킵니다. 기대값은 $WORKSHOP_VENV 입니다." >&2
  exit 1
fi

echo "실습 환경 준비 완료. Python prefix: $resolved_prefix"
