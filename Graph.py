import numpy as np
import matplotlib.pyplot as plt
import pygame
from io import BytesIO

class Graph:
    def __init__(self, mass_sun=1.989e30, radius_sun=6.957e8, density_function=None, resolution=500):
        self.G = 6.67430e-11
        self.M_sun = mass_sun
        self.R_sun = radius_sun
        self.density_function = density_function or self.default_density_function
        self.resolution = resolution
        self.r_values = np.linspace(0.1, self.R_sun, self.resolution)
        self.P_values = np.zeros_like(self.r_values)
    
    def default_density_function(self, r):
        return 1e3 * (1 - r / self.R_sun)
    
    def mass_enclosed(self, r):
        return self.M_sun * (r / self.R_sun)
    
    def pressure_gradient(self, r, P):
        M_r = self.mass_enclosed(r)
        rho_r = self.density_function(r)
        return - (self.G * M_r * rho_r) / r**2

    def solve_equilibrium(self):
        self.P_values[0] = 1e10
        for i in range(1, len(self.r_values)):
            r = self.r_values[i]
            dP = self.pressure_gradient(r, self.P_values[i-1])
            self.P_values[i] = self.P_values[i-1] + dP * (self.r_values[i] - self.r_values[i-1])
    
    def plot_pressure_profile(self):
        """Plot the pressure profile as a Pygame surface."""
        self.solve_equilibrium()
        plt.figure(figsize=(5, 3))  # Aspect ratio matches the screen proportions
        plt.plot(self.r_values, self.P_values, label="Pressure Profile")
        plt.xlabel("Radius (m)")
        plt.ylabel("Pressure (Pa)")
        plt.title("Pressure vs Radius")
        plt.grid(True)
        plt.legend()

        # Save the plot to an in-memory buffer
        buf = BytesIO()
        plt.savefig(buf, format='PNG', bbox_inches='tight')
        buf.seek(0)
        plt.close()  # Close the plt figure to avoid opening new windows

        # Convert the image buffer to a Pygame surface
        return pygame.image.load(buf)

