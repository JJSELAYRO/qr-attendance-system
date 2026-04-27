@echo off
chcp 65001 >nul

:: QR Attendance - Google Drive Upload Script
:: Usage: upload.bat <path_to_apk_file>

echo ========================================
echo   Upload APK to Google Drive            
echo ========================================
echo.

:: Check if APK path is provided
if "%~1"=="" (
    echo ERROR: Please provide the path to the APK file
    echo.
    echo Usage:
    echo   upload.bat ..\frontend\bin\qrattendance-1.0.0-arm64-v8a.apk
    echo.
    pause
    exit /b 1
)

:: Check if client_secret.json exists
if not exist "client_secret.json" (
    echo ERROR: client_secret.json not found!
    echo.
    echo Please download it from Google Cloud Console:
    echo   1. Go to https://console.cloud.google.com/
    echo   2. Create a project and enable Google Drive API
    echo   3. Create OAuth 2.0 credentials ^(Desktop app^)
    echo   4. Download client_secret.json and place it in this folder
    echo.
    echo Expected path: %~dp0client_secret.json
    echo.
    pause
    exit /b 1
)

:: Activate virtual environment and run upload
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting upload script...
echo First time will open browser for Google authorization
echo.

python upload_to_drive.py %1

:: Deactivate environment
call venv\Scripts\deactivate.bat

echo.
echo ========================================
echo   Upload process completed!             
echo ========================================
echo.
pause
