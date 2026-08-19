@echo off
cd /d "%~dp0"
echo.
py publicar_pendentes.py %*
if errorlevel 1 (python publicar_pendentes.py %*)
echo.
pause
