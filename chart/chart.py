import pygame
import sys
import math

class chart:        

    # Initialize pygame
    pygame.init()
    
    def get_star_phase(age):
        """
        Determines the phase of a star's life based on its age.
        
        Parameters:
        age (float): The age of the star in billions of years.
        
        Returns:
        str: The phase of the star's life.
        """
        if age < 0.01:
            return "Protostar"
        elif age < 10:
            return "Main Sequence"
        elif age < 12:
            return "Red Giant"
        elif age < 14:
            return "Planetary Nebula"
        else:
            return "White Dwarf"
        
    
    """
    method to calculate energy produced per second with e=mc^2
    
    parameters:
    mass per second (kg)
    """
    def calculate_energy(mass):
        # Speed of light in meters per second
        c = 3 * 10**8
        # Energy formula
        energy = mass * c**2
        return energy
    
    """
    determines gamma factor

    parameters:
    mass (kg), radius (meters)

    returns: gamma factor
    """
    def calculate_gamma(mass, radius):
        c = 3 * 10**8
        gamma = 1 / math.sqrt(1 - (2 * 6.67 * 10**-11 * mass) / (radius * c**2))
        return gamma

    # Screen dimensions
    WIDTH, HEIGHT = 600,400

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Create the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Info chart or wtv")

    # Clock to control frame rate
    clock = pygame.time.Clock()

    # Square properties
    rectangle_base = 180
    rectangle_height = 110
    x, y = 410, 10

    # Font for labels
    font = pygame.font.Font(None, 16)  # Default font with size 36

    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Drawing
        screen.fill(WHITE)  # Clear the screen

        pygame.draw.rect(screen, BLACK, (x, y, rectangle_base, rectangle_height))

        # Create the label
        stage_label = font.render("Stage: " + get_star_phase(5), True, WHITE)  # Render text
        stage_label_rect = stage_label.get_rect(topleft=(x + 5, y + 5)) # stage label position
        energy_label = font.render("Energy per second (E = mc^2):", True, WHITE)
        energy_label_rect = energy_label.get_rect(topleft=(x + 5, y + 35)) # energy label position
        energy_result_label = font.render(str(calculate_energy(4.28*10**9)), True, WHITE)
        energy_result_label_rect = energy_result_label.get_rect(topleft=(x+5, y+50))
        time_dilation_label = font.render("Gamma factor:", True, WHITE)
        time_dilation_label_rect = time_dilation_label.get_rect(topleft=(x + 5, y + 80)) # time dilation label position
        gamma_result_label = font.render(str(calculate_gamma(1.9 * 10**30, 6.96 * 10**8)), True, WHITE)
        gamma_result_label_rect = energy_result_label.get_rect(topleft=(x+5, y+95))

        # Draw the label
        screen.blit(stage_label, stage_label_rect) 
        screen.blit(energy_label, energy_label_rect)
        screen.blit(energy_result_label, energy_result_label_rect)
        screen.blit(time_dilation_label, time_dilation_label_rect)
        screen.blit(gamma_result_label, gamma_result_label_rect)

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Maintain 60 FPS

    # Quit pygame
    pygame.quit()
    sys.exit()
