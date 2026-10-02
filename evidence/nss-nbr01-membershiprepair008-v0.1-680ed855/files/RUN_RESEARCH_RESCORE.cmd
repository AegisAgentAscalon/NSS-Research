@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (python run.py rescore) else (py -3 run.py rescore)
set "RESULT=%ERRORLEVEL%"
echo Exit code: %RESULT%
pause
exit /b %RESULT%
