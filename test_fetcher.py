from src.data_fetcher import TLEDataFetcher

# Test our fetcher
fetcher = TLEDataFetcher()
tle_file = fetcher.download_tle_data('stations')
print(f"TLE file saved to: {tle_file}")