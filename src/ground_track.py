"""
Ground Track Module
Calculates and visualizes satellite ground tracks (where satellites pass over Earth)
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import Tuple, List

class GroundTrackCalculator:
    """
    Calculates satellite ground tracks and creates map visualizations
    """
    
    def __init__(self):
        self.earth_radius = 6371  # km
    
    def calculate_ground_track(self, predictor, satellite_name: str, 
                             duration_hours: float = 3, points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate latitude/longitude ground track
        
        Returns:
            (latitudes, longitudes) arrays in degrees
        """
        if satellite_name not in predictor.satellites:
            raise ValueError(f"Satellite '{satellite_name}' not found")
        
        satellite = predictor.satellites[satellite_name]
        
        # Create time array
        start_time = datetime.utcnow()
        time_deltas = np.linspace(0, duration_hours, points)
        
        latitudes = []
        longitudes = []
        
        for delta in time_deltas:
            dt = start_time + timedelta(hours=delta)
            t = predictor.ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
            
            geocentric = satellite.at(t)
            subpoint = geocentric.subpoint()
            
            latitudes.append(subpoint.latitude.degrees)
            longitudes.append(subpoint.longitude.degrees)
        
        return np.array(latitudes), np.array(longitudes)
    
    def plot_ground_track_simple(self, latitudes: np.ndarray, longitudes: np.ndarray, 
                               satellite_name: str):
        """
        Simple ground track plot using matplotlib
        """
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Plot world map outline
        ax.plot([-180, 180, 180, -180, -180], [-90, -90, 90, 90, -90], 'k-', linewidth=1)
        ax.plot([0, 0], [-90, 90], 'k--', alpha=0.3)  # Prime meridian
        ax.plot([-180, 180], [0, 0], 'k--', alpha=0.3)  # Equator
        
        # Plot ground track
        ax.plot(longitudes, latitudes, 'r-', linewidth=2, label=f'{satellite_name} Ground Track')
        
        # Mark current position (first point)
        ax.plot(longitudes[0], latitudes[0], 'ro', markersize=10, label='Current Position')
        
        # Mark future positions
        ax.scatter(longitudes[1:], latitudes[1:], c='orange', s=20, alpha=0.6, label='Future Positions')
        
        # Set labels and limits
        ax.set_xlabel('Longitude (°)')
        ax.set_ylabel('Latitude (°)')
        ax.set_xlim(-180, 180)
        ax.set_ylim(-90, 90)
        ax.grid(True, alpha=0.3)
        ax.set_title(f'{satellite_name} - Ground Track Over Earth')
        ax.legend()
        
        plt.tight_layout()
        plt.show()
        
        return fig, ax
    
    def analyze_coverage(self, latitudes: np.ndarray, longitudes: np.ndarray) -> dict:
        """
        Analyze ground track coverage statistics
        """
        return {
            'max_latitude': np.max(latitudes),
            'min_latitude': np.min(latitudes),
            'latitude_range': np.max(latitudes) - np.min(latitudes),
            'longitude_span': np.max(longitudes) - np.min(longitudes),
            'equatorial_crossings': np.sum(np.diff(np.sign(latitudes)) != 0),
            'total_points': len(latitudes)
        }