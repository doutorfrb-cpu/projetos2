@echo off
cd /d "%~dp0"
py postar.py %*
if errorlevel 1 (py -3 postar.py %*)
echo.
pause
