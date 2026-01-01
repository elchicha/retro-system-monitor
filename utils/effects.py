import pygame


class Effects:
    """Visual effects for retro styling"""

    @staticmethod
    def apply_scanlines(surface, intensity=0.3, spacing=2):
        """
        Apply CRT-style scanlines to a surface

        Args:
            surface: pygame Surface to apply effect to
            intensity: How dark the scanlines are (0.0 to 1.0)
            spacing: Pixels between scanlines
        """
        width, height = surface.get_size()

        # Create a semi-transparent black surface for scanlines
        scanline_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        alpha = int(255 * intensity)

        # Draw horizontal lines
        for y in range(0, height, spacing):
            pygame.draw.line(scanline_surface, (0, 0, 0, alpha), (0, y), (width, y), 1)

        # Blit onto the main surface
        surface.blit(scanline_surface, (0, 0))
