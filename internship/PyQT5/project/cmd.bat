@echo off
set iter=0

:loop
set /a iter+=1
echo %iter%
ping 127.0.0.1 -n 2 >nul
goto loop