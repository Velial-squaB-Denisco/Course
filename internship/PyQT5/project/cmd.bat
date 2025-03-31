@echo off
set iter=0

:loop
set /a iter+=1
echo %iter%
timeout /t 1 >nul
goto loop
