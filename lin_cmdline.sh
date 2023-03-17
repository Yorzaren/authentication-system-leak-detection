#!/usr/bin/env sh
if [ -d "venv/" ]; then
    . venv/bin/activate
fi
python3 cmdline_driver.py