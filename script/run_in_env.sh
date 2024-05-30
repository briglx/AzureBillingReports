#!/usr/bin/env bash
###################################################################
# Activate pyenv and virtualenv if present, then run the specified command
# Params
#
###################################################################

# Stop on errors
set -eu

printf 'Running %s with args %s\n' "$0" "$*"

# pyenv, pyenv-virtualenv
if [ -s .python-version ]; then
    PYENV_VERSION=$(head -n 1 .python-version)
    export PYENV_VERSION
fi

# other common virtualenvs
my_path=$(git rev-parse --show-toplevel)

if [ -f "${my_path}/venv/bin/activate" ]; then
  activate_path="${my_path}/venv/bin/activate"
  echo "Found environment in venv $activate_path"
  # shellcheck disable=SC1090,SC1091
  . "$activate_path"
fi

if [ -f "${my_path}/.venv/bin/activate" ]; then
  activate_path="${my_path}/.venv/bin/activate"
  echo "Found environment in .venv $activate_path"
  # shellcheck disable=SC1090,SC1091
  . "$activate_path"
fi

exec "$@"
