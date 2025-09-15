from src.data_fetcher import TLEDataFetcher
from src.orbit_predictor import SatelliteOrbitPredictor
from src.collision_detector import CollisionDetector

# Get satellite data
fetcher = TLEDataFetcher(cache_dir="data")
tle_file = fetcher.download_tle_data('stations')

predictor = SatelliteOrbitPredictor()
satellites = predictor.load_tle_file(tle_file)

# Create collision detector
detector = CollisionDetector(warning_distance_km=50.0)  # 50km warning threshold

print("🛰️ Available satellites for collision analysis:")
sat_list = list(satellites.keys())
for i, name in enumerate(sat_list[:5]):
    print(f"  {i+1}. {name}")

# Analyze collision risk between ISS and Chinese space station
if 'ISS (ZARYA)' in satellites and 'CSS (TIANHE)' in satellites:
    print("\n🚨 Analyzing collision risk: ISS vs Chinese Space Station...")
    
    analysis = detector.analyze_close_approach(
        predictor, 'ISS (ZARYA)', 'CSS (TIANHE)', 
        duration_hours=12, points=150
    )
    
    # Display results
    if 'error' not in analysis:
        print(f"\n📊 COLLISION ANALYSIS RESULTS:")
        print(f"Risk Level: {analysis['collision_risk']}")
        print(f"Minimum Distance: {analysis['min_distance_km']:.2f} km")
        print(f"Closest Approach: {analysis['closest_approach_time'].strftime('%H:%M:%S UTC')}")
        print(f"Relative Velocity: {analysis['relative_velocity_km_s']:.3f} km/s")
        
        # Generate professional report
        report = detector.generate_collision_report(analysis)
        print(report)
        
        # Create visualization
        print("\n📈 Creating collision analysis plot...")
        detector.plot_collision_analysis(analysis)
        
    else:
        print(f"Analysis failed: {analysis['error']}")

else:
    print("❌ Required satellites not found for collision analysis")