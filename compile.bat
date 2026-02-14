@echo off
REM =================================================================
REM  Build-Skript für den Logfile-Viewer
REM =================================================================
REM
REM  Dieses Skript verwendet PyInstaller, um die Python-Anwendung
REM  "logviewer.py" in eine einzelne, portable EXE-Datei zu kompilieren.
REM
REM  Voraussetzungen:
REM  - Python muss installiert und im System-PATH sein.
REM  - PyInstaller muss installiert sein: pip install pyinstaller
REM
REM  Das Skript muss im selben Verzeichnis wie "logviewer.py" und
REM  "icon.ico" ausgeführt werden.

echo.
echo [INFO] Starte Kompilierung von Logfile-Viewer...
echo.

pyinstaller ^
    --name "Logfile-Viewer" ^
    --onefile ^
    --windowed ^
    --clean ^
    --icon="icon.ico" ^
    "logviewer.py"

echo.
echo [INFO] Raeume temporaere Build-Dateien auf...

if exist "build" (
    rd /s /q "build"
)
if exist "Logfile-Viewer.spec" (
    del /q "Logfile-Viewer.spec"
)

echo.
echo [SUCCESS] Kompilierung abgeschlossen.
echo Die fertige EXE-Datei befindet sich im "dist"-Ordner.
echo.

pause