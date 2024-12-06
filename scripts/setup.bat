@echo off
:: Remove SETLOCAL to allow environment changes to persist

python --version >NUL 2>&1
if errorlevel 9009 (
    echo Python not found
    exit /b 1
)

if exist .venv (
    echo Virtual environment exists
) else (
    echo Creating virtual environment with Python venv
    python -m venv .venv
)

echo Activating virtual environment...
CALL .venv\scripts\activate.bat
if errorlevel 1 (
    echo Venv activation failed
    exit /b 1
)

:: Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

:: Install the package in editable mode
echo Installing package in editable mode...
pip install -e .
if errorlevel 1 (
    echo Failed to install package
    exit /b 1
)

echo Setup completed successfully