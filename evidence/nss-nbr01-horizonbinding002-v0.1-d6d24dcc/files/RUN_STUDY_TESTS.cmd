@echo off
setlocal
cd /d "%~dp0"
set PYTHONDONTWRITEBYTECODE=1
where py >nul 2>nul
if errorlevel 1 (
  python run.py tests --output "%TEMP%\NSS_HB002_tests"
) else (
  py -3 run.py tests --output "%TEMP%\NSS_HB002_tests"
)
set RESULT=%ERRORLEVEL%
echo.
echo Exit code: %RESULT%
pause
exit /b %RESULT%
