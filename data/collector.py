from abc import ABC, abstractmethod

class DataCollector(ABC):
    """Abstract Base Class for all system data collectors"""
    def __init__(self):
        self._data = None

    def get_data(self):
        """Returns the most recently collected data"""
        return self._data

    @abstractmethod
    def update(self):
        raise NotImplementedError("Subclasses must implement update method")