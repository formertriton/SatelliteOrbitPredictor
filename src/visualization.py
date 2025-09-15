"""
3D Satellite Orbit Visualization Module
Creates interactive 3D plots of satellite orbits around Earth
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from typing import List, Tuple, Dict
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

class SatelliteVisualizer:
    """
    Creates 3D visualizations of satellite orbits
    """
    
    def __init__(self, figsize: Tuple[int, int] = (12, 10)):
        self.figsize = figsize
        self.earth_radius = 6371  # km
        
    def create_earth_sphere(self, ax, radius: float = None):
        """
        Create a 3D sphere representing Earth
        """
        if radius is None:
            radius = self.earth_radius
            
        # Create sphere coordinates
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        x = radius * np.outer(np.cos(u), np.sin(v))
        y = radius * np.outer(np.sin(u), np.sin(v))
        z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Plot Earth as blue sphere
        ax.plot_surface(x, y, z, color='lightblue', alpha=0.6)
        
    def plot_satellite_orbit(self, orbit_data: Dict[str, Tuple], 
                           title: str = "Satellite Orbits"):
        """
        Plot multiple satellite orbits in 3D
        
        Args:
            orbit_data: Dict with satellite names as keys and (x, y, z) arrays as values
            title: Plot title
        """
        fig = plt.figure(figsize=self.figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        # Create Earth
        self.create_earth_sphere(ax)
        
        # Color palette for different satellites
        colors = ['red', 'green', 'orange', 'purple', 'yellow', 'cyan', 'magenta']
        
        # Plot each satellite orbit
        for i, (sat_name, (x, y, z)) in enumerate(orbit_data.items()):
            color = colors[i % len(colors)]
            ax.plot(x, y, z, color=color, linewidth=2, label=sat_name)
            
            # Mark current position
            ax.scatter(x[0], y[0], z[0], color=color, s=100, marker='o')
        
        # Set labels and title
        ax.set_xlabel('X (km)')
        ax.set_ylabel('Y (km)')
        ax.set_zlabel('Z (km)')
        ax.set_title(title)
        
        # Set equal aspect ratio
        max_range = np.array([x.max()-x.min(), y.max()-y.min(), z.max()-z.min()]).max() / 2.0
        mid_x = (x.max()+x.min()) * 0.5
        mid_y = (y.max()+y.min()) * 0.5
        mid_z = (z.max()+z.min()) * 0.5
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)
        
        # Add legend
        ax.legend()
        
        # Show plot
        plt.tight_layout()
        plt.show()
        
        return fig, ax
    
    def plot_single_satellite(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, 
                            satellite_name: str):
        """
        Plot a single satellite's orbit with enhanced details
        """
        fig = plt.figure(figsize=self.figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        # Create Earth
        self.create_earth_sphere(ax)
        
        # Plot orbit path
        ax.plot(x, y, z, color='red', linewidth=3, label=f'{satellite_name} Orbit')
        
        # Mark current position (first point)
        ax.scatter(x[0], y[0], z[0], color='red', s=200, marker='o', label='Current Position')
        
        # Mark future positions
        ax.scatter(x[1:], y[1:], z[1:], color='orange', s=20, alpha=0.6)
        
        # Calculate and display orbital info
        orbital_radius = np.sqrt(x**2 + y**2 + z**2)
        altitude = orbital_radius - self.earth_radius
        
        ax.set_title(f'{satellite_name}\nAltitude: {altitude[0]:.1f} km')
        ax.set_xlabel('X (km)')
        ax.set_ylabel('Y (km)')
        ax.set_zlabel('Z (km)')
        
        # Set viewing limits
        max_coord = max(np.max(np.abs(x)), np.max(np.abs(y)), np.max(np.abs(z)))
        ax.set_xlim(-max_coord, max_coord)
        ax.set_ylim(-max_coord, max_coord)
        ax.set_zlim(-max_coord, max_coord)
        
        ax.legend()
        plt.tight_layout()
        plt.show()
        
        return fig, ax