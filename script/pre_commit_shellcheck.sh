#!/usr/bin/env bash
###################################################################
# Run shellcheck on passed in files.
# Needed to ensure .config file is loaded
#
# Params
#   Files. path to one or more json files separated by spaces
###################################################################

# Stop on errors
set -e

printf 'Running %s with args %s\n' "$0" "$*"
for i do
    if ! shellcheck -x "$i"; then
        echo "Shellcheck failed."
        exit 1
    fi
done
