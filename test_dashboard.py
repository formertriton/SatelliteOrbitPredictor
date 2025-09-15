from src.data_fetcher import TLEDataFetcher
from src.orbit_predictor import SatelliteOrbitPredictor
from src.satellite_dashboard import SatelliteDashboard

def main():
    print("🚀 LOADING SATELLITE TRACKING DASHBOARD...")
    
    # Get latest satellite data
    fetcher = TLEDataFetcher(cache_dir="data")
    tle_file = fetcher.download_tle_data('stations')
    
    # Initialize predictor
    predictor = SatelliteOrbitPredictor()
    satellites = predictor.load_tle_file(tle_file)
    
    # Select satellites for dashboard
    available_sats = list(satellites.keys())
    satellites_to_track = available_sats[:4]  # Track first 4 satellites
    
    print(f"📡 Tracking {len(satellites_to_track)} satellites:")
    for i, sat in enumerate(satellites_to_track, 1):
        print(f"  {i}. {sat}")
    
    # Create dashboard
    print("\n📊 GENERATING COMPREHENSIVE DASHBOARD...")
    dashboard = SatelliteDashboard()
    
    # Generate the full dashboard
    fig = dashboard.create_comprehensive_dashboard(
        predictor, 
        satellites_to_track, 
        duration_hours=6
    )
    
    print("✅ DASHBOARD COMPLETE!")
    print("\n🎯 Your dashboard includes:")
    print("  • 3D Orbital Visualization")
    print("  • Real-time Ground Tracks") 
    print("  • Altitude Profiles")
    print("  • Satellite Status Table")
    print("  • Orbital Elements Analysis")
    print("  • Coverage Comparison")
    print("\nThis is professional-grade space situational awareness! 🛰️")

if __name__ == "__main__":
    main()