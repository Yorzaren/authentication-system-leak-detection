@echo off
if exist venv/ (
  call venv/Scripts/activate
)
flask --app web run --debug