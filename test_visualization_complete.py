from src.data_fetcher import TLEDataFetcher
from src.orbit_predictor import SatelliteOrbitPredictor
from src.visualization import SatelliteVisualizer

def main():
    # Get TLE data
    fetcher = TLEDataFetcher(cache_dir="data")
    tle_file = fetcher.download_tle_data('stations')

    # Load satellites
    predictor = SatelliteOrbitPredictor()
    satellites = predictor.load_tle_file(tle_file)

    # Create visualizer
    visualizer = SatelliteVisualizer()

    print("\n=== SATELLITE ORBIT VISUALIZATION OPTIONS ===")
    print("1. Single satellite (ISS detailed view)")
    print("2. Multiple satellites (comparison view)")
    print("3. Both visualizations")
    
    choice = input("\nEnter your choice (1, 2, or 3): ")
    
    if choice in ['1', '3']:
        # Single satellite visualization
        if 'ISS (ZARYA)' in satellites:
            print("\n🚀 Generating ISS detailed orbit visualization...")
            x, y, z = predictor.generate_orbit_path('ISS (ZARYA)', duration_hours=2, points=50)
            visualizer.plot_single_satellite(x, y, z, 'ISS (ZARYA)')
            print("✅ ISS detailed plot created!")
        else:
            print("❌ ISS not found in satellite data")
    
    if choice in ['2', '3']:
        # Multiple satellites visualization
        print("\n🛰️ Generating multi-satellite comparison...")
        orbit_data = {}
        
        # Get orbits for first 3 satellites
        satellite_names = list(satellites.keys())[:3]
        for sat_name in satellite_names:
            try:
                x, y, z = predictor.generate_orbit_path(sat_name, duration_hours=2, points=40)
                orbit_data[sat_name] = (x, y, z)
                print(f"  ✅ Added {sat_name}")
            except Exception as e:
                print(f"  ❌ Error with {sat_name}: {e}")
        
        # Plot multiple satellites
        if orbit_data:
            visualizer.plot_satellite_orbit(orbit_data, "Space Station Orbits - Live Tracking")
            print("✅ Multi-satellite comparison plot created!")
    
    if choice not in ['1', '2', '3']:
        print("❌ Invalid choice. Please run again and select 1, 2, or 3.")
    
    print("\n🎯 Visualization complete! Check your plot windows.")

if __name__ == "__main__":
    main()