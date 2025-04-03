@echo off
for /L %%i in (1,1,10) do (
  echo Step 1 - %%i
  ping 127.0.0.1 -n 2 >nul
)
