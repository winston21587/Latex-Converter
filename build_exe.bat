@echo off
REM Builds "LaTeX Translator.exe" (no console window) from latex_to_text.py
cd /d "%~dp0"
python -m pip install --upgrade pyinstaller
python -m PyInstaller --onefile --windowed --clean --name "LaTeX Translator" latex_to_text.py
echo.
echo ============================================================
echo  Done!  Your app is here:  dist\LaTeX Translator.exe
echo  You can move it anywhere (Desktop, taskbar, etc.).
echo ============================================================
pause
