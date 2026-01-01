from ui.display import Display
from ui.graph_widget import GraphWidget
from data.cpu_collector import CPUCollector
from data.memory_collector import MemoryCollector
from data.disk_collector import DiskCollector
from data.network_collector import NetworkCollector
from utils.effects import Effects
import pygame


def main():
    # Initialize display with shorter height
    display = Display(width=1024, height=500)

    collectors = {
        "cpu": CPUCollector(),
        "memory": MemoryCollector(),
        "disk": DiskCollector(),
        "network": NetworkCollector(),
    }

    # Create graph widgets in a 2x2 grid layout
    cpu_graph = GraphWidget(
        x=50, y=50, width=400, height=150, max_samples=120, color=(0, 255, 0)
    )
    mem_graph = GraphWidget(
        x=500, y=50, width=400, height=150, max_samples=120, color=(0, 200, 255)
    )
    disk_graph = GraphWidget(
        x=50, y=270, width=400, height=150, max_samples=120, color=(255, 200, 0)
    )
    net_graph = GraphWidget(
        x=500, y=270, width=400, height=150, max_samples=120, color=(255, 0, 255)
    )

    # Font for labels
    font = pygame.font.Font(None, 24)

    # Frame counter for slower updates
    frame_count = 0
    update_interval = 10  # Update collectors every 10 frames

    # Track previous network bytes to calculate rate
    prev_net_sent = 0
    prev_net_recv = 0

    while display.running:
        display.handle_events()

        # Only update collectors every N frames
        if frame_count % update_interval == 0:
            for collector in collectors.values():
                collector.update()

            # Update graphs with new data
            cpu_data = collectors["cpu"].get_data()
            if cpu_data:
                cpu_graph.update(cpu_data["cpu_percent"])

            mem_data = collectors["memory"].get_data()
            if mem_data:
                # Graph memory allocation rate
                # Convert to MB/s and scale for visibility
                # Negative = freeing memory, positive = allocating
                usage_rate_mbs = mem_data["usage_rate"] / (1024**2)

                # Center at 50, scale to make visible (±50 MB/s range)
                scaled_rate = 50 + (usage_rate_mbs * 5)  # 10 MB/s = ±50 on graph
                mem_graph.update(max(0, min(100, scaled_rate)))  # Clamp to 0-100

            disk_data = collectors["disk"].get_data()
            if disk_data:
                # Graph combined I/O activity in MB/s (scaled to 0-100 range)
                # Assuming max 100 MB/s for scaling (adjust based on your disk)
                io_rate_mbs = (disk_data["read_rate"] + disk_data["write_rate"]) / (
                    1024**2
                )
                disk_graph.update(min(io_rate_mbs * 10, 100))  # Scale up for visibility

            # Network: calculate transfer rate (bytes per interval)
            net_data = collectors["network"].get_data()
            if net_data:
                # Calculate delta since last update
                sent_delta = net_data["bytes_sent"] - prev_net_sent
                recv_delta = net_data["bytes_recv"] - prev_net_recv

                # Update previous values
                prev_net_sent = net_data["bytes_sent"]
                prev_net_recv = net_data["bytes_recv"]

                # Total network activity (sent + received) in KB/s
                # Multiply by (1000ms / update_interval * 33.33ms) to get per second
                total_rate = (sent_delta + recv_delta) / 1024  # Convert to KB
                total_rate_per_sec = total_rate * (
                    30 / update_interval
                )  # Scale to per second

                # Cap at 100 for graph display (or use dynamic scaling)
                net_graph.update(min(total_rate_per_sec, 100))

        frame_count += 1

        # Render
        display.clear((0, 20, 0))  # Dark green background

        # Get current data for labels
        cpu_data = collectors["cpu"].get_data()
        mem_data = collectors["memory"].get_data()
        disk_data = collectors["disk"].get_data()
        net_data = collectors["network"].get_data()

        # Render graphs
        cpu_graph.render(display.screen)
        mem_graph.render(display.screen)
        disk_graph.render(display.screen)
        net_graph.render(display.screen)

        # Render labels
        if cpu_data:
            cpu_label = font.render(
                f"CPU: {cpu_data['cpu_percent']:.1f}%", True, (0, 255, 0)
            )
            display.screen.blit(cpu_label, (50, 25))

        if mem_data:
            usage_rate_mbs = mem_data["usage_rate"] / (1024**2)
            sign = "+" if usage_rate_mbs >= 0 else ""
            mem_label = font.render(
                f"RAM: {sign}{usage_rate_mbs:.1f}MB/s", True, (0, 200, 255)
            )
            display.screen.blit(mem_label, (500, 25))

        if disk_data:
            io_rate_mbs = (disk_data["read_rate"] + disk_data["write_rate"]) / (1024**2)
            disk_label = font.render(
                f"DISK I/O: {io_rate_mbs:.1f}MB/s", True, (255, 200, 0)
            )
            display.screen.blit(disk_label, (50, 245))

        if net_data:
            # Show total throughput
            total_mb = (net_data["bytes_sent"] + net_data["bytes_recv"]) / (1024**2)
            net_label = font.render(f"NET: {total_mb:.1f}MB total", True, (255, 0, 255))
            display.screen.blit(net_label, (500, 245))

        # Apply scanlines effect
        Effects.apply_scanlines(display.screen, intensity=0.5, spacing=2)

        display.update()
        display.tick(30)

    display.quit()


if __name__ == "__main__":
    main()
