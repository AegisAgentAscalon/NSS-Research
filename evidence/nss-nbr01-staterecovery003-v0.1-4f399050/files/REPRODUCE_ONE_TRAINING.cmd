@echo off
setlocal
cd /d "%~dp0"
set "OUT=%TEMP%\NSS_StateRecovery003_retrain_%RANDOM%_%RANDOM%"
echo Writing synthetic training reproduction to "%OUT%"
python -B tools\reproduce_one.py --output "%OUT%"
pause
