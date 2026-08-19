@echo off
cd /d "%~dp0"
if "%~1"=="" (
  echo.
  echo  Arraste o arquivo .mp4 para cima deste arquivo.
  echo  A legenda sai do legenda.txt que estiver na mesma pasta do video.
  echo.
  pause
  exit /b
)
py publicar_reel.py "%~1"
echo.
pause
