import psutil
from psutil import cpu_percent

from data.collector import DataCollector


class CPUCollector(DataCollector):
    """Concrete collector for CPU data"""

    def update(self):
        cpu_usage_percent: float = cpu_percent()
        cpu_usage_per_core: list[float] = cpu_percent(percpu=True)

        self._data = {
            "cpu_percent": cpu_usage_percent,
            "per_core": cpu_usage_per_core
        }