@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  python run.py verify
) else (
  py -3 run.py verify
)
set "RESULT=%ERRORLEVEL%"
echo.
echo Exit code: %RESULT%
pause
exit /b %RESULT%
