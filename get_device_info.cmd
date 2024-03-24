@echo off


SET mypath=%~dp0

py -3.6 -V

if %errorlevel% equ 0 (
  py -3.6 "%mypath%\pycl.py"
) else (
  py -3 "%mypath%\pycl.py"
)




echo Press any key to exit...



pause >nul