#!/usr/bin/env python3
"""
NSE Annual Reports Scraper using CURL commands
This script uses subprocess to execute curl commands for scraping NSE annual reports.
"""

import csv
import json
import os
import re
import subprocess
import time
from pathlib import Path
from urllib.parse import quote, unquote

class CurlBasedNSEScraper:
    def __init__(self):
        self.base_url = "https://www.nseindia.com"
        self.api_url = "https://www.nseindia.com/api/annual-reports"
        
        # Create downloads directory
        self.downloads_dir = Path("downloaded_reports")
        self.downloads_dir.mkdir(exist_ok=True)
        
        # Create a temporary directory for curl outputs
        self.temp_dir = Path("temp_curl_outputs")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Basic headers for curl
        self.curl_headers = [
            'accept: */*',
            'accept-language: en-US,en;q=0.9,en-IN;q=0.8',
            'priority: u=1, i',
            'referer: https://www.nseindia.com/companies-listing/corporate-filings-annual-reports',
            'sec-ch-ua: "Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile: ?0',
            'sec-ch-ua-platform: "Windows"',
            'sec-fetch-dest: empty',
            'sec-fetch-mode: cors',
            'sec-fetch-site: same-origin',
            'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'
        ]
        
        # Cookies file path
        self.cookies_file = self.temp_dir / "cookies.txt"
    
    def get_initial_cookies(self):
        """Get initial cookies using curl"""
        try:
            cmd = [
                'curl',
                '-s',
                '-c', str(self.cookies_file),  # Save cookies
                'https://www.nseindia.com/companies-listing/corporate-filings-annual-reports'
            ]
            
            for header in self.curl_headers:
                cmd.extend(['-H', header])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Initial cookies obtained successfully")
                return True
            else:
                print(f"Failed to get initial cookies: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error getting initial cookies: {e}")
            return False
    
    def clean_company_name(self, company_name):
        """Clean company name for API search"""
        cleaned = re.sub(r'\s+(LIMITED|LTD\.?|PRIVATE|PVT\.?|COMPANY|CO\.?|CORPORATION|CORP\.?)$', '', company_name, flags=re.IGNORECASE)
        return cleaned.strip()
    
    def search_company_reports_curl(self, company_name, symbol):
        """Search for annual reports using curl"""
        try:
            clean_name = self.clean_company_name(company_name)
            
            # URL encode the parameters
            encoded_name = quote(clean_name)
            encoded_symbol = quote(symbol)
            
            # Construct the API URL with parameters
            api_url = f"{self.api_url}?index=equities&symbol={encoded_symbol}&issuer={encoded_name}"
            
            # Output file for this request
            output_file = self.temp_dir / f"response_{symbol}.json"
            
            print(f"Searching reports for: {company_name} (Symbol: {symbol})")
            
            cmd = [
                'curl',
                '-s',
                '-b', str(self.cookies_file),  # Use saved cookies
                '-o', str(output_file),  # Save output to file
                api_url
            ]
            
            for header in self.curl_headers:
                cmd.extend(['-H', header])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Read the response file
                if output_file.exists():
                    with open(output_file, 'r', encoding='utf-8') as f:
                        try:
                            data = json.load(f)
                            return data
                        except json.JSONDecodeError:
                            print(f"Invalid JSON response for {company_name}")
                            return None
                else:
                    print(f"No response file created for {company_name}")
                    return None
            else:
                print(f"Curl command failed for {company_name}: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"Error searching reports for {company_name}: {e}")
            return None
    
    def download_file_curl(self, url, company_name, filename=None):
        """Download a file using curl"""
        try:
            if not filename:
                filename = os.path.basename(unquote(url))
            
            # Create company-specific directory
            company_dir = self.downloads_dir / self.sanitize_filename(company_name)
            company_dir.mkdir(exist_ok=True)
            
            file_path = company_dir / filename
            
            # Skip if file already exists
            if file_path.exists():
                print(f"File already exists: {file_path}")
                return True
            
            print(f"Downloading: {filename}")
            
            cmd = [
                'curl',
                '-s',
                '-L',  # Follow redirects
                '-b', str(self.cookies_file),  # Use cookies
                '-o', str(file_path),  # Output file
                url
            ]
            
            # Add basic headers for download
            download_headers = [
                'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
                'referer: https://www.nseindia.com/'
            ]
            
            for header in download_headers:
                cmd.extend(['-H', header])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and file_path.exists() and file_path.stat().st_size > 0:
                print(f"Downloaded: {file_path} ({file_path.stat().st_size} bytes)")
                return True
            else:
                print(f"Failed to download {url}")
                if file_path.exists():
                    file_path.unlink()  # Remove empty file
                return False
                
        except Exception as e:
            print(f"Error downloading file {url}: {e}")
            return False
    
    def sanitize_filename(self, filename):
        """Sanitize filename for Windows compatibility"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename.strip()
    
    def extract_download_links_from_response(self, data):
        """Extract download links from API response"""
        download_links = []
        
        if not data or not isinstance(data, dict):
            return download_links
        
        def find_links_recursive(obj, links_list):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, str) and (value.endswith('.pdf') or value.endswith('.zip')):
                        if 'nsearchives.nseindia.com' in value:
                            links_list.append(value)
                    else:
                        find_links_recursive(value, links_list)
            elif isinstance(obj, list):
                for item in obj:
                    find_links_recursive(item, links_list)
        
        find_links_recursive(data, download_links)
        return download_links
    
    def process_company(self, company_name, symbol):
        """Process a single company - search and download reports"""
        print(f"\n{'='*50}")
        print(f"Processing: {company_name}")
        print(f"{'='*50}")
        
        # Search for company reports
        data = self.search_company_reports_curl(company_name, symbol)
        
        if not data:
            print(f"No data found for {company_name}")
            return 0
        
        # Extract download links
        download_links = self.extract_download_links_from_response(data)
        
        if not download_links:
            print(f"No download links found for {company_name}")
            print(f"API Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            return 0
        
        print(f"Found {len(download_links)} files to download")
        
        # Download each file
        downloaded_count = 0
        for link in download_links:
            if self.download_file_curl(link, company_name):
                downloaded_count += 1
            
            # Add a small delay between downloads
            time.sleep(1)
        
        print(f"Downloaded {downloaded_count} files for {company_name}")
        return downloaded_count
    
    def load_companies_from_csv(self, csv_file_path):
        """Load company names from CSV file"""
        companies = []
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    company_name = row.get('Company Name', '').strip()
                    symbol = row.get('Symbol', '').strip()
                    
                    if company_name and symbol:
                        companies.append((company_name, symbol))
        
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return []
        
        return companies
    
    def run_scraper(self, csv_file_path, max_companies=None, start_from=0):
        """Main method to run the scraper"""
        print("NSE Annual Reports Scraper (CURL-based) Starting...")
        
        # Get initial cookies
        if not self.get_initial_cookies():
            print("Failed to get initial cookies. Continuing anyway...")
        
        # Load companies from CSV
        companies = self.load_companies_from_csv(csv_file_path)
        
        if not companies:
            print("No companies loaded from CSV file")
            return
        
        print(f"Loaded {len(companies)} companies from CSV")
        
        # Apply limits if specified
        if start_from > 0:
            companies = companies[start_from:]
            print(f"Starting from company index {start_from}")
        
        if max_companies:
            companies = companies[:max_companies]
            print(f"Processing only first {max_companies} companies")
        
        total_downloads = 0
        successful_companies = 0
        
        # Process each company
        for i, (company_name, symbol) in enumerate(companies, start_from + 1):
            try:
                downloads = self.process_company(company_name, symbol)
                total_downloads += downloads
                
                if downloads > 0:
                    successful_companies += 1
                
                # Add delay between companies
                print(f"Processed company {i}/{len(companies) + start_from}")
                time.sleep(2)  # Be respectful to the server
                
            except KeyboardInterrupt:
                print("\nScraping interrupted by user")
                break
            except Exception as e:
                print(f"Error processing {company_name}: {e}")
                continue
        
        print(f"\n{'='*50}")
        print("SCRAPING COMPLETED")
        print(f"{'='*50}")
        print(f"Total companies processed: {len(companies)}")
        print(f"Companies with downloads: {successful_companies}")
        print(f"Total files downloaded: {total_downloads}")
        print(f"Downloads saved in: {self.downloads_dir.absolute()}")
        
        # Clean up temporary files
        self.cleanup()
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            for file in self.temp_dir.glob("*"):
                file.unlink()
            self.temp_dir.rmdir()
            print("Temporary files cleaned up")
        except Exception as e:
            print(f"Error cleaning up temporary files: {e}")

def main():
    """Main function"""
    # Configuration
    CSV_FILE = "ind_nifty500list.csv"
    MAX_COMPANIES = None # Set to None to process all companies, or set a number like 5 for testing
    START_FROM = 0  # Start from a specific company index (0-based)
    
    # Create and run scraper
    scraper = CurlBasedNSEScraper()
    scraper.run_scraper(CSV_FILE, max_companies=MAX_COMPANIES, start_from=START_FROM)

if __name__ == "__main__":
    main()
