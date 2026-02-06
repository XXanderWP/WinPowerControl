#!/bin/bash

echo "========================================"
echo "Battery Shutdown - Build Script"
echo "========================================"
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "ERROR: Virtual environment is not activated"
    echo "Please run: source venv/bin/activate"
    exit 1
fi

# Check if icon file exists (optional)
ICON_PARAM=""
if [ -f "icon.ico" ]; then
    echo "Using icon file: icon.ico"
    ICON_PARAM="--icon=icon.ico"
else
    echo "Warning: icon.ico not found, building without custom icon"
fi

echo ""
echo "Cleaning previous build..."
rm -rf build dist BatteryShutdown.spec

echo ""
echo "Building executable with PyInstaller..."
echo "This may take a few minutes..."
echo ""

pyinstaller --onefile \
    --windowed \
    --name=BatteryShutdown \
    $ICON_PARAM \
    --add-data "src:src" \
    main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Build failed"
    exit 1
fi

echo ""
echo "========================================"
echo "Build completed successfully!"
echo "========================================"
echo ""
echo "Executable location: dist/BatteryShutdown"
echo ""
echo "You can now distribute the executable file."
echo ""