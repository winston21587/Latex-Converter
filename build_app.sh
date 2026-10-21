#!/usr/bin/env bash
# Builds a standalone app (macOS / Linux) from latex_to_text.py
cd "$(dirname "$0")"
python3 -m pip install --upgrade pyinstaller
python3 -m PyInstaller --onefile --windowed --clean --name "LaTeX Translator" latex_to_text.py
echo
echo "Done! Your app is in the 'dist' folder."
