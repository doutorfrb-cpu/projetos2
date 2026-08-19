@echo off
cd /d "%~dp0"
if "%~1"=="" (
  echo.
  echo  Arraste a imagem 9x16 para cima deste arquivo.
  echo  Ou rode:  py publicar_story.py caminho\da\imagem.png
  echo.
  pause
  exit /b
)
py publicar_story.py "%~1"
echo.
pause
