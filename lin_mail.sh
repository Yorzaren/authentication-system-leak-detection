#!/usr/bin/env sh
if [ -d "venv/" ]; then
    . venv/bin/activate
fi
echo Do NOT exit this command.
echo You should receive the emails below here when they are sent:
python3 -m aiosmtpd -n -l localhost:1025