import psutil
import time
from data.base_collector import DataCollector


class MemoryCollector(DataCollector):
    def __init__(self):
        super().__init__()
        self._last_used = None
        self._last_time = None

    def update(self):
        virtual_mem = psutil.virtual_memory()
        swap_mem = psutil.swap_memory()
        current_time = time.time()

        usage_rate = 0

        # Calculate rate if we have previous data
        if self._last_used is not None and self._last_time is not None:
            time_delta = current_time - self._last_time
            if time_delta > 0:
                usage_rate = (virtual_mem.used - self._last_used) / time_delta

        # Store current values for next calculation
        self._last_used = virtual_mem.used
        self._last_time = current_time

        self._data = {
            "percent": virtual_mem.percent,
            "total": virtual_mem.total,
            "available": virtual_mem.available,
            "used": virtual_mem.used,
            "swap_percent": swap_mem.percent,
            "swap_total": swap_mem.total,
            "swap_used": swap_mem.used,
            "usage_rate": usage_rate,  # Bytes per second (can be negative)
        }
