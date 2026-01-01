import pygame
from typing import Tuple


class Display:
    """Class for handling display operations"""

    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Retro System Monitor")
        self.clock = pygame.time.Clock()
        self.running = True


    def quit(self):
        """Quit the display and clean up resources"""
        pygame.quit()
        self.running = False

    def handle_events(self):
        """Handle pygame events for display operations"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

    def clear(self, color=(0,0,0)):
        """Clear the display with a specified color"""
        self.screen.fill(color)

    def update(self):
        """Update the display by flipping the screen buffer"""
        pygame.display.flip()

    def tick(self, frame_rate=60):
        """Update the display and handle frame rate"""
        self.clock.tick(frame_rate)

    def is_running(self):
        """Check if the display is still running"""
        return self.running
