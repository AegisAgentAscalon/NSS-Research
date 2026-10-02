@echo off
setlocal
cd /d "%~dp0"
set PYTHONDONTWRITEBYTECODE=1
set OUT=..\NSS_HB002_verification_%RANDOM%_%RANDOM%
where py >nul 2>nul
if errorlevel 1 (
  python run.py verify --output "%OUT%"
) else (
  py -3 run.py verify --output "%OUT%"
)
set RESULT=%ERRORLEVEL%
echo.
echo Output: %OUT%
echo Exit code: %RESULT%
pause
exit /b %RESULT%
