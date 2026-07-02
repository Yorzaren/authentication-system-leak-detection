#!/bin/bash

# Launch the backends
gnome-terminal --title="Front-end: Website" -- uv run flask --app web run --debug &
FLASK_WIN_PID=$!

gnome-terminal --title="Local SMTP (Look here for breach emails)" -- uv run python -m aiosmtpd -n -l localhost:1025 &
SMTP_WIN_PID=$!

# Kill on close
cleanup() {
    echo ""
    echo "Closing backend windows..."
    kill $FLASK_WIN_PID $SMTP_WIN_PID 2>/dev/null
}
trap cleanup EXIT

# Start the interactive console
uv run python cmdline_driver.py