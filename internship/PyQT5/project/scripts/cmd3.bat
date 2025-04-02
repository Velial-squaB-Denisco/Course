@echo off
for /L %%i in (1,1,10) do (
  echo Step 3 - %%i
  timeout /t 1 >nul
)
