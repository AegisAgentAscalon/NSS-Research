@echo off
setlocal
cd /d "%~dp0"
set "OUT=%TEMP%\NSS_StateRecovery003_verify_%RANDOM%_%RANDOM%"
echo Writing fresh verification to "%OUT%"
python -B tools\verify_results.py --output "%OUT%"
pause
