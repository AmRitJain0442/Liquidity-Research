# NSE Annual Reports Scraper - PowerShell Script
Write-Host "NSE Annual Reports Scraper" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Green

Write-Host "`nChecking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Python found: $pythonVersion" -ForegroundColor Green

Write-Host "`nInstalling required Python packages..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "`nStarting the scraper..." -ForegroundColor Yellow
Write-Host "You can choose between two versions:" -ForegroundColor Cyan
Write-Host "1. Python requests-based scraper (scrape_annual_reports.py)" -ForegroundColor White
Write-Host "2. CURL-based scraper (scrape_reports_curl.py)" -ForegroundColor White

$choice = Read-Host "`nChoose version (1 or 2)"

switch ($choice) {
    "1" {
        Write-Host "Running Python requests-based scraper..." -ForegroundColor Green
        python scrape_annual_reports.py
    }
    "2" {
        Write-Host "Running CURL-based scraper..." -ForegroundColor Green
        python scrape_reports_curl.py
    }
    default {
        Write-Host "Invalid choice. Running default Python requests-based scraper..." -ForegroundColor Yellow
        python scrape_annual_reports.py
    }
}

Write-Host "`nScraping completed. Check the 'downloaded_reports' folder for your files." -ForegroundColor Green
Read-Host "Press Enter to exit"
