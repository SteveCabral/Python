@echo off
SetLocal
cd /d "%~dp0"

echo Activating Python environment...
call "C:\PythonVenv\py311\Scripts\activate.bat"

echo Building PDF_Page_Size_Finder.exe...
python -m PyInstaller --noconfirm "PDF_Page_Size_Finder.spec"

if exist "dist\PDF_Page_Size_Finder.exe" (
    echo.
    echo SUCCESS: dist\PDF_Page_Size_Finder.exe rebuilt.
) else (
    echo.
    echo ERROR: Build did not produce dist\PDF_Page_Size_Finder.exe.
    exit /b 1
)

echo.
echo Build finished.
pause
