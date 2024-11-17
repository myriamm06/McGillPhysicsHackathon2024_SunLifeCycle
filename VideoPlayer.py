import pygame
import sys
from moviepy.editor import VideoFileClip
from PIL import Image

class VideoPlayer:
    def __init__(self, video_path, width=800, height=600):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Video Player with Time Control Slider")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.SLIDER_COLOR = (0, 128, 255)
        self.BUTTON_COLOR = (0, 128, 255)
        self.BUTTON_TEXT_COLOR = self.WHITE

        # Button properties
        self.button_width = 100
        self.button_height = 40
        self.play_button_rect = pygame.Rect(100, 500, self.button_width, self.button_height)
        self.pause_button_rect = pygame.Rect(250, 500, self.button_width, self.button_height)
        self.rewind_button_rect = pygame.Rect(400, 500, self.button_width, self.button_height)

        # Slider properties
        self.slider_width = 600
        self.slider_height = 20
        self.slider_x = 10
        self.slider_y = 550
        self.slider_handle_width = 20

        # Load the video using moviepy
        self.clip = VideoFileClip(video_path)
        self.clip = self.clip.resize(width=500)
        self.clip = self.clip.resize(height=500)
        self.clip_duration = self.clip.duration  # Get the total duration of the video
        self.clip = self.clip.rotate(90)

        # Initial slider value
        self.slider_value = 0
        self.slider_handle_x = self.slider_x
        self.video_time = 0
        self.is_playing = True

        # Set up the clock
        self.clock = pygame.time.Clock()

        # Flag to track if user is dragging the slider handle
        self.dragging = False

    def get_video_time(self, slider_position):
        return (slider_position - self.slider_x) / self.slider_width * self.clip_duration

    def draw_button(self, rect, text):
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, rect)
        font = pygame.font.SysFont(None, 30)
        text_surface = font.render(text, True, self.BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Mouse button press (start dragging)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Check if Play button is clicked
                if self.play_button_rect.collidepoint(mouse_x, mouse_y):
                    self.is_playing = True

                # Check if Pause button is clicked
                if self.pause_button_rect.collidepoint(mouse_x, mouse_y):
                    self.is_playing = False

                # Check if Rewind button is clicked
                if self.rewind_button_rect.collidepoint(mouse_x, mouse_y):
                    self.video_time = 0
                    self.slider_handle_x = self.slider_x

                # Check if the slider is clicked
                if self.slider_x <= mouse_x <= self.slider_x + self.slider_width and self.slider_y <= mouse_y <= self.slider_y + self.slider_height:
                    # Check if the mouse is on the handle
                    if self.slider_handle_x <= mouse_x <= self.slider_handle_x + self.slider_handle_width:
                        self.dragging = True

            # Mouse motion (dragging the slider handle)
            if event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    mouse_x, _ = event.pos
                    # Constrain the handle within the slider range
                    self.slider_handle_x = max(self.slider_x, min(mouse_x - self.slider_handle_width // 2, self.slider_x + self.slider_width - self.slider_handle_width))

                    # Update the video time based on slider position
                    self.video_time = self.get_video_time(self.slider_handle_x)
                    self.is_playing = False

            # Mouse button release (stop dragging)
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

        return True  # Return True if the game should keep running

    def update(self):
        if self.is_playing:
            self.video_time += 1 / 30  # Increment by frame duration (30 FPS)
            if self.video_time >= self.clip_duration:
                self.video_time = self.clip_duration
                self.is_playing = False

        # Update slider handle position
        self.slider_handle_x = self.slider_x + (self.video_time / self.clip_duration) * self.slider_width

    def draw_ui(self):
        # Draw the buttons
        self.draw_button(self.play_button_rect, "Play")
        self.draw_button(self.pause_button_rect, "Pause")
        self.draw_button(self.rewind_button_rect, "Rewind")

        # Draw the slider background (gray bar)
        pygame.draw.rect(self.screen, self.GRAY, (self.slider_x, self.slider_y, self.slider_width, self.slider_height))

        # Draw the slider handle (blue rectangle)
        pygame.draw.rect(self.screen, self.SLIDER_COLOR, (self.slider_handle_x, self.slider_y - 5, self.slider_handle_width, self.slider_height + 10))

        # Display the slider value (time) on the screen
        font = pygame.font.SysFont(None, 30)
        time_text = font.render(f'Time: {self.video_time:.2f}s', True, self.BLACK)
        self.screen.blit(time_text, (self.slider_x + self.slider_width + 20, self.slider_y))

    def render_video_frame(self):
        # Get the video frame at the current time and display it
        subclip = self.clip.subclip(self.video_time, min(self.video_time + 0.04, self.clip_duration))  # Extract 40ms subclip
        frame = subclip.get_frame(0)  # Get the frame at the start of the subclip

        # Convert video frame to Pygame surface
        frame_surface = pygame.surfarray.make_surface(frame)

        # Display the frame on the screen
        self.screen.blit(frame_surface, (0, 0))

    def run(self):
        running = True
        while running:
            self.screen.fill(self.WHITE)

            # Handle events
            running = self.handle_events()

            if not running:
                break

            # Update video time and slider position
            self.update()

            # Draw the UI (buttons, slider, time)
            self.draw_ui()

            # Render the current video frame
            self.render_video_frame()

            # Update the display
            pygame.display.flip()

            # Control the frame rate
            self.clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    video_path = "TakeOffCopy.mp4"  # Replace with your video file path
    player = VideoPlayer(video_path)
    player.run()
