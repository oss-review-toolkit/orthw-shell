#!/bin/bash

cmd="$1"
lower_cmd="${cmd//-/_}"

location=$(dirname "${BASH_SOURCE}")

if [ -f "$location/command_template.py.tmpl" ]; then
    cat "$location/command_template.py.tmpl" | \
    sed -e "s,@@@command@@@,$cmd,g" \
    -e "s,@@@lower_command@@@,$lower_cmd,g" > "$location/$lower_cmd.py"
fi
