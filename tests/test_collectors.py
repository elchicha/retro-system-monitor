import pytest
from data.collector import DataCollector
from data.cpu_collector import CPUCollector

class MockCollector(DataCollector):
    def update(self):
        self._data = {"test": 42}

def test_collector_initialization():
    collector = MockCollector()
    assert collector.get_data() is None

def test_collector_update_stores_data():
    """Test that update() stores retrievable data"""
    collector = MockCollector()
    collector.update()
    data = collector.get_data()
    assert data == {'test': 42}

def test_collector_multiple_updates():
    """Test that subsequent updates replace old data"""
    collector = MockCollector()
    collector.update()
    collector.update()
    data = collector.get_data()
    assert data == {'test': 42}


def test_cpu_collector_returns_percentage():
    """Test that CPU collector returns a valid percentage"""
    collector = CPUCollector()
    collector.update()
    data = collector.get_data()

    assert data is not None
    assert 'cpu_percent' in data
    assert 0 <= data['cpu_percent'] <= 100


def test_cpu_collector_returns_per_core():
    """Test that CPU collector returns per-core data"""
    collector = CPUCollector()
    collector.update()
    data = collector.get_data()

    assert 'per_core' in data
    assert isinstance(data['per_core'], list)
    assert len(data['per_core']) > 0
    for core_percent in data['per_core']:
        assert 0 <= core_percent <= 100