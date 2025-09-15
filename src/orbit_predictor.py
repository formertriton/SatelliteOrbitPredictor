"""
Orbit Predictor Module
Parses TLE data and predicts satellite positions using SGP4
"""

from skyfield.api import load, EarthSatellite
from skyfield.timelib import Time
from datetime import datetime, timedelta
import numpy as np
from typing import List, Tuple, Dict

class SatelliteOrbitPredictor:
    """
    Handles TLE parsing and orbit prediction using SGP4 model
    """
    
    def __init__(self):
        self.satellites = {}
        self.ts = load.timescale()
    
    def load_tle_file(self, tle_filepath: str) -> Dict[str, EarthSatellite]:
        """
        Load satellites from a TLE file
        """
        print(f"Loading TLE file: {tle_filepath}")
        satellites = load.tle_file(tle_filepath)
        
        # Store satellites by name
        for sat in satellites:
            self.satellites[sat.name] = sat
            
        print(f"Loaded {len(satellites)} satellites")
        return {sat.name: sat for sat in satellites}

    def predict_position(self, satellite_name: str, time_utc: datetime) -> Tuple[float, float, float]:
        """
        Predict satellite position at a specific time
        
        Returns:
            (x, y, z) position in kilometers (Earth-centered coordinates)
        """
        if satellite_name not in self.satellites:
            raise ValueError(f"Satellite '{satellite_name}' not found")
        
        satellite = self.satellites[satellite_name]
        t = self.ts.utc(time_utc.year, time_utc.month, time_utc.day, 
                       time_utc.hour, time_utc.minute, time_utc.second)
        
        geocentric = satellite.at(t)
        x, y, z = geocentric.position.km
        
        return x, y, z
    
    def generate_orbit_path(self, satellite_name: str, duration_hours: float = 24, 
                          points: int = 100) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate orbital path for visualization
        """
        if satellite_name not in self.satellites:
            raise ValueError(f"Satellite '{satellite_name}' not found")
        
        satellite = self.satellites[satellite_name]
        
        # Create time array properly
        start_time = datetime.utcnow()
        time_deltas = np.linspace(0, duration_hours, points)
        
        # Calculate positions for all times
        positions = []
        for delta in time_deltas:
            dt = start_time + timedelta(hours=delta)
            t = self.ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
            geocentric = satellite.at(t)
            positions.append(geocentric.position.km)
        
        # Convert to arrays
        positions = np.array(positions)
        x, y, z = positions[:, 0], positions[:, 1], positions[:, 2]
        
        return x, y, z
    
    def get_satellite_info(self, satellite_name: str) -> Dict:
        """
        Get detailed information about a satellite
        """
        if satellite_name not in self.satellites:
            raise ValueError(f"Satellite '{satellite_name}' not found")
        
        satellite = self.satellites[satellite_name]
        
        # Current position
        now = self.ts.now()
        geocentric = satellite.at(now)
        subpoint = geocentric.subpoint()
        
        return {
            'name': satellite.name,
            'norad_id': satellite.model.satnum,
            'current_latitude': subpoint.latitude.degrees,
            'current_longitude': subpoint.longitude.degrees,
            'altitude_km': subpoint.elevation.km,
            'epoch': satellite.epoch.utc_iso()
        }