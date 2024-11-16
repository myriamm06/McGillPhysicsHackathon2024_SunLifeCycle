import pygame
import math

class Chart:
    def __init__(self, screen):
        """
        Initializes the chart object.
        
        Parameters:
        screen (pygame.Surface): The Pygame surface to draw on.
        """
        self.screen = screen

        # Square properties
        self.rectangle_base = 180
        self.rectangle_height = 110
        self.x, self.y = 610, 10  # Chart position

        # Font for labels
        self.font = pygame.font.Font(None, 16)  # Default font with size 16

    def get_star_phase(self, age):
        """
        Determines the phase of a star's life based on its age.
        
        Parameters:
        age (float): The age of the star in billions of years.
        
        Returns:
        str: The phase of the star's life.
        """
        if age < 50000000:
            return "Protostar"
        elif age < 10050000000:
            return "Main Sequence"
        elif age < 11050000000:
            return "Red Giant"
        elif age < 11050010000:
            return "Planetary Nebula"
        else:
            return "White Dwarf"
    
    def calculate_energy(self, mass):
        """
        Calculates energy produced per second using E=mc^2.

        Parameters:
        mass (float): Mass in kilograms.

        Returns:
        float: Energy in Joules.
        """
        c = 299792458  # Speed of light in m/s
        return mass * c**2
    
    def calculate_gamma(self, mass, radius):
        """
        Determines the gamma factor.

        Parameters:
        mass (float): Mass in kilograms.
        radius (float): Radius in meters.

        Returns:
        float: Gamma factor.
        """
        c = 3 * 10**8  # Speed of light in m/s
        return 1 / math.sqrt(1 - (2 * 6.67 * 10**-11 * mass) / (radius * c**2))

    def draw(self, years):
        """
        Draws the info chart on the screen.
        """
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        # Draw the rectangle
        pygame.draw.rect(self.screen, BLACK, (self.x, self.y, self.rectangle_base, self.rectangle_height))

        # Render the labels
        stage_label = self.font.render("Stage: " + self.get_star_phase(years), True, WHITE)
        energy_label = self.font.render("Energy per second (E = mc^2):", True, WHITE)
        energy_result_label = self.font.render(str(self.calculate_energy(4.28 * 10**9)), True, WHITE)
        time_dilation_label = self.font.render("Gamma factor:", True, WHITE)
        gamma_result_label = self.font.render(str(self.calculate_gamma(1.9 * 10**30, 6.96 * 10**8)), True, WHITE)

        # Blit the labels to the screen
        self.screen.blit(stage_label, (self.x + 5, self.y + 5))
        self.screen.blit(energy_label, (self.x + 5, self.y + 35))
        self.screen.blit(energy_result_label, (self.x + 5, self.y + 50))
        self.screen.blit(time_dilation_label, (self.x + 5, self.y + 80))
        self.screen.blit(gamma_result_label, (self.x + 5, self.y + 95))
