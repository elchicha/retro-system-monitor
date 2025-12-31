from data.memory_collector import MemoryCollector


def test_memory_collector_returns_usage():
    """Test that memory collector returns memory usage data"""
    collector = MemoryCollector()
    collector.update()
    data = collector.get_data()

    assert data is not None
    assert "percent" in data
    assert "total" in data
    assert "available" in data
    assert "used" in data

    assert 0 <= data["percent"] <= 100
    assert data["total"] > 0
    assert data["available"] >= 0
    assert data["used"] >= 0


def test_memory_collector_includes_swap():
    """Test that memory collector includes swap memory data"""
    collector = MemoryCollector()
    collector.update()
    data = collector.get_data()

    assert "swap_percent" in data
    assert "swap_total" in data
    assert "swap_used" in data

    assert 0 <= data["swap_percent"] <= 100
