"""
Satellite Performance Dashboard
Comprehensive satellite tracking and analysis system
"""

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import matplotlib.patches as patches

class SatelliteDashboard:
    """
    Creates comprehensive satellite tracking dashboard
    """
    
    def __init__(self):
        self.earth_radius = 6371  # km
        
    def create_comprehensive_dashboard(self, predictor, satellites_to_track: List[str], 
                                     duration_hours: float = 6):
        """
        Create a comprehensive multi-panel dashboard
        """
        # Create figure with subplots
        fig = plt.figure(figsize=(20, 12))
        gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
        
        # Panel 1: 3D Orbital View (top-left, large)
        ax1 = fig.add_subplot(gs[0:2, 0:2], projection='3d')
        self._plot_3d_orbits(ax1, predictor, satellites_to_track, duration_hours)
        
        # Panel 2: Ground Track (top-right)
        ax2 = fig.add_subplot(gs[0, 2])
        self._plot_ground_tracks(ax2, predictor, satellites_to_track[0] if satellites_to_track else None)
        
        # Panel 3: Altitude Profile (middle-right)
        ax3 = fig.add_subplot(gs[1, 2])
        self._plot_altitude_profiles(ax3, predictor, satellites_to_track)
        
        # Panel 4: Satellite Status Table (bottom-left)
        ax4 = fig.add_subplot(gs[2, 0])
        self._create_status_table(ax4, predictor, satellites_to_track)
        
        # Panel 5: Orbital Elements (bottom-middle)
        ax5 = fig.add_subplot(gs[2, 1])
        self._plot_orbital_elements(ax5, predictor, satellites_to_track)
        
        # Panel 6: Coverage Analysis (bottom-right)
        ax6 = fig.add_subplot(gs[2, 2])
        self._plot_coverage_analysis(ax6, predictor, satellites_to_track)
        
        # Main title
        fig.suptitle('🛰️ SATELLITE TRACKING DASHBOARD - REAL TIME SPACE SITUATIONAL AWARENESS', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        # Add timestamp
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        fig.text(0.02, 0.02, f'Generated: {timestamp}', fontsize=10, alpha=0.7)
        
        plt.show()
        return fig
    
    def _plot_3d_orbits(self, ax, predictor, satellites, duration_hours):
        """3D orbital visualization panel"""
        # Create Earth sphere
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 30)
        x_earth = self.earth_radius * np.outer(np.cos(u), np.sin(v))
        y_earth = self.earth_radius * np.outer(np.sin(u), np.sin(v))
        z_earth = self.earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(x_earth, y_earth, z_earth, color='lightblue', alpha=0.4)
        
        colors = ['red', 'green', 'orange', 'purple', 'yellow']
        
        for i, sat_name in enumerate(satellites[:5]):
            try:
                x, y, z = predictor.generate_orbit_path(sat_name, duration_hours, 40)
                color = colors[i % len(colors)]
                ax.plot(x, y, z, color=color, linewidth=2, label=sat_name.split()[0])
                ax.scatter(x[0], y[0], z[0], color=color, s=100)
            except:
                continue
        
        ax.set_title('3D Orbital Paths')
        ax.legend(fontsize=8)
        max_range = 20000
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
        ax.set_zlim(-max_range, max_range)
    
    def _plot_ground_tracks(self, ax, predictor, satellite_name):
        """Ground track panel"""
        if not satellite_name:
            ax.text(0.5, 0.5, 'No satellite selected', ha='center', va='center', transform=ax.transAxes)
            return
            
        try:
            from src.ground_track import GroundTrackCalculator
            tracker = GroundTrackCalculator()
            lats, lons = tracker.calculate_ground_track(predictor, satellite_name, 3, 30)
            
            # Simple world outline
            ax.plot([-180, 180, 180, -180, -180], [-90, -90, 90, 90, -90], 'k-', linewidth=1)
            ax.plot([0, 0], [-90, 90], 'k--', alpha=0.3)
            ax.plot([-180, 180], [0, 0], 'k--', alpha=0.3)
            
            ax.plot(lons, lats, 'r-', linewidth=2)
            ax.plot(lons[0], lats[0], 'ro', markersize=8)
            
            ax.set_xlim(-180, 180)
            ax.set_ylim(-90, 90)
            ax.set_title(f'Ground Track\n{satellite_name.split()[0]}')
            ax.grid(True, alpha=0.3)
        except Exception as e:
            ax.text(0.5, 0.5, f'Ground track\nerror: {str(e)[:20]}', ha='center', va='center', transform=ax.transAxes)
    
    def _plot_altitude_profiles(self, ax, predictor, satellites):
        """Altitude profile panel"""
        try:
            colors = ['red', 'green', 'orange', 'purple', 'yellow']
            
            for i, sat_name in enumerate(satellites[:3]):
                try:
                    x, y, z = predictor.generate_orbit_path(sat_name, 3, 30)
                    altitudes = np.sqrt(x**2 + y**2 + z**2) - self.earth_radius
                    time_points = np.linspace(0, 3, len(altitudes))
                    
                    color = colors[i % len(colors)]
                    ax.plot(time_points, altitudes, color=color, linewidth=2, 
                           label=sat_name.split()[0])
                except:
                    continue
            
            ax.set_xlabel('Time (hours)')
            ax.set_ylabel('Altitude (km)')
            ax.set_title('Altitude Profiles')
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=8)
        except:
            ax.text(0.5, 0.5, 'Altitude data\nunavailable', ha='center', va='center', transform=ax.transAxes)
    
    def _create_status_table(self, ax, predictor, satellites):
        """Status table panel"""
        ax.axis('off')
        
        # Create table data
        table_data = [['Satellite', 'Status', 'Altitude']]
        
        for sat_name in satellites[:4]:
            try:
                info = predictor.get_satellite_info(sat_name)
                short_name = sat_name.split()[0]
                status = "ACTIVE"
                altitude = f"{info['altitude_km']:.0f} km"
                table_data.append([short_name, status, altitude])
            except:
                table_data.append([sat_name.split()[0], "ERROR", "N/A"])
        
        # Create table
        table = ax.table(cellText=table_data[1:], colLabels=table_data[0],
                        cellLoc='center', loc='center', cellColours=None)
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)
        
        ax.set_title('Satellite Status')
    
    def _plot_orbital_elements(self, ax, predictor, satellites):
        """Orbital elements visualization"""
        try:
            # Simple orbital period comparison
            periods = []
            names = []
            
            for sat_name in satellites[:4]:
                try:
                    # Rough orbital period calculation
                    x, y, z = predictor.generate_orbit_path(sat_name, 2, 20)
                    altitude = np.mean(np.sqrt(x**2 + y**2 + z**2)) - self.earth_radius
                    # Simplified period calculation
                    period = 2 * np.pi * np.sqrt((self.earth_radius + altitude)**3 / 398600) / 60  # minutes
                    periods.append(period)
                    names.append(sat_name.split()[0])
                except:
                    continue
            
            if periods:
                bars = ax.bar(names, periods, color=['red', 'green', 'orange', 'purple'][:len(periods)])
                ax.set_ylabel('Orbital Period (min)')
                ax.set_title('Orbital Periods')
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
                
                # Add value labels on bars
                for bar, period in zip(bars, periods):
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                           f'{period:.0f}', ha='center', va='bottom', fontsize=8)
        except:
            ax.text(0.5, 0.5, 'Orbital elements\ncalculation error', ha='center', va='center', transform=ax.transAxes)
    
    def _plot_coverage_analysis(self, ax, predictor, satellites):
        """Coverage analysis panel"""
        try:
            # Simple coverage metrics
            coverage_data = []
            labels = []
            
            for sat_name in satellites[:3]:
                try:
                    info = predictor.get_satellite_info(sat_name)
                    # Simple coverage metric based on altitude
                    altitude = info['altitude_km']
                    coverage_area = 2 * np.pi * self.earth_radius * altitude / 1000  # simplified
                    coverage_data.append(coverage_area)
                    labels.append(sat_name.split()[0])
                except:
                    continue
            
            if coverage_data:
                wedges, texts = ax.pie(coverage_data, labels=labels, autopct='%1.1f%%', 
                                     colors=['red', 'green', 'orange'][:len(coverage_data)])
                ax.set_title('Coverage Comparison')
        except:
            ax.text(0.5, 0.5, 'Coverage analysis\nunavailable', ha='center', va='center', transform=ax.transAxes)