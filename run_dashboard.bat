@echo off
REM TN Spark Dashboard - Automated Setup and Launch Script
REM =====================================================
REM This batch file creates a local virtual environment (outside OneDrive),
REM installs dependencies from requirements.txt, and launches the Streamlit app.
REM Usage: Double-click this file or run from a command prompt.

setlocal
set VENV_DIR=%LOCALAPPDATA%\tnspark-venv

echo ==========================================
echo TN Spark Dashboard - Setup and Launch
echo ==========================================
echo.

echo [1/3] Ensuring virtual environment at "%VENV_DIR%"
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo Creating virtual environment...
    where py >nul 2>nul
    if %errorlevel%==0 (
        py -m venv "%VENV_DIR%"
    ) else (
        python -m venv "%VENV_DIR%"
    )
)

echo.
echo [2/3] Installing required Python packages (this may take a moment)...
"%VENV_DIR%\Scripts\pip.exe" install --upgrade pip
"%VENV_DIR%\Scripts\pip.exe" install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [✗] Error installing dependencies. Please check:
    echo     - Python is installed and available as 'py' or 'python'
    echo     - pip is working correctly
    echo     - requirements.txt is present
    pause
    exit /b 1
)
echo [✓] Dependencies installed successfully!

echo.
echo [3/3] Starting Streamlit dashboard application...
set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
"%VENV_DIR%\Scripts\python.exe" -m streamlit run dashboard_streamlit.py --server.headless true

if %errorlevel% neq 0 (
    echo.
    echo [✗] Failed to start Streamlit application
    echo Please ensure:
    echo     - All dependencies were installed successfully
    echo     - dashboard_streamlit.py exists in this directory
    echo     - No other application is using the Streamlit port
    pause
)

echo.
echo ==========================================
echo Dashboard session ended
echo ==========================================
endlocal
pause
