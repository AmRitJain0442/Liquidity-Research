#!/usr/bin/env python3
"""
Test script to verify the NSE scraper with a few sample companies
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrape_reports_curl import CurlBasedNSEScraper

def test_scraper():
    """Test the scraper with a few sample companies"""
    print("Testing NSE Annual Reports Scraper")
    print("=" * 40)
    
    # Sample companies to test (name, symbol)
    test_companies = [
        ("Reliance Industries LIMITED", "RELIANCE"),
        ("Tata Consultancy Services LIMITED", "TCS"),
        ("HDFC Bank LIMITED", "HDFCBANK")
    ]
    
    scraper = CurlBasedNSEScraper()
    
    # Get initial cookies
    print("Getting initial cookies...")
    if not scraper.get_initial_cookies():
        print("Warning: Failed to get initial cookies")
    
    print(f"\nTesting with {len(test_companies)} sample companies:")
    
    total_downloads = 0
    
    for i, (company_name, symbol) in enumerate(test_companies, 1):
        print(f"\n{'-' * 30}")
        print(f"Test {i}/{len(test_companies)}: {company_name}")
        print(f"{'-' * 30}")
        
        try:
            downloads = scraper.process_company(company_name, symbol)
            total_downloads += downloads
            print(f"Result: {downloads} files downloaded")
        except Exception as e:
            print(f"Error testing {company_name}: {e}")
    
    print(f"\n{'=' * 40}")
    print("TEST COMPLETED")
    print(f"{'=' * 40}")
    print(f"Total files downloaded: {total_downloads}")
    
    if total_downloads > 0:
        print("✓ Test successful! The scraper is working.")
        print("You can now run the full scraper with all companies.")
    else:
        print("⚠ Test completed but no files were downloaded.")
        print("This might be due to:")
        print("- API changes on the NSE website")
        print("- Network connectivity issues")
        print("- Need for additional headers or authentication")
    
    # Cleanup
    scraper.cleanup()

if __name__ == "__main__":
    test_scraper()
