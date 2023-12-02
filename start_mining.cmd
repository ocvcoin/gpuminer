@echo off


SET mypath=%~dp0

py -3.6 "%mypath%\ocvcoin_miner.py" || py -3 "%mypath%\ocvcoin_miner.py"

echo Press any key to exit...



pause >nul