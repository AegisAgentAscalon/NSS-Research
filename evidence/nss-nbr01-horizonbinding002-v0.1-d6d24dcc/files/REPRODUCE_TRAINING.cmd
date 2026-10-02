@echo off
setlocal
cd /d "%~dp0"
set PYTHONDONTWRITEBYTECODE=1
set OUT=..\NSS_HB002_training_%RANDOM%_%RANDOM%
echo This prepares all 40 synthetic models. It does not change NSS or install software.
where py >nul 2>nul
if errorlevel 1 (
  python run.py train-all --steps 2400 --output "%OUT%"
) else (
  py -3 run.py train-all --steps 2400 --output "%OUT%"
)
set RESULT=%ERRORLEVEL%
echo.
echo Output: %OUT%
echo Exit code: %RESULT%
pause
exit /b %RESULT%
