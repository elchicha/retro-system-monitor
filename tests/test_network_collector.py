import pytest
from data.network_collector import NetworkCollector


def test_network_collector_returns_traffic_data():
    """Test that network collector returns bytes sent and received"""
    collector = NetworkCollector()
    collector.update()
    data = collector.get_data()

    assert data is not None
    assert "bytes_sent" in data
    assert "bytes_recv" in data
    assert data["bytes_sent"] >= 0
    assert data["bytes_recv"] >= 0


def test_network_collector_returns_packet_data():
    """Test that network collector returns packet counts"""
    collector = NetworkCollector()
    collector.update()
    data = collector.get_data()

    assert "packets_sent" in data
    assert "packets_recv" in data
    assert data["packets_sent"] >= 0
    assert data["packets_recv"] >= 0


def test_network_collector_counters_are_cumulative():
    """Test that network counters are cumulative since boot"""
    collector = NetworkCollector()
    collector.update()
    first_sent = collector.get_data()["bytes_sent"]

    import time

    time.sleep(0.1)

    collector.update()
    second_sent = collector.get_data()["bytes_sent"]

    # Should be equal or increased (cumulative counter)
    assert second_sent >= first_sent
