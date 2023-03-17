@echo off
if exist venv/ (
  call venv/Scripts/activate
)
echo Do NOT exit this command.
echo You should receive the emails below here when they are sent:
python -m aiosmtpd -n -l localhost:1025