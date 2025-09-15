from src.data_fetcher import TLEDataFetcher
from src.orbit_predictor import SatelliteOrbitPredictor
from datetime import datetime

# Download TLE data
fetcher = TLEDataFetcher(cache_dir="data")
tle_file = fetcher.download_tle_data('stations')

# Create orbit predictor and load data
predictor = SatelliteOrbitPredictor()
satellites = predictor.load_tle_file(tle_file)

print("Available satellites:")
for name in list(satellites.keys())[:5]:  # Show first 5
    print(f"  - {name}")

# Test with ISS if available
if 'ISS (ZARYA)' in satellites:
    sat_name = 'ISS (ZARYA)'
    print(f"\nTesting with {sat_name}")
    
    # Get current position
    x, y, z = predictor.predict_position(sat_name, datetime.utcnow())
    print(f"Current position: ({x:.1f}, {y:.1f}, {z:.1f}) km")
    
    # Get satellite info
    info = predictor.get_satellite_info(sat_name)
    print(f"Latitude: {info['current_latitude']:.2f}°")
    print(f"Longitude: {info['current_longitude']:.2f}°")