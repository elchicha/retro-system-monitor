import pytest
import pygame
from ui.widget import Widget


class MockWidget(Widget):
    """Concrete widget for testing abstract base class"""

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.update_called = False
        self.render_called = False

    def update(self, data=None):
        self.update_called = True
        self.data = data

    def render(self, surface):
        self.render_called = True


def test_widget_initialization():
    """Test that widget initializes with position and size"""
    widget = MockWidget(10, 20, 100, 50)

    assert widget.x == 10
    assert widget.y == 20
    assert widget.width == 100
    assert widget.height == 50


def test_widget_has_rect():
    """Test that widget has a pygame Rect for positioning"""
    widget = MockWidget(10, 20, 100, 50)

    assert hasattr(widget, "rect")
    assert widget.rect.x == 10
    assert widget.rect.y == 20
    assert widget.rect.width == 100
    assert widget.rect.height == 50


def test_widget_update_must_be_implemented():
    """Test that update is an abstract method"""
    widget = MockWidget(0, 0, 10, 10)

    # Should be able to call it
    widget.update({"test": 123})
    assert widget.update_called is True
    assert widget.data == {"test": 123}


def test_widget_render_must_be_implemented():
    """Test that render is an abstract method"""
    pygame.init()
    widget = MockWidget(0, 0, 10, 10)
    surface = pygame.Surface((100, 100))

    # Should be able to call it
    widget.render(surface)
    assert widget.render_called is True

    pygame.quit()
