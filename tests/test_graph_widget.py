import pytest
import pygame
from ui.graph_widget import GraphWidget
from utils.ring_buffer import RingBuffer


def test_graph_widget_initialization():
    """Test that graph widget initializes correctly"""
    widget = GraphWidget(x=10, y=20, width=200, height=100, max_samples=50)

    assert widget.x == 10
    assert widget.y == 20
    assert widget.width == 200
    assert widget.height == 100
    assert widget.max_samples == 50


def test_graph_widget_has_ring_buffer():
    """Test that graph widget creates a ring buffer for data"""
    widget = GraphWidget(x=0, y=0, width=100, height=100, max_samples=30)

    assert hasattr(widget, "buffer")
    assert isinstance(widget.buffer, RingBuffer)
    assert widget.buffer.max_size == 30


def test_graph_widget_update_adds_to_buffer():
    """Test that update adds data points to the buffer"""
    widget = GraphWidget(x=0, y=0, width=100, height=100, max_samples=10)

    widget.update(50.0)
    widget.update(75.0)
    widget.update(25.0)

    data = list(widget.buffer.get_all())
    assert len(data) == 3
    assert data == [50.0, 75.0, 25.0]


def test_graph_widget_update_handles_none():
    """Test that update handles None data gracefully"""
    widget = GraphWidget(x=0, y=0, width=100, height=100, max_samples=10)

    widget.update(None)

    data = list(widget.buffer.get_all())
    assert len(data) == 0


def test_graph_widget_render_creates_surface():
    """Test that render draws on the provided surface"""
    pygame.init()
    widget = GraphWidget(x=10, y=10, width=200, height=100, max_samples=10)
    surface = pygame.Surface((400, 300))

    # Add some data
    widget.update(50.0)
    widget.update(75.0)

    # Should not raise an exception
    widget.render(surface)

    pygame.quit()


def test_graph_widget_has_color():
    """Test that graph widget has a configurable line color"""
    widget = GraphWidget(x=0, y=0, width=100, height=100, color=(0, 255, 0))

    assert widget.color == (0, 255, 0)


def test_graph_widget_default_color():
    """Test that graph widget has a default color"""
    widget = GraphWidget(x=0, y=0, width=100, height=100)

    assert widget.color is not None
    assert len(widget.color) == 3  # RGB tuple


from unittest.mock import patch, call


def test_graph_widget_render_draws_border():
    """Test that render draws a border rectangle"""
    pygame.init()
    widget = GraphWidget(x=10, y=10, width=200, height=100)
    surface = pygame.Surface((400, 300))

    with patch("pygame.draw.rect") as mock_rect:
        widget.render(surface)

        # Verify rect was called with correct parameters
        mock_rect.assert_called_once()
        args = mock_rect.call_args[0]
        assert args[0] == surface  # surface
        assert args[1] == (0, 40, 0)  # border color
        assert args[2] == widget.rect  # rect

    pygame.quit()


def test_graph_widget_render_draws_lines_with_data():
    """Test that render draws lines when data exists"""
    pygame.init()
    widget = GraphWidget(x=10, y=10, width=200, height=100)
    surface = pygame.Surface((400, 300))

    widget.update(25.0)
    widget.update(50.0)
    widget.update(75.0)

    with patch("pygame.draw.lines") as mock_lines:
        widget.render(surface)

        # Verify lines was called
        mock_lines.assert_called_once()
        args = mock_lines.call_args[0]
        assert args[0] == surface  # surface
        assert args[1] == widget.color  # line color
        assert len(args[3]) == 3  # 3 points

    pygame.quit()


def test_graph_widget_render_skips_lines_with_insufficient_data():
    """Test that render doesn't draw lines with less than 2 points"""
    pygame.init()
    widget = GraphWidget(x=10, y=10, width=200, height=100)
    surface = pygame.Surface((400, 300))

    widget.update(50.0)  # Only 1 point

    with patch("pygame.draw.lines") as mock_lines:
        widget.render(surface)

        # Should NOT call draw.lines
        mock_lines.assert_not_called()

    pygame.quit()
