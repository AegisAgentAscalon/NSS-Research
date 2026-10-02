@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (python run.py checks) else (py -3 run.py checks)
set "RESULT=%ERRORLEVEL%"
echo Exit code: %RESULT%
pause
exit /b %RESULT%
