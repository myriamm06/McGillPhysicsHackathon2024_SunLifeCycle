import pygame
import math

class Chart:
    # Chart constructor
    def __init__(self, screen):
        self.screen = screen

        # Square properties
        self.rectangle_base = 180
        self.rectangle_height = 110
        self.x, self.y = 500, 10  # Chart position

        # Font for labels
        self.font = pygame.font.Font(None, 20) 

    # Get the stage of the sun depending on the time
    def get_star_phase(self, age):
        if age < 1e7:
            return "Protostar"
        elif age < 1e10:
            return "Main Sequence"
        elif age < 1.2e10:
            return "Red Giant"
        elif age < 1.3e10:
            return "Planetary Nebula"
        else:
            return "White Dwarf"
    
    # Calculates the energy of sun
    def calculate_energy(self, age):
        c = 299792458  # Speed of light in m/s
        if age < 1e7:
            return 0
        
        elif age < 1e10:
            return (1.215e28)/365/24/60/60
        
        elif age < 1.2e10:
            return (1.215e31)/365/24/60/60
        
        elif age < 1.3e10:
            0
        
        else:
            return (1.215e25)/365/24/60/60
    
    # Calculates gamma factor
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
        c = 299792458  # Speed of light in m/s
        return 1 / math.sqrt(1 - (2 * 6.67 * 10**-11 * mass) / (radius * c**2))

    # Draw chart on screen
    def draw(self, years,temperature=None):
        
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        # Draw the rectangle
        pygame.draw.rect(self.screen, BLACK, (self.x, self.y, self.rectangle_base, self.rectangle_height))

        # Render the labels
        stage_label = self.font.render("Stage: " + self.get_star_phase(years), True, WHITE)
        energy_label = self.font.render("MegaJoules per second (E = mc^2):", True, WHITE)
        energy_result_label = self.font.render(str(self.calculate_energy(years)), True, WHITE)
        time_dilation_label = self.font.render("Gamma factor:", True, WHITE)
        gamma_result_label = self.font.render(str(self.calculate_gamma(years)), True, WHITE)

        # Blit the labels to the screen
        self.screen.blit(stage_label, (self.x + 5, self.y + 25))
        self.screen.blit(energy_label, (self.x + 5, self.y + 55))
        self.screen.blit(energy_result_label, (self.x + 5, self.y + 70))
        self.screen.blit(time_dilation_label, (self.x + 5, self.y + 100))
        self.screen.blit(gamma_result_label, (self.x + 5, self.y + 115))
        # Render and display the temperature label if provided
        if temperature is not None:
            temp_label = self.font.render(f"Temperature: {temperature:.2f} K", True, WHITE)
            self.screen.blit(temp_label, (self.x + 5, self.y + 135))  # Position below other labels
