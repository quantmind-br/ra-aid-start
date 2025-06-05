@echo off
echo Installing ra-aid-start using pipx...
echo.

REM Check if pipx is installed
pipx --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pipx is not installed or not in PATH
    echo Please install pipx first: pip install pipx
    echo.
    pause
    exit /b 1
)

REM Install the package in editable mode
echo Running: pipx install -e .
pipx install -e .

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: ra-aid-start has been installed successfully!
    echo You can now run the application with: ra-aid-start
    echo.
) else (
    echo.
    echo ERROR: Installation failed
    echo.
)

pause