#!/usr/bin/env sh
if [ -d "venv/" ]; then
    . venv/bin/activate
fi
flask --app web run --debug