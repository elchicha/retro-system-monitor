from abc import ABC, abstractmethod
import pygame


class Widget(ABC):
    """Abstract base class for all UI widgets"""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)