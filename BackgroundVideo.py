import pygame
from moviepy.editor import VideoFileClip

class BackgroundVideo:
    def __init__(self, video_path, screen, screen_width=800, screen_height=600, fps=30):
      
        self.video_path = video_path
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fps = fps
        # Load the video clip
        self.clip = VideoFileClip(video_path)
        self.clip = self.clip.resize((screen_width, screen_height))  # Resize video to fit the screen
        self.clip_duration = self.clip.duration  # Duration of the video
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Background Video")
        # Clock to control frame rate
        self.clock = pygame.time.Clock()
    def play(self):
        """
        Play the video in the background.
        """
        running = True
        video_time = 0  # Start at the beginning of the video
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # Update video time
            video_time += 1 / self.fps
            if video_time >= self.clip_duration:
                video_time = 0  # Loop the video
            # Get the video frame at the current time
            subclip = self.clip.subclip(video_time, min(video_time + 1 / self.fps, self.clip_duration))
            frame = subclip.get_frame(0)
            # Convert the video frame to a Pygame surface
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            # Display the video frame on the screen
            self.screen.blit(frame_surface, (0, 0))
            # Update the display
            pygame.display.flip()
            # Control the frame rate
            self.clock.tick(self.fps)
        pygame.quit()