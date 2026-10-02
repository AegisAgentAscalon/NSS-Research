@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  python run.py replay --kind record_hop --seed 801
) else (
  py -3 run.py replay --kind record_hop --seed 801
)
set "RESULT=%ERRORLEVEL%"
echo.
echo Exit code: %RESULT%
pause
exit /b %RESULT%
