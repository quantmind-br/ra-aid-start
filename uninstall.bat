@echo off
echo Uninstalling ra-aid-start using pipx...
echo.

REM Check if pipx is installed
pipx --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pipx is not installed or not in PATH
    echo.
    pause
    exit /b 1
)

REM Uninstall the package
echo Running: pipx uninstall ra-aid-start
pipx uninstall ra-aid-start

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: ra-aid-start has been uninstalled successfully!
    echo.
) else (
    echo.
    echo ERROR: Uninstallation failed or package was not installed
    echo.
)

pause