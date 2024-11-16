import pygame
import sys
from Slider import Slider
from Stages import Protostar,MainSequence,RedGiant,PlanetaryNebula,WhiteDwarf
from Graph import Graph
import numpy as np
import matplotlib.pyplot as plt
from Chart import Chart
# Main application class
class Main:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600  # Adjusted to fit all components
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Star Simulation")
        self.font = pygame.font.Font(None, 36)

        # Initialize components
        self.slider = Slider(100, 500, 400, 0, 12000000000, self.screen)
        self.graph = Graph()
        self.chart = Chart(self.screen)  # Add the Chart component
        self.running = True
        self.graph_surface = None

    def update_graph(self):
        """Generate the graph and convert it to a Pygame surface."""
        self.graph_surface = self.graph.plot_pressure_profile()

    def run(self):
        self.update_graph()  # Generate the graph before entering the loop

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.slider.handle_event(event)  # Handle slider events

            self.screen.fill((255, 255, 255))  # Clear the screen

            # Draw the graph
            if self.graph_surface:
                self.screen.blit(self.graph_surface, (50, 50))  # Position the graph at (50, 50)

            # Draw the slider
            self.slider.draw(self.font)

            # Draw the chart
            age=self.slider.current_value
            self.chart.draw(age)

            pygame.display.flip()  # Update the display

        pygame.quit()
        sys.exit()





# Run the application
if __name__ == "__main__":
    app = Main()
    app.run()