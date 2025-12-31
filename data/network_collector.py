import psutil

from data.base_collector import DataCollector


class NetworkCollector(DataCollector):
    """Network collector for system network statistics"""

    def update(self):
        network_data = psutil.net_io_counters()
        self._data = {
            "bytes_sent": network_data.bytes_sent,
            "bytes_recv": network_data.bytes_recv,
            "packets_sent": network_data.packets_sent,
            "packets_recv": network_data.packets_recv,
        }