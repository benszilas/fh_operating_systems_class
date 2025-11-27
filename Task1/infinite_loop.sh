#!/bin/bash
set -e

if [[ -x $1 ]]; then
    while true ; do
        $1
    done
fi

echo "Usage: $0 [path_to_program]"
exit 1