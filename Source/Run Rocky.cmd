@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 goto python
py -3 -c "import PySide6" >nul 2>nul
if errorlevel 1 py -3 -m pip install -r requirements.txt
if errorlevel 1 goto failed
py -3 launch_windows.py
if errorlevel 1 goto failed
exit /b 0
:python
python -c "import PySide6" >nul 2>nul
if errorlevel 1 python -m pip install -r requirements.txt
if errorlevel 1 goto failed
python launch_windows.py
if errorlevel 1 goto failed
exit /b 0
:failed
echo Rocky could not start. Install Python 3.11 or newer with pip enabled.
pause
exit /b 1
