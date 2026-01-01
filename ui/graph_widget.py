from ui.widget import Widget
from utils.ring_buffer import RingBuffer
import pygame

class GraphWidget(Widget):
    """Widget for displaying a graph of data over time"""

    def __init__(self, x, y, width, height, max_samples=100, color=(0, 0, 0)):
        super().__init__(x, y, width, height)
        self.max_samples = max_samples
        self.buffer = RingBuffer(max_samples)
        self.color = color
        self.min_value = 0
        self.max_value = 100  # Default range for percentages

    def update(self, data):
        """Add data point to the graph buffer"""
        if data is None:
            return
        self.buffer.append(data)

    def render(self, surface):
        """Render the graph as a line on the surface"""
        # Draw background/border
        pygame.draw.rect(surface, (0, 40, 0), self.rect, 1)  # Dark green border

        # Get all data points
        data_points = list(self.buffer.get_all())

        if len(data_points) < 2:
            return  # Need at least 2 points to draw a line

        # Calculate scaling factors
        x_scale = self.width / (self.max_samples - 1)
        y_scale = self.height / (self.max_value - self.min_value)

        # Convert data points to screen coordinates
        points = []
        for i, value in enumerate(data_points):
            # Clamp value to min/max range
            clamped = max(self.min_value, min(self.max_value, value))

            # Calculate screen position
            x = self.x + (i * x_scale)
            # Flip y-axis (pygame y increases downward)
            y = self.y + self.height - ((clamped - self.min_value) * y_scale)

            points.append((x, y))

        # Draw the line graph
        if len(points) >= 2:
            pygame.draw.lines(surface, self.color, False, points, 2)
