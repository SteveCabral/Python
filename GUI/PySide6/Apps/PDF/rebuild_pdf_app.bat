@echo off
SetLocal
cd /d "%~dp0"

set "PYTHON=C:\PythonVenv\py311\Scripts\python.exe"

if not exist "%PYTHON%" (
    echo ERROR: Python not found at %PYTHON%
    pause
    exit /b 1
)

echo Checking source for syntax errors...
"%PYTHON%" -m py_compile main.py config\settings.py model\pdf_page_analyzer.py view\main_window.py
if errorlevel 1 (
    echo.
    echo ERROR: Syntax error in source. EXE was not rebuilt.
    pause
    exit /b 1
)

echo Building PDF_Page_Size_Finder.exe...
if exist "dist\PDF_Page_Size_Finder.exe" del /q "dist\PDF_Page_Size_Finder.exe"
"%PYTHON%" -m PyInstaller --noconfirm "PDF_Page_Size_Finder.spec"
if errorlevel 1 (
    echo.
    echo ERROR: PyInstaller failed.
    pause
    exit /b 1
)

if exist "dist\PDF_Page_Size_Finder.exe" (
    echo.
    echo SUCCESS: dist\PDF_Page_Size_Finder.exe rebuilt.
) else (
    echo.
    echo ERROR: Build did not produce dist\PDF_Page_Size_Finder.exe.
    pause
    exit /b 1
)

echo.
echo Build finished.
pause
