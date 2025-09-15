"""
TLE Data Fetcher Module
Downloads and parses Two-Line Element data from various sources
"""

import requests
import os
from datetime import datetime
from typing import List, Dict, Optional
import time

class TLEDataFetcher:
    """
    Handles downloading and caching TLE data from CelesTrak and other sources
    """
    
    def __init__(self, cache_dir: str = "../data"):
        self.cache_dir = cache_dir
        self.base_urls = {
            'stations': 'https://celestrak.org/NORAD/elements/stations.txt',
            'active': 'https://celestrak.org/NORAD/elements/active.txt',
            'starlink': 'https://celestrak.org/NORAD/elements/starlink.txt',
            'gps': 'https://celestrak.org/NORAD/elements/gps-ops.txt',
            'weather': 'https://celestrak.org/NORAD/elements/weather.txt'
        }
        
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)

    def download_tle_data(self, category: str = 'stations', force_refresh: bool = False) -> str:
        """
        Download TLE data for a specific satellite category
        """
        if category not in self.base_urls:
            raise ValueError(f"Unknown category: {category}")
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{category}_{timestamp}.tle"
        filepath = os.path.join(self.cache_dir, filename)
        
        # Download the data
        print(f"Downloading {category} TLE data...")
        response = requests.get(self.base_urls[category], timeout=30)
        response.raise_for_status()
        
        # Save to file
        with open(filepath, 'w') as f:
            f.write(response.text)
        
        print(f"Downloaded to {filepath}")
        return filepath