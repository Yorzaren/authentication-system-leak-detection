@echo off
if exist venv/ (
  call venv/Scripts/activate
)
python cmdline_driver.py