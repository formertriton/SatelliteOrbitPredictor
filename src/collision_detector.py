"""
Collision Detection Module
Analyzes potential collisions between satellites and space debris
"""

import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import matplotlib.pyplot as plt

class CollisionDetector:
    """
    Detects potential satellite collisions and close approaches
    """
    
    def __init__(self, warning_distance_km: float = 10.0):
        self.warning_distance_km = warning_distance_km
        self.earth_radius = 6371  # km
    
    def calculate_distance(self, pos1: Tuple[float, float, float], 
                          pos2: Tuple[float, float, float]) -> float:
        """
        Calculate 3D distance between two satellite positions
        """
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2
        return np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
    
    def analyze_close_approach(self, predictor, sat1_name: str, sat2_name: str,
                             duration_hours: float = 24, points: int = 200) -> Dict:
        """
        Analyze potential close approaches between two satellites
        
        Returns:
            Dictionary with collision analysis results
        """
        # Generate orbital paths for both satellites
        try:
            x1, y1, z1 = predictor.generate_orbit_path(sat1_name, duration_hours, points)
            x2, y2, z2 = predictor.generate_orbit_path(sat2_name, duration_hours, points)
        except Exception as e:
            return {'error': f"Could not generate orbits: {e}"}
        
        # Calculate distances at each time point
        distances = []
        times = []
        start_time = datetime.utcnow()
        
        for i in range(len(x1)):
            pos1 = (x1[i], y1[i], z1[i])
            pos2 = (x2[i], y2[i], z2[i])
            distance = self.calculate_distance(pos1, pos2)
            distances.append(distance)
            
            # Calculate corresponding time
            time_delta = (duration_hours * i / points)
            times.append(start_time + timedelta(hours=time_delta))
        
        distances = np.array(distances)
        
        # Find closest approach
        min_distance_idx = np.argmin(distances)
        min_distance = distances[min_distance_idx]
        closest_time = times[min_distance_idx]
        
        # Find all close approaches within warning distance
        warning_indices = np.where(distances < self.warning_distance_km)[0]
        
        # Calculate relative velocity at closest approach
        if min_distance_idx > 0 and min_distance_idx < len(distances) - 1:
            # Simple velocity approximation
            dt = duration_hours / points  # hours
            dt_seconds = dt * 3600  # convert to seconds
            
            # Distance change rate
            dist_before = distances[min_distance_idx - 1]
            dist_after = distances[min_distance_idx + 1]
            relative_velocity = abs(dist_after - dist_before) / (2 * dt_seconds)  # km/s
        else:
            relative_velocity = 0
        
        return {
            'satellite_1': sat1_name,
            'satellite_2': sat2_name,
            'min_distance_km': min_distance,
            'closest_approach_time': closest_time,
            'relative_velocity_km_s': relative_velocity,
            'collision_risk': 'HIGH' if min_distance < 1 else 'MEDIUM' if min_distance < 5 else 'LOW',
            'warning_periods': len(warning_indices),
            'all_distances': distances,
            'times': times
        }
    
    def plot_collision_analysis(self, analysis_result: Dict):
        """
        Plot collision analysis results
        """
        if 'error' in analysis_result:
            print(f"Error: {analysis_result['error']}")
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Plot 1: Distance over time
        times = analysis_result['times']
        distances = analysis_result['all_distances']
        
        ax1.plot(times, distances, 'b-', linewidth=2, label='Distance Between Satellites')
        ax1.axhline(y=self.warning_distance_km, color='r', linestyle='--', 
                   label=f'Warning Threshold ({self.warning_distance_km} km)')
        
        # Mark closest approach
        min_idx = np.argmin(distances)
        ax1.plot(times[min_idx], distances[min_idx], 'ro', markersize=10, 
                label=f"Closest Approach: {distances[min_idx]:.2f} km")
        
        ax1.set_ylabel('Distance (km)')
        ax1.set_title(f"Collision Analysis: {analysis_result['satellite_1']} vs {analysis_result['satellite_2']}")
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Plot 2: Risk assessment
        risk_colors = {'HIGH': 'red', 'MEDIUM': 'orange', 'LOW': 'green'}
        risk = analysis_result['collision_risk']
        
        ax2.bar(['Collision Risk'], [1], color=risk_colors[risk], alpha=0.7)
        ax2.set_ylabel('Risk Level')
        ax2.set_title(f'Risk Assessment: {risk}')
        ax2.text(0, 0.5, f"Min Distance: {analysis_result['min_distance_km']:.2f} km\n"
                         f"Relative Velocity: {analysis_result['relative_velocity_km_s']:.3f} km/s\n"
                         f"Closest Time: {analysis_result['closest_approach_time'].strftime('%H:%M:%S UTC')}",
                ha='center', va='center', fontsize=12, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        
        return fig
    
    def generate_collision_report(self, analysis_result: Dict) -> str:
        """
        Generate a professional collision assessment report
        """
        if 'error' in analysis_result:
            return f"ERROR: {analysis_result['error']}"
        
        report = f"""
=== SATELLITE COLLISION ANALYSIS REPORT ===

Satellites Analyzed:
- Primary: {analysis_result['satellite_1']}
- Secondary: {analysis_result['satellite_2']}

COLLISION ASSESSMENT:
- Risk Level: {analysis_result['collision_risk']}
- Minimum Distance: {analysis_result['min_distance_km']:.2f} km
- Time of Closest Approach: {analysis_result['closest_approach_time'].strftime('%Y-%m-%d %H:%M:%S UTC')}
- Relative Velocity: {analysis_result['relative_velocity_km_s']:.3f} km/s

RECOMMENDATIONS:
"""
        
        if analysis_result['collision_risk'] == 'HIGH':
            report += "• IMMEDIATE ATTENTION REQUIRED\n• Consider avoidance maneuver\n• Continuous monitoring recommended"
        elif analysis_result['collision_risk'] == 'MEDIUM':
            report += "• Increased monitoring recommended\n• Prepare contingency plans\n• Track approach closely"
        else:
            report += "• Normal operations can continue\n• Routine monitoring sufficient"
        
        report += f"\n\nAnalysis completed at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
        
        return report