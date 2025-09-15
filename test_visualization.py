from src.data_fetcher import TLEDataFetcher
from src.orbit_predictor import SatelliteOrbitPredictor
from src.visualization import SatelliteVisualizer

# Get TLE data
fetcher = TLEDataFetcher(cache_dir="data")
tle_file = fetcher.download_tle_data('stations')

# Load satellites
predictor = SatelliteOrbitPredictor()
satellites = predictor.load_tle_file(tle_file)

# Create visualizer
visualizer = SatelliteVisualizer()

# Generate ISS orbit path
if 'ISS (ZARYA)' in satellites:
    print("Generating ISS orbit visualization...")
    x, y, z = predictor.generate_orbit_path('ISS (ZARYA)', duration_hours=2, points=50)
    
    # Create single satellite plot
    visualizer.plot_single_satellite(x, y, z, 'ISS (ZARYA)')
    
    print("ISS orbit plotted! Check the 3D visualization window.")
else:
    print("ISS not found in satellite data")

# Let's also try multiple satellites
print("\nGenerating multi-satellite visualization...")
orbit_data = {}

# Get orbits for first 3 satellites
satellite_names = list(satellites.keys())[:3]
for sat_name in satellite_names:
    try:
        x, y, z = predictor.generate_orbit_path(sat_name, duration_hours=2, points=30)
        orbit_data[sat_name] = (x, y, z)
        print(f"Added {sat_name} to visualization")
    except Exception as e:
        print(f"Error with {sat_name}: {e}")

# Plot multiple satellites
if orbit_data:
    visualizer.plot_satellite_orbit(orbit_data, "Space Station Orbits")
    print("Multi-satellite plot created!")