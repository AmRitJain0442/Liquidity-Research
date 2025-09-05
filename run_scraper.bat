@echo off
echo NSE Annual Reports Scraper
echo =========================

echo.
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Installing required Python packages...
pip install -r requirements.txt

echo.
echo Starting the scraper...
echo You can choose between two versions:
echo 1. Python requests-based scraper (scrape_annual_reports.py)
echo 2. CURL-based scraper (scrape_reports_curl.py)

echo.
set /p choice="Choose version (1 or 2): "

if "%choice%"=="1" (
    echo Running Python requests-based scraper...
    python scrape_annual_reports.py
) else if "%choice%"=="2" (
    echo Running CURL-based scraper...
    python scrape_reports_curl.py
) else (
    echo Invalid choice. Running default Python requests-based scraper...
    python scrape_annual_reports.py
)

echo.
echo Scraping completed. Check the 'downloaded_reports' folder for your files.
pause
