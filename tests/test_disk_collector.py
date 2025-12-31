from data.disk_collector import DiskCollector

def test_disk_collector_returns_usage():
    """Test that disk collector returns disk usage data"""
    collector = DiskCollector()
    collector.update()
    data = collector.get_data()

    assert data is not None
    assert "percent" in data
    assert "total" in data
    assert "used" in data
    assert "free" in data

    assert 0 <= data["percent"] <= 100
    assert data["total"] > 0
    assert data["used"] >= 0
    assert data["free"] >= 0


def test_disk_collector_returns_io_stats():
    """Test that disk collector returns I/O statistics"""
    collector = DiskCollector()
    collector.update()
    data = collector.get_data()

    assert "read_bytes" in data
    assert "write_bytes" in data
    assert data["read_bytes"] >= 0
    assert data["write_bytes"] >= 0


def test_disk_collector_multiple_updates():
    """Test that disk I/O counters can increase between updates"""
    collector = DiskCollector()
    collector.update()
    first_read = collector.get_data()["read_bytes"]

    # Do some disk activity (this might not always trigger, but tests the mechanism)
    import time

    time.sleep(0.1)

    collector.update()
    second_read = collector.get_data()["read_bytes"]

    # Should be equal or increased (cumulative counter)
    assert second_read >= first_read
