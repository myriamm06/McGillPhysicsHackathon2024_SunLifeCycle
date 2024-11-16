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
    
    def calculate_energy(self, age):
        c = 299792458  # Speed of light in m/s
        if age < 50000000:
            return (1.809e27)/365/24/60/60
        
        elif age < 10050000000:
            return (1.215e28)/365/24/60/60
        
        elif age < 11050000000:
            return (1.215e31)/365/24/60/60
        
        elif age < 11050010000:
            return (1.215e25)/365/24/60/60
        
        else:
            return (1.215e25)/365/24/60/60
       
        """
        Calculates energy produced per second using E=mc^2.

        Parameters:
        mass (float): Mass in kilograms.

        Returns:
        float: Energy in Joules.
        """
        

    def calculate_gamma(self, phase_name):

        phase = self.get_star_phase(phase_name)

        if phase == "Protostar":
            mass = 1.989 * 10**30
            radius = 10**11
        elif phase == "Main Sequence":
            mass = 1.989 * 10**30
            radius = 7 * 10**8
        elif phase == "Red Giant":
            mass = 0.65 * 1.989 * 10**30
            radius = 1.5 * 10**11
        elif phase == "Planetary Nebula":
            mass = 0.65 * 1.989 * 10**30
            radius = 5 * 10**15
        elif phase == "White Dwarf":
            mass = 0.5 * 1.989 * 10**30
            radius = 6 * 10**6


        """
        Determines the gamma factor.

        Parameters:
        mass (float): Mass in kilograms.
        radius (float): Radius in meters.

        Returns:
        float: Gamma factor.
        """
        c = 299792458  # Speed of light in m/s
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
        energy_label = self.font.render("MegaJoules per second (E = mc^2):", True, WHITE)
        energy_result_label = self.font.render(f"{self.calculate_energy(years):.2e}", True, WHITE)
        time_dilation_label = self.font.render("Gamma factor:", True, WHITE)
        gamma_result_label = self.font.render(str(self.calculate_gamma(years)), True, WHITE)

        # Blit the labels to the screen
        self.screen.blit(stage_label, (self.x + 5, self.y + 5))
        self.screen.blit(energy_label, (self.x + 5, self.y + 35))
        self.screen.blit(energy_result_label, (self.x + 5, self.y + 50))
        self.screen.blit(time_dilation_label, (self.x + 5, self.y + 80))
        self.screen.blit(gamma_result_label, (self.x + 5, self.y + 95))
