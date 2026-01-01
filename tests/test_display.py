import pytest
import pygame
from ui.display import Display


def test_display_initialization():
    """Test that display initializes with correct dimensions"""
    display = Display(width=800, height=600)

    assert display.width == 800
    assert display.height == 600
    assert display.screen is not None


def test_display_has_clock():
    """Test that display has a clock for frame rate control"""
    display = Display()

    assert display.clock is not None
    assert isinstance(display.clock, pygame.time.Clock)


def test_display_default_dimensions():
    """Test that display has sensible defaults"""
    display = Display()

    assert display.width > 0
    assert display.height > 0


def test_display_initialization():
    """Test that display initializes with correct dimensions"""
    display = Display(width=800, height=600)

    assert display.width == 800
    assert display.height == 600
    assert display.screen is not None
    display.quit()


def test_display_has_clock():
    """Test that display has a clock for frame rate control"""
    display = Display()

    assert display.clock is not None
    assert isinstance(display.clock, pygame.time.Clock)
    display.quit()


def test_display_default_dimensions():
    """Test that display has sensible defaults"""
    display = Display()

    assert display.width > 0
    assert display.height > 0
    display.quit()


def test_display_starts_running():
    """Test that display running flag starts as True"""
    display = Display()

    assert display.running is True
    display.quit()


def test_display_quit_event_stops_running():
    """Test that QUIT event sets running to False"""
    display = Display()

    # Simulate a QUIT event
    quit_event = pygame.event.Event(pygame.QUIT)
    pygame.event.post(quit_event)

    display.handle_events()

    assert display.running is False
    display.quit()


def test_display_clear_fills_screen():
    """Test that clear method fills screen with color"""
    display = Display(width=100, height=100)

    # Clear with a specific color
    test_color = (255, 0, 0)
    display.clear(test_color)

    # Check a pixel to verify the color
    pixel_color = display.screen.get_at((50, 50))
    assert pixel_color[:3] == test_color  # Compare RGB, ignore alpha

    display.quit()


def test_display_tick_controls_framerate():
    """Test that tick method exists and can be called"""
    display = Display()

    # Should not raise an exception
    display.tick(60)

    display.quit()


def test_display_caption_is_set():
    """Test that window caption is set correctly"""
    display = Display()

    caption = pygame.display.get_caption()[0]
    assert caption == "Retro System Monitor"

    display.quit()


def test_display_screen_surface_type():
    """Test that screen is a pygame Surface"""
    display = Display()

    assert isinstance(display.screen, pygame.Surface)

    display.quit()


def test_display_update_flips_display():
    """Test that update method flips the pygame display"""
    display = Display()

    # Should not raise an exception
    display.update()

    # We can't easily test if flip was called without mocking,
    # but we can verify the method exists and runs
    assert hasattr(display, "update")

    display.quit()
