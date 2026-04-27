@echo off
chcp 65001 >nul

:: QR Attendance System - APK Build Script (Windows)
:: Run this script to build the Android APK

echo ========================================
echo   QR Attendance System - APK Builder    
echo ========================================
echo.

:: Check if buildozer is installed
buildozer --version >nul 2>&1
if errorlevel 1 (
    echo Error: buildozer is not installed!
    echo Install it with: pip install buildozer
    pause
    exit /b 1
)

:: Navigate to frontend directory
cd /d "%~dp0\..\frontend"

:: Clean previous builds
echo Cleaning previous builds...
buildozer android clean

:: Build APK
echo.
echo Building APK...
echo This may take 10-30 minutes on first run...
echo.

buildozer android debug

:: Check if build was successful
if %errorlevel% == 0 (
    echo.
    echo ========================================
    echo   Build Successful!                     
    echo ========================================
    echo.
    echo APK location: .\bin\
    dir /b .\bin\*.apk 2>nul || echo Check the bin directory
    echo.
    echo To install on device:
    echo   buildozer android deploy run
    echo.
) else (
    echo.
    echo ========================================
    echo   Build Failed!                         
    echo ========================================
    echo.
    echo Check the error messages above.
    echo Common issues:
    echo   - Missing dependencies
    echo   - Java not installed
    echo   - Android SDK not configured
    echo.
)

pause
