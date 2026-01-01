import pytest
import pygame
from utils.effects import Effects


def test_effects_apply_scanlines():
    """Test that scanlines effect can be applied to a surface"""
    pygame.init()
    surface = pygame.Surface((100, 100))
    surface.fill((0, 255, 0))

    # Should not raise an exception
    Effects.apply_scanlines(surface)

    pygame.quit()


def test_effects_scanlines_darkens_lines():
    """Test that scanlines actually darken alternating lines"""
    pygame.init()
    surface = pygame.Surface((100, 100))
    surface.fill((100, 100, 100))

    Effects.apply_scanlines(surface, intensity=0.3, spacing=2)

    # Line 0 should have a scanline (darkened)
    # Line 1 should NOT have a scanline (original brightness)
    scanline = surface.get_at((50, 0))  # This line has scanline
    normal_line = surface.get_at((50, 1))  # This line is normal

    # Scanline should be darker than normal line
    assert scanline.r < normal_line.r
    assert scanline.r < 100  # Should be darker than original
    assert normal_line.r == 100  # Should still be original

    pygame.quit()


def test_effects_scanlines_configurable_spacing():
    """Test that scanline spacing can be configured"""
    pygame.init()
    surface = pygame.Surface((100, 100))

    # Should accept spacing parameter
    Effects.apply_scanlines(surface, spacing=3)

    pygame.quit()
