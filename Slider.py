import pygame
import sys

# Slider class
class Slider:
    def __init__(self, x, y, width, min_value, max_value, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = 5
        self.handle_radius = 15
        self.min_value = min_value
        self.max_value = max_value
        self.handle_x = x + width // 2
        self.current_value = self.calculate_value()
        self.screen = screen
        self.dragging = False

    def calculate_value(self):
        return (self.handle_x - self.x) / self.width * (self.max_value - self.min_value)

    def draw(self, font, ticks=10):
        # Draw the slider
        pygame.draw.rect(self.screen, (200, 200, 200), (self.x, self.y - self.height // 2, self.width, self.height))

        # Draw ticks and numbers
        for i in range(ticks + 1):
            tick_x = self.x + i * (self.width / ticks)
            pygame.draw.line(self.screen, (0, 0, 0), (tick_x, self.y - 10), (tick_x, self.y + 10), 2)
        
            # # Draw numbers
            # tick_value = self.min_value + i * (self.max_value - self.min_value) / ticks
            # number_text = font.render(f"{tick_value:.2e}", True, (0, 0, 0))
            # self.screen.blit(number_text, (tick_x - number_text.get_width() // 2, self.y + 15))

        # Display the current value
        value_text = font.render(f"Age in years: {self.current_value:.2e}", True, (255, 255, 255))
        self.screen.blit(value_text, (self.x + self.width // 2 - value_text.get_width() // 2, self.y - 40))
        pygame.draw.circle(self.screen, (255, 246, 0), (self.handle_x, self.y), self.handle_radius)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                distance = ((event.pos[0] - self.handle_x) ** 2 + (event.pos[1] - self.y) ** 2) ** 0.5
                if distance <= self.handle_radius:
                    self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, _ = event.pos
            self.handle_x = max(self.x, min(mouse_x, self.x + self.width))
            self.current_value = self.calculate_value()
