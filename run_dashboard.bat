@echo off
REM TN Spark Dashboard - Automated Setup and Launch Script
REM =====================================================
REM This batch file automates the setup and launch process for the Streamlit dashboard
REM It installs required dependencies and starts the application
REM Usage: Double-click this file or run from command prompt

echo ==========================================
echo TN Spark Dashboard - Setup and Launch
echo ==========================================
echo.

REM Install Python dependencies from requirements file
echo [1/2] Installing required Python packages...
echo This may take a few minutes on first run...
python -m pip install -r requirements_streamlit.txt

REM Check if installation was successful
if %errorlevel% equ 0 (
    echo [✓] Dependencies installed successfully!
) else (
    echo [✗] Error installing dependencies. Please check:
    echo     - Python is installed and in PATH
    echo     - pip is working correctly
    echo     - requirements_streamlit.txt exists
    pause
    exit /b 1
)

echo.
echo [2/2] Starting Streamlit dashboard application...
echo The dashboard will open in your default web browser

REM Launch the Streamlit application
streamlit run dashboard_streamlit.py

REM If Streamlit command fails, provide helpful error message
if %errorlevel% neq 0 (
    echo.
    echo [✗] Failed to start Streamlit application
    echo Please ensure:
    echo     - All dependencies were installed successfully
    echo     - dashboard_streamlit.py exists in this directory
    echo     - No other application is using port 8501
    pause
)

echo.
echo ==========================================
echo Dashboard session ended
echo ==========================================
pause