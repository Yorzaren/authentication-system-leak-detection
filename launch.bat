@echo off
title Auth System Test

: Launch the backends
start "Front-end: Website" /min uv run flask --app web run --debug
start "Local SMTP (Look here for breach emails)" /min uv run python -m aiosmtpd -n -l localhost:1025

: Start the interactive console
uv run python cmdline_driver.py

: Kill on close
taskkill /FI "WINDOWTITLE eq Front-end: Website" /T /F
taskkill /FI "WINDOWTITLE eq Local SMTP (Look here for breach emails)" /T /F