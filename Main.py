import pygame
import sys
from Slider import Slider
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from Chart import Chart
from Graph import Graph
from PIL import Image
from moviepy.editor import VideoFileClip
from BackgroundVideo import BackgroundVideo
# Main application class
class Main:
    def __init__(self,video_path,fps = 30):
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
        self.video_path = video_path
        self.screen_width = self.WIDTH
        self.screen_height = self.HEIGHT
        self.fps = fps

        # Load the video clip
        self.clip = VideoFileClip(video_path)
        self.clip = self.clip.resize((self.WIDTH, self.HEIGHT))  # Resize video to fit the screen
        self.clip_duration = self.clip.duration  # Duration of the video

                # Initialize Pygame and mixer
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()  # Initialize pygame after preinitializing the mixer

        # Load and play background music
        self.background_music = pygame.mixer.Sound("background_music.ogg")
        self.background_music.set_volume(1.0)  # Ensure volume is at maximum
        self.background_music.play(loops=-1)  # Play the music on a loop

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

    def display_image(self, time):
        """
        Load and set the correct image based on the current time.
        """
        if time < 1e7:  # Protostar
            self.image = pygame.image.load("prostar-jwst.jpg")
            self.image = pygame.transform.scale(self.image, (250, 200))
        elif time < 1e10:  # Main Sequence
            self.image = pygame.image.load("sun.jpg")
            self.image = pygame.transform.scale(self.image, (125, 125))
        elif time < 1.2e10:  # Red Giant
            self.image = pygame.image.load("redGiant.jpg")
            self.image = pygame.transform.scale(self.image, (190, 190))
        elif time < 1.3e10:  # Planetary Nebula
            self.image = pygame.image.load("nebula.jpg")
            self.image = pygame.transform.scale(self.image, (200, 150))
        else:  # White Dwarf
            self.image = pygame.image.load("whiteDwarf-nasa.jpg")
            self.image = pygame.transform.scale(self.image, (200, 150))
        
        

        
    def draw_graph(self):
        """
        Draw the graph on the Pygame surface with a black background and white axes/labels.
        """
        # Clear previous plot
        self.ax.clear()
        self.figure.patch.set_facecolor("black")  # Set the figure background to black
        self.ax.set_facecolor("black")  # Set the plot background to black

        # Set title and labels with white text
        self.ax.set_title("Temperature of the Sun's Surface vs Time", color="white")
        self.ax.set_xlabel("Time (Years)", color="white")
        self.ax.set_ylabel("Temperature (K)", color="white")

        # Customize tick labels to be white
        self.ax.tick_params(axis="x", colors="white")
        self.ax.tick_params(axis="y", colors="white")

        # Plot the data with a bright color
        self.ax.plot(self.time_values, self.temp_values, color="orange", label="Temperature (K)")

        # Enable grid with a subtle gray color
        self.ax.grid(color="gray", linestyle="--", linewidth=0.5)

        # Add a legend with white text
        self.ax.legend(facecolor="black", edgecolor="white", labelcolor="white")

        # Render the Matplotlib figure to a Pygame surface
        self.canvas.draw()
        raw_data = self.canvas.buffer_rgba()
        plot_surface = pygame.image.frombuffer(raw_data, self.canvas.get_width_height(), "RGBA")
        self.screen.blit(plot_surface, (50, 50))  # Adjust position as needed


    def update_graph(self):
        """Generate the graph and convert it to a Pygame surface."""
        self.graph_surface = self.graph.plot_pressure_profile()

    def run(self):
        video_time = 0
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
            if len(self.time_values) > 75:
                self.time_values.pop(0)
                self.temp_values.pop(0)

            # Video
            self.screen.fill((0,0,0))

            video_time += 1 / self.fps
            if video_time >= self.clip_duration:
                video_time = 0
            subclip = self.clip.subclip(video_time, min(video_time + 1 / self.fps, self.clip_duration))
            frame = subclip.get_frame(0)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0,1))
            self.screen.blit(frame_surface, (0,0))
            # Draw the background and graph
            
            self.slider.draw(self.font)
            self.draw_graph()
            
            # Draw the chart
            self.chart.draw(current_time, temperature=current_temp)

            # Display the image at a specific position
            self.display_image(current_time)
            self.screen.blit(self.image, (500, 250))  # Position the image
            pygame.display.flip()
            
        self.background_music.stop()
        pygame.quit()
        sys.exit()


# Run the application
if __name__ == "__main__":
    app = Main(video_path="IMG_1068.MOV")
    app.run()
