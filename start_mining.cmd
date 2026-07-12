@echo off
SETLOCAL DisableDelayedExpansion

SET "mypath=%~dp0"



py -3.6 -V >nul 2>&1

IF %errorlevel% equ 0 (
	echo "Found Python 3.6"
	py -3.6 "%mypath%\ocvcoin_miner.py"
) ELSE (
	echo "Found Python 3+"
	py -3 "%mypath%\ocvcoin_miner.py"
)


echo Press any key to exit...



pause >nul

ENDLOCAL