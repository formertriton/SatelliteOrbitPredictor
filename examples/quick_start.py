#!/usr/bin/env python3
"""
🛰️ SatelliteOrbitPredictor - Quick Start Demo
Professional satellite tracking in just a few lines!
"""

from src.data_fetcher import TLEDataFetcher
from src.orbit_predictor import SatelliteOrbitPredictor
from src.satellite_dashboard import SatelliteDashboard
from datetime import datetime

def main():
    print("🚀 SATELLITE ORBIT PREDICTOR - LIVE DEMO")
    print("=" * 50)
    
    # 1. Get real-time satellite data
    print("📡 Downloading live satellite data from NORAD...")
    fetcher = TLEDataFetcher(cache_dir="data")
    tle_file = fetcher.download_tle_data('stations')
    
    # 2. Load and analyze satellites
    print("🛰️  Loading satellite catalog...")
    predictor = SatelliteOrbitPredictor()
    satellites = predictor.load_tle_file(tle_file)
    
    # 3. Track ISS in real-time
    if 'ISS (ZARYA)' in satellites:
        print(f"\n🎯 TRACKING ISS AT {datetime.utcnow().strftime('%H:%M:%S UTC')}")
        
        # Current position
        x, y, z = predictor.predict_position('ISS (ZARYA)', datetime.utcnow())
        print(f"   Position: ({x:.1f}, {y:.1f}, {z:.1f}) km from Earth center")
        
        # Detailed info
        info = predictor.get_satellite_info('ISS (ZARYA)')
        print(f"   Latitude: {info['current_latitude']:.2f}°")
        print(f"   Longitude: {info['current_longitude']:.2f}°")
        print(f"   Altitude: {info['altitude_km']:.1f} km")
        
        print(f"\n🌍 ISS is currently over: {info['current_latitude']:.1f}°N, {info['current_longitude']:.1f}°E")
        
    # 4. Launch full dashboard
    print(f"\n📊 LAUNCHING MISSION CONTROL DASHBOARD...")
    dashboard = SatelliteDashboard()
    dashboard.create_comprehensive_dashboard(predictor, list(satellites.keys())[:3], duration_hours=4)
    
    print("\n✅ DEMO COMPLETE!")
    print("🎯 You just tracked real satellites with professional accuracy!")

if __name__ == "__main__":
    main()