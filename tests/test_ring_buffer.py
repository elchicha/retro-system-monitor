import pytest
from utils.ring_buffer import RingBuffer


def test_ring_buffer_initialization():
    """Test that ring buffer initializes with correct size"""
    buffer = RingBuffer(max_size=5)
    
    assert buffer.max_size == 5
    assert len(buffer) == 0


def test_ring_buffer_append():
    """Test that append adds items to buffer"""
    buffer = RingBuffer(max_size=3)
    
    buffer.append(1)
    buffer.append(2)
    
    assert len(buffer) == 2


def test_ring_buffer_wraparound():
    """Test that buffer wraps around when full"""
    buffer = RingBuffer(max_size=3)
    
    buffer.append(1)
    buffer.append(2)
    buffer.append(3)
    buffer.append(4)  # Should replace 1
    
    assert len(buffer) == 3
    assert list(buffer.get_all()) == [2, 3, 4]


def test_ring_buffer_get_all_empty():
    """Test that get_all returns empty list when buffer is empty"""
    buffer = RingBuffer(max_size=5)
    
    assert list(buffer.get_all()) == []


def test_ring_buffer_get_all_partial():
    """Test that get_all returns correct items when partially filled"""
    buffer = RingBuffer(max_size=5)
    
    buffer.append(10)
    buffer.append(20)
    buffer.append(30)
    
    assert list(buffer.get_all()) == [10, 20, 30]