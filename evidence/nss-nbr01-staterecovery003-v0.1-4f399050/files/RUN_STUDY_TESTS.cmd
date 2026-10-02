@echo off
setlocal
cd /d "%~dp0"
python -B -m unittest discover -s tests -v
if errorlevel 1 goto done
python -B tools\verify_manifest.py
:done
pause
