import psutil

from data.collector import DataCollector


class MemoryCollector(DataCollector):
    """Concrete collector for memory data"""

    def update(self):
        memory_utilization = psutil.virtual_memory()
        swap_utilization = psutil.swap_memory()
        self._data = {
            "percent": memory_utilization.percent,
            "total": memory_utilization.total,
            "available": memory_utilization.available,
            "used": memory_utilization.used,
            "swap_percent": swap_utilization.percent,
            "swap_total": swap_utilization.total,
            "swap_used": swap_utilization.used,
        }
