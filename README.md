# NSE Annual Reports Scraper

This project scrapes annual reports (PDF and ZIP files) from the NSE India website for companies listed in the CSV file.

## Files Overview

- `scrape_annual_reports.py` - Main scraper using Python requests library
- `scrape_reports_curl.py` - Alternative scraper using curl commands (as requested)
- `test_scraper.py` - Test script to verify functionality with sample companies
- `run_scraper.bat` - Windows batch script to run the scraper
- `run_scraper.ps1` - PowerShell script to run the scraper
- `requirements.txt` - Python dependencies
- `ind_nifty500list.csv` - Input file with company data (already modified with "LIMITED")

## Prerequisites

1. **Python 3.6+** installed and available in PATH
2. **curl** command available (usually pre-installed on Windows 10/11)
3. **Internet connection**

## Quick Start

### Option 1: Using PowerShell (Recommended for Windows)

```powershell
# Navigate to the project directory
cd "c:\Users\amrit\Desktop\LIq-proj"

# Run the PowerShell script
.\run_scraper.ps1
```

### Option 2: Using Command Prompt

```cmd
# Navigate to the project directory
cd c:\Users\amrit\Desktop\LIq-proj

# Run the batch script
run_scraper.bat
```

### Option 3: Manual Python Execution

```powershell
# Install dependencies
pip install -r requirements.txt

# Test with sample companies first
python test_scraper.py

# Run the full scraper (choose one)
python scrape_annual_reports.py          # Python requests-based
python scrape_reports_curl.py           # CURL-based (preferred as requested)
```

## Configuration

Edit the main configuration at the bottom of the Python files:

```python
# Configuration
CSV_FILE = "ind_nifty500list.csv"
MAX_COMPANIES = None    # Set to a number like 10 for testing, None for all
START_FROM = 0          # Start from a specific company index (0-based)
```

## How It Works

1. **Cookie Setup**: First gets initial cookies from the NSE website
2. **Company Processing**: For each company in the CSV:
   - Cleans the company name for API compatibility
   - Calls the NSE API: `https://www.nseindia.com/api/annual-reports`
   - Extracts download links for PDF and ZIP files
   - Downloads all found files to organized folders
3. **File Organization**: Creates folders per company in `downloaded_reports/`

## API Endpoint Used

The scraper uses the official NSE API endpoint:

```
https://www.nseindia.com/api/annual-reports?index=equities&symbol=SYMBOL&issuer=COMPANY_NAME
```

## Download Structure

```
downloaded_reports/
├── 360_ONE_WAM_LIMITED/
│   ├── AR_12345_2023_report.pdf
│   └── AR_12345_2022_report.zip
├── 3M_India_LIMITED/
│   └── AR_67890_2023_report.pdf
└── ... (other companies)
```

## Features

- **Resume Capability**: Skips already downloaded files
- **Error Handling**: Continues processing even if some companies fail
- **Progress Tracking**: Shows detailed progress and statistics
- **Rate Limiting**: Includes delays between requests to be respectful to the server
- **Multiple Formats**: Supports both PDF and ZIP file downloads
- **Clean Naming**: Sanitizes filenames for Windows compatibility

## Troubleshooting

### Common Issues

1. **No files downloaded**

   - Run `test_scraper.py` first to test with sample companies
   - Check internet connection
   - NSE website might have changed their API

2. **Permission errors**

   - Make sure you have write permissions in the project directory
   - Run as administrator if needed

3. **CURL not found**

   - Ensure curl is installed and available in PATH
   - Use the Python requests version instead

4. **Rate limiting**
   - The scraper includes built-in delays
   - If you get blocked, wait and try again later

### Testing

Always test first with a small number of companies:

```python
# In the script, modify:
MAX_COMPANIES = 5  # Test with only 5 companies first
```

## API Response Structure

The NSE API returns JSON data containing download links. The scraper recursively searches through the response to find URLs ending with `.pdf` or `.zip` from `nsearchives.nseindia.com`.

## Compliance Notes

- This scraper only accesses publicly available data
- Includes appropriate delays between requests
- Uses standard browser headers to avoid being flagged
- Respects the website's structure and doesn't overload servers

## Customization

### Adding More File Types

Edit the `extract_download_links_from_response` method to include additional file extensions:

```python
if isinstance(value, str) and (value.endswith('.pdf') or value.endswith('.zip') or value.endswith('.doc')):
```

### Changing Company Search Logic

Modify the `clean_company_name` method to adjust how company names are processed for API calls.

### Adding Custom Headers

Add more headers to the `curl_headers` or `headers` lists if needed for authentication or to mimic specific browsers.

## Support

If you encounter issues:

1. Check the console output for specific error messages
2. Test with the `test_scraper.py` script first
3. Verify that the NSE website structure hasn't changed
4. Ensure all dependencies are properly installed
