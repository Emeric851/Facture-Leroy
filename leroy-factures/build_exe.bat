@echo off

echo =====================================
echo BUILD EXE LEROY MERLIN FACTURES
echo =====================================

pyinstaller ^
--noconfirm ^
--onefile ^
--windowed ^
app.py

pause
