import threading
import time
import os
from collections import defaultdict, Counter
import socket
from datetime import datetime
import logging
from typing import Dict, List, Tuple, Optional
import queue
import random
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Try to import scapy, but provide fallback if it fails
try:
    from scapy.all import sniff, IP, TCP, UDP
    logger.info("Scapy successfully imported")
    SCAPY_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Scapy not available: {e}. Using mock data generation instead.")
    SCAPY_AVAILABLE = False

    # Define dummy classes for type hints
    class IP:
        src = "0.0.0.0"
        dst = "0.0.0.0"

    class TCP:
        sport = 0
        dport = 0

    class UDP:
        sport = 0
        dport = 0

# Try to import ipaddress, but provide fallback if it fails
try:
    import ipaddress
except ImportError:
    logger.warning("ipaddress module not available. Using simplified IP validation.")

# Remove duplicate logging configuration

# Global variables
packet_queue = queue.Queue()
stop_collection = threading.Event()
collection_thread = None
processing_thread = None

# Packet statistics
packet_stats = {
    "start_time": None,
    "total_packets": 0,
    "ip_packets": 0,
    "tcp_packets": 0,
    "udp_packets": 0,
    "other_packets": 0,
    "incoming_bytes": 0,
    "outgoing_bytes": 0,
    "source_ips": Counter(),
    "dest_ips": Counter(),
    "port_traffic": defaultdict(int),
    "latency_samples": [],
}

# Network interface to monitor - get from environment or use None for all interfaces
INTERFACE = os.getenv("INTERFACE", None)

# Check if packet capture is enabled (default to True)
PACKET_CAPTURE_ENABLED = os.getenv("PACKET_CAPTURE_ENABLED", "true").lower() == "true"

# Check if mock data fallback is enabled (default to True)
MOCK_DATA_FALLBACK = os.getenv("MOCK_DATA_FALLBACK", "true").lower() == "true"

def reset_stats():
    """Reset packet statistics"""
    global packet_stats
    packet_stats = {
        "start_time": datetime.now(),
        "total_packets": 0,
        "ip_packets": 0,
        "tcp_packets": 0,
        "udp_packets": 0,
        "other_packets": 0,
        "incoming_bytes": 0,
        "outgoing_bytes": 0,
        "source_ips": Counter(),
        "dest_ips": Counter(),
        "port_traffic": defaultdict(int),
        "latency_samples": [],
    }

def packet_callback(packet):
    """Callback function for each captured packet"""
    try:
        if stop_collection.is_set():
            return

        # Add packet to queue for processing
        packet_queue.put(packet)
    except Exception as e:
        logger.error(f"Error in packet callback: {e}")

def process_packets():
    """Process packets from the queue"""
    global packet_stats

    while not stop_collection.is_set() or not packet_queue.empty():
        try:
            # Get packet with timeout to allow checking stop_collection
            packet = packet_queue.get(timeout=1)

            # Update total packet count
            packet_stats["total_packets"] += 1

            # Process IP packets
            if packet.haslayer(IP):
                packet_stats["ip_packets"] += 1

                # Get packet size
                packet_size = len(packet)

                # Update source and destination IP counters
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                packet_stats["source_ips"][src_ip] += 1
                packet_stats["dest_ips"][dst_ip] += 1

                # Determine if packet is incoming or outgoing
                # This is a simplified approach - in production, you'd need to define
                # what constitutes "incoming" vs "outgoing" based on your network
                if is_local_ip(dst_ip):
                    packet_stats["incoming_bytes"] += packet_size
                else:
                    packet_stats["outgoing_bytes"] += packet_size

                # Process TCP packets
                if packet.haslayer(TCP):
                    packet_stats["tcp_packets"] += 1
                    src_port = packet[TCP].sport
                    dst_port = packet[TCP].dport
                    packet_stats["port_traffic"][dst_port] += packet_size

                # Process UDP packets
                elif packet.haslayer(UDP):
                    packet_stats["udp_packets"] += 1
                    src_port = packet[UDP].sport
                    dst_port = packet[UDP].dport
                    packet_stats["port_traffic"][dst_port] += packet_size

                # Other IP-based protocols
                else:
                    packet_stats["other_packets"] += 1

            # Non-IP packets
            else:
                packet_stats["other_packets"] += 1

            # Simulate latency measurement (in production, use actual measurements)
            # In a real implementation, you'd measure actual network latency
            packet_stats["latency_samples"].append(random.uniform(10, 200))

            # Limit latency samples to prevent memory issues
            if len(packet_stats["latency_samples"]) > 1000:
                packet_stats["latency_samples"] = packet_stats["latency_samples"][-1000:]

            packet_queue.task_done()

        except queue.Empty:
            continue
        except Exception as e:
            logger.error(f"Error processing packet: {e}")

def is_local_ip(ip):
    """Determine if an IP is local to the network"""
    try:
        # This is a simplified approach - in production, you'd need to define
        # what constitutes a "local" IP based on your network configuration
        return ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("172.16.")
    except Exception:
        return False

def generate_random_ip():
    """Generate a random IP address"""
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

def generate_random_port():
    """Generate a random port number"""
    return random.randint(1, 65535)

def mock_packet_processing():
    """Simulate packet processing with mock data"""
    global packet_stats

    # Simulate receiving a packet
    packet_stats["total_packets"] += 1
    packet_stats["ip_packets"] += 1

    # Generate random source and destination IPs
    src_ip = generate_random_ip()
    dst_ip = generate_random_ip()

    # Update IP counters
    packet_stats["source_ips"][src_ip] += 1
    packet_stats["dest_ips"][dst_ip] += 1

    # Generate random packet size (500-1500 bytes)
    packet_size = random.randint(500, 1500)

    # Determine if packet is incoming or outgoing
    if random.random() < 0.5:  # 50% chance of being incoming
        packet_stats["incoming_bytes"] += packet_size
    else:
        packet_stats["outgoing_bytes"] += packet_size

    # Determine protocol (TCP or UDP)
    if random.random() < 0.8:  # 80% chance of being TCP
        packet_stats["tcp_packets"] += 1
        dst_port = generate_random_port()
        packet_stats["port_traffic"][dst_port] += packet_size
    else:
        packet_stats["udp_packets"] += 1
        dst_port = generate_random_port()
        packet_stats["port_traffic"][dst_port] += packet_size

    # Simulate latency measurement
    packet_stats["latency_samples"].append(random.uniform(10, 200))

    # Limit latency samples to prevent memory issues
    if len(packet_stats["latency_samples"]) > 1000:
        packet_stats["latency_samples"] = packet_stats["latency_samples"][-1000:]

def mock_data_generator():
    """Generate mock network data continuously"""
    global packet_stats, stop_collection

    # Reset statistics
    reset_stats()

    logger.info("Starting mock data generator")

    # Generate mock data until stopped
    while not stop_collection.is_set():
        try:
            # Generate 10-50 mock packets per iteration
            for _ in range(random.randint(10, 50)):
                mock_packet_processing()

            # Sleep for a short time to simulate real-time data
            time.sleep(0.1)
        except Exception as e:
            logger.error(f"Error in mock data generation: {e}")
            time.sleep(1)  # Wait a bit before retrying

def get_current_stats():
    """Get current packet statistics"""
    global packet_stats

    # Calculate time elapsed
    if packet_stats["start_time"]:
        elapsed_seconds = (datetime.now() - packet_stats["start_time"]).total_seconds()
    else:
        elapsed_seconds = 0

    # Avoid division by zero
    if elapsed_seconds == 0:
        elapsed_seconds = 1

    # Calculate traffic rates (convert bytes to Mbps)
    incoming_traffic = (packet_stats["incoming_bytes"] * 8) / (elapsed_seconds * 1_000_000)
    outgoing_traffic = (packet_stats["outgoing_bytes"] * 8) / (elapsed_seconds * 1_000_000)

    # Calculate average latency
    if packet_stats["latency_samples"]:
        average_latency = sum(packet_stats["latency_samples"]) / len(packet_stats["latency_samples"])
    else:
        average_latency = 0

    # Get top source IPs
    top_source_ips = [
        {"ip": ip, "count": count, "location": "Unknown", "latency": average_latency}
        for ip, count in packet_stats["source_ips"].most_common(5)
    ]

    # Get top destination IPs
    top_dest_ips = [
        {"ip": ip, "count": count, "location": "Unknown", "latency": average_latency}
        for ip, count in packet_stats["dest_ips"].most_common(5)
    ]

    # Get top ports by traffic
    top_ports = [
        {"port": port, "bytes": bytes}
        for port, bytes in sorted(packet_stats["port_traffic"].items(), key=lambda x: x[1], reverse=True)[:5]
    ]

    # Calculate protocol distribution
    total_protocol_packets = packet_stats["tcp_packets"] + packet_stats["udp_packets"]
    if total_protocol_packets > 0:
        tcp_percentage = packet_stats["tcp_packets"] / total_protocol_packets
        udp_percentage = packet_stats["udp_packets"] / total_protocol_packets
    else:
        tcp_percentage = 0
        udp_percentage = 0

    # Simulate packet loss (in production, measure actual packet loss)
    packet_loss = random.uniform(0, 2)

    # Return formatted statistics
    return {
        "timestamp": datetime.now(),
        "incoming_traffic": incoming_traffic,
        "outgoing_traffic": outgoing_traffic,
        "active_connections": len(packet_stats["source_ips"]),
        "average_latency": average_latency,
        "packet_loss": packet_loss,
        "top_source_ips": top_source_ips,
        "top_dest_ips": top_dest_ips,
        "protocols": {
            "tcp": tcp_percentage * 100,
            "udp": udp_percentage * 100
        },
        "port_traffic": top_ports
    }

def start_packet_collection():
    """Start packet collection in a background thread"""
    global collection_thread, processing_thread, stop_collection

    try:
        if collection_thread and collection_thread.is_alive():
            logger.warning("Packet collection already running")
            return

        # Reset stop event and statistics
        stop_collection.clear()
        reset_stats()

        # Start processing thread
        processing_thread = threading.Thread(target=process_packets)
        processing_thread.daemon = True
        processing_thread.start()

        # Check if we should use real packet capture
        if PACKET_CAPTURE_ENABLED and SCAPY_AVAILABLE:
            # Start collection thread with real packet capture
            def collection_worker():
                try:
                    logger.info(f"Starting packet collection on interface: {INTERFACE or 'all'}")
                    # Use a timeout to make sure we can stop even if no packets are received
                    sniff(prn=packet_callback, store=False, iface=INTERFACE,
                          stop_filter=lambda p: stop_collection.is_set(), timeout=1)
                except Exception as e:
                    logger.error(f"Error in packet collection: {e}")
                    # If we get an error, try to use a mock data generator instead
                    if MOCK_DATA_FALLBACK:
                        logger.info("Falling back to mock data generation")
                        while not stop_collection.is_set():
                            try:
                                # Simulate packet processing with mock data
                                mock_packet_processing()
                                time.sleep(0.1)  # Don't overwhelm the system
                            except Exception as inner_e:
                                logger.error(f"Error in mock data generation: {inner_e}")
                                time.sleep(1)  # Wait a bit before retrying

            collection_thread = threading.Thread(target=collection_worker)
            collection_thread.daemon = True
            collection_thread.start()

            logger.info("Packet collection started with real packet capture")
        else:
            # Use mock data generation instead
            if not PACKET_CAPTURE_ENABLED:
                logger.info("Packet capture disabled by configuration, using mock data")
            elif not SCAPY_AVAILABLE:
                logger.info("Scapy not available, using mock data")

            mock_data_thread = threading.Thread(target=mock_data_generator)
            mock_data_thread.daemon = True
            mock_data_thread.start()
            collection_thread = mock_data_thread

            logger.info("Started mock data generator")
    except Exception as e:
        logger.error(f"Failed to start packet collection: {e}")
        # Fall back to mock data if we can't start packet collection
        if MOCK_DATA_FALLBACK:
            try:
                mock_data_thread = threading.Thread(target=mock_data_generator)
                mock_data_thread.daemon = True
                mock_data_thread.start()
                collection_thread = mock_data_thread
                logger.info("Started mock data generator as fallback")
            except Exception as mock_e:
                logger.error(f"Failed to start mock data generator: {mock_e}")

def stop_packet_collection():
    """Stop packet collection"""
    global stop_collection

    try:
        logger.info("Stopping packet collection")
        stop_collection.set()

        # Wait for threads to finish
        if collection_thread:
            collection_thread.join(timeout=5)

        if processing_thread:
            processing_thread.join(timeout=5)

        logger.info("Packet collection stopped")
    except Exception as e:
        logger.error(f"Error stopping packet collection: {e}")

# For testing
if __name__ == "__main__":
    try:
        start_packet_collection()

        # Print statistics every 5 seconds
        for _ in range(5):
            time.sleep(5)
            stats = get_current_stats()
            print(f"Incoming Traffic: {stats['incoming_traffic']:.2f} Mbps")
            print(f"Outgoing Traffic: {stats['outgoing_traffic']:.2f} Mbps")
            print(f"Active Connections: {stats['active_connections']}")
            print(f"Average Latency: {stats['average_latency']:.2f} ms")
            print(f"Packet Loss: {stats['packet_loss']:.2f}%")
            print("Top Source IPs:", stats['top_source_ips'])
            print("Top Destination IPs:", stats['top_dest_ips'])
            print("Protocol Distribution:", stats['protocols'])
            print("Port Traffic:", stats['port_traffic'])
            print("-" * 50)

        stop_packet_collection()

    except KeyboardInterrupt:
        stop_packet_collection()
        print("Packet collection stopped by user")
