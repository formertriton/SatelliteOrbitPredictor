from src.data_fetcher import TLEDataFetcher
from src.orbit_predictor import SatelliteOrbitPredictor
from src.ground_track import GroundTrackCalculator

# Get data
fetcher = TLEDataFetcher(cache_dir="data")
tle_file = fetcher.download_tle_data('stations')

predictor = SatelliteOrbitPredictor()
satellites = predictor.load_tle_file(tle_file)

# Create ground track calculator
ground_tracker = GroundTrackCalculator()

# Calculate ISS ground track
if 'ISS (ZARYA)' in satellites:
    print("🌍 Calculating ISS ground track...")
    lats, lons = ground_tracker.calculate_ground_track(predictor, 'ISS (ZARYA)', 
                                                      duration_hours=3, points=80)
    
    # Show ground track on world map
    ground_tracker.plot_ground_track_simple(lats, lons, 'ISS (ZARYA)')
    
    # Analyze coverage
    coverage = ground_tracker.analyze_coverage(lats, lons)
    print(f"📊 Coverage Analysis:")
    print(f"  Max Latitude: {coverage['max_latitude']:.1f}°")
    print(f"  Min Latitude: {coverage['min_latitude']:.1f}°")
    print(f"  Equatorial Crossings: {coverage['equatorial_crossings']}")