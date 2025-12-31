from data.collector import DataCollector


def test_collector_initialization():
    collector = MockCollector()
    assert collector.get_data() is None


def test_collector_update_stores_data():
    """Test that update() stores retrievable data"""
    collector = MockCollector()
    collector.update()
    data = collector.get_data()
    assert data == {"test": 42}


def test_collector_multiple_updates():
    """Test that subsequent updates replace old data"""
    collector = MockCollector()
    collector.update()
    collector.update()
    data = collector.get_data()
    assert data == {"test": 42}


class MockCollector(DataCollector):
    def update(self):
        self._data = {"test": 42}
