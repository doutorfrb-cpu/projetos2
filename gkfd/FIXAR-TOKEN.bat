@echo off
cd /d "%~dp0"
echo.
py fixar_token.py
if errorlevel 1 (python fixar_token.py)
echo.
pause
