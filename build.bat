@echo off
echo ========================================
echo Battery Shutdown - Build Script
echo ========================================
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo ERROR: Virtual environment is not activated
    echo Please run: venv\Scripts\activate.bat
    pause
    exit /b 1
)

REM Check if icon file exists (optional)
set ICON_PARAM=
if exist "icon.ico" (
    echo Using icon file: icon.ico
    set ICON_PARAM=--icon=icon.ico
) else (
    echo Warning: icon.ico not found, building without custom icon
)

echo.
echo Cleaning previous build...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "BatteryShutdown.spec" del /q BatteryShutdown.spec

echo.
echo Building executable with PyInstaller...
echo This may take a few minutes...
echo.

pyinstaller --onefile ^
    --windowed ^
    --name=BatteryShutdown ^
    %ICON_PARAM% ^
    --add-data "src;src" ^
    main.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Executable location: dist\BatteryShutdown.exe
echo.
echo You can now distribute the executable file.
echo.
pause