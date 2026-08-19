@echo off
cd /d "%~dp0"
echo.
py checar_token.py
if errorlevel 1 (python checar_token.py)
echo.
pause
