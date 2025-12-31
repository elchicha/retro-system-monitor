from shutil import disk_usage

import psutil

from data.base_collector import DataCollector


class DiskCollector(DataCollector):
    def update(self):
        disk_usage_data = psutil.disk_usage('/')
        disk_io_data = psutil.disk_io_counters()

        self._data = {
            "percent": disk_usage_data.percent,
            "total": disk_usage_data.total,
            "used": disk_usage_data.used,
            "free": disk_usage_data.free,
            "read_bytes": disk_io_data.read_bytes,
            "write_bytes": disk_io_data.write_bytes,
        }