@echo off
setlocal
rem Wrapper para ejecutar el script PowerShell que inicia la API y abre /docs
set PS1=%~dp0run_and_open.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%" -ApiHost "127.0.0.1" -ApiPort 8000
endlocal
