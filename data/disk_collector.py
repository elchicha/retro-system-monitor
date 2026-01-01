import psutil
import time
from data.base_collector import DataCollector


class DiskCollector(DataCollector):
    def __init__(self, path="/"):
        super().__init__()
        self.path = path
        self._last_io = None
        self._last_time = None

    def update(self):
        usage = psutil.disk_usage(self.path)
        io_counters = psutil.disk_io_counters()
        current_time = time.time()

        read_rate = 0
        write_rate = 0

        # Calculate rates if we have previous data
        if self._last_io is not None and self._last_time is not None:
            time_delta = current_time - self._last_time
            if time_delta > 0:
                read_rate = (
                    io_counters.read_bytes - self._last_io.read_bytes
                ) / time_delta
                write_rate = (
                    io_counters.write_bytes - self._last_io.write_bytes
                ) / time_delta

        # Store current values for next calculation
        self._last_io = io_counters
        self._last_time = current_time

        self._data = {
            "percent": usage.percent,
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "read_bytes": io_counters.read_bytes,
            "write_bytes": io_counters.write_bytes,
            "read_rate": read_rate,  # Bytes per second
            "write_rate": write_rate,  # Bytes per second
        }
