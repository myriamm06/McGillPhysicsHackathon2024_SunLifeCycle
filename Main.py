import pygame
import sys
from Slider import Slider
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from Chart import Chart

# Main application class
class Main:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Sun Temperature vs Time")
        self.font = pygame.font.Font(None, 36)

        # Slider setup for time (from 0 to 15 billion years)
        self.slider = Slider(100, 500, 600, 0, 15_000_000_000, self.screen)  # 0 to 15 billion years
        # Chart
        self.chart = Chart(self.screen)
        # Matplotlib Figure for the graph
        self.figure = Figure(figsize=(5.2, 4), dpi=80)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Temperature of the Sun's Surface vs Time")
        self.ax.set_xlabel("Time (Years)")
        self.ax.set_ylabel("Temperature (K)")
        self.ax.grid(True)
        self.time_values = []  # x-axis values
        self.temp_values = []  # y-axis values
        self.canvas = FigureCanvas(self.figure)
        self.running = True

    def calculate_temperature(self, time):
        """
        Simulates the temperature of the Sun's surface over time (simplified).
        :param time: Time in years
        :return: Temperature in Kelvin
        """
        if time < 1e7:  # Protostar
            return 3000 + 1000 * (time / 1e7)
        elif time < 1e10:  # Main Sequence
            return 5778  # Stable at ~5778K
        elif time < 1.2e10:  # Red Giant
            return 4500
        elif time < 1.3e10:  # Planetary Nebula
            return 8000
        else:  # White Dwarf
            return 3000

    def draw_graph(self):
        """
        Draw the graph on the Pygame surface.
        """
        # Clear previous plot
        self.ax.clear()
        self.ax.set_title("Temperature of the Sun's Surface vs Time")
        self.ax.set_xlabel("Time (Years)")
        self.ax.set_ylabel("Temperature (K)")
        self.ax.grid(True)

        # Plot the data
        self.ax.plot(self.time_values, self.temp_values, color="orange")

        # Render the Matplotlib figure to a Pygame surface
        self.canvas.draw()
        raw_data = self.canvas.buffer_rgba()
        plot_surface = pygame.image.frombuffer(raw_data, self.canvas.get_width_height(), "RGBA")
        self.screen.blit(plot_surface, (0, 0))

    def run(self):
        # Main Loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.slider.handle_event(event)

            # Get the slider value and calculate temperature
            current_time = self.slider.current_value  # Time in years
            current_temp = self.calculate_temperature(current_time)

            # Update the data for the graph
            self.time_values.append(current_time)
            self.temp_values.append(current_temp)

            # Ensure the graph only animates a specific range of values (limited to 200 points for smooth animation)
            if len(self.time_values) > 200:
                self.time_values.pop(0)
                self.temp_values.pop(0)

            # Draw the background and graph
            self.screen.fill((0,0,0))
            self.slider.draw(self.font)
            self.draw_graph()
            
            # Draw the chart
            age = self.slider.current_value
            self.chart.draw(age)
            pygame.display.flip()

        pygame.quit()
        sys.exit()


# Run the application
if __name__ == "__main__":
    app = Main()
    app.run()
