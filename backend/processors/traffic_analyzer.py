from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import SQLAlchemy Session type
try:
    from sqlalchemy.orm import Session
except ImportError:
    # Define a dummy Session type for type hints
    class Session:
        pass
    logger.warning("SQLAlchemy not available. Using dummy Session type.")

# Try both import paths to handle different execution contexts
try:
    # When running from project root
    from backend.database.db_connector import NetworkMetrics, SourceIP, DestinationIP, PortTraffic
    from backend.collectors.packet_collector import get_current_stats
except ImportError:
    try:
        # When running from backend directory
        from database.db_connector import NetworkMetrics, SourceIP, DestinationIP, PortTraffic
        from collectors.packet_collector import get_current_stats
    except ImportError:
        logger.error("Failed to import required modules. Some functionality may be limited.")

        # Define dummy functions and classes for fallback
        def get_current_stats():
            """Dummy function that returns mock data"""
            from datetime import datetime
            return {
                "timestamp": datetime.now(),
                "incoming_traffic": 100.0,
                "outgoing_traffic": 50.0,
                "active_connections": 10,
                "average_latency": 20.0,
                "packet_loss": 0.5,
                "top_source_ips": [{"ip": "192.168.1.1", "count": 100, "location": "Local", "latency": 10.0}],
                "top_dest_ips": [{"ip": "8.8.8.8", "count": 50, "location": "Google DNS", "latency": 30.0}],
                "protocols": {"tcp": 80, "udp": 20},
                "port_traffic": [{"port": 80, "bytes": 1000}, {"port": 443, "bytes": 2000}]
            }

        # Dummy classes
        class NetworkMetrics:
            pass

        class SourceIP:
            pass

        class DestinationIP:
            pass

        class PortTraffic:
            pass

# Function to handle database errors gracefully
def handle_db_error(func):
    """Decorator to handle database errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Database error in {func.__name__}: {e}")
            # Return mock data as fallback
            if func.__name__ == "get_network_metrics":
                return get_current_stats()
            elif func.__name__ == "get_historical_metrics":
                # Return empty list for historical metrics
                return []
            else:
                raise
    return wrapper

@handle_db_error
def get_network_metrics(db: Session) -> Dict[str, Any]:
    """
    Get the most recent network metrics
    """
    # Get real-time metrics from packet collector
    metrics = get_current_stats()

    # Save metrics to database
    try:
        save_metrics_to_db(db, metrics)
    except Exception as e:
        logger.warning(f"Failed to save metrics to database: {e}")

    return metrics

@handle_db_error
def get_historical_metrics(
    db: Session,
    start_time: datetime,
    end_time: datetime
) -> List[Dict[str, Any]]:
    """
    Get historical network metrics from the database
    """
    # Query metrics from database
    db_metrics = db.query(NetworkMetrics).filter(
        NetworkMetrics.timestamp >= start_time,
        NetworkMetrics.timestamp <= end_time
    ).order_by(NetworkMetrics.timestamp.asc()).all()

    # If no metrics found, return empty list
    if not db_metrics:
        logger.warning(f"No metrics found between {start_time} and {end_time}")
        return []

    # Convert to response format
    result = []
    for metric in db_metrics:
        try:
            # Get source IPs
            source_ips = [
                {
                    "ip": ip.ip_address,
                    "count": ip.count,
                    "location": ip.location,
                    "latency": ip.latency
                }
                for ip in metric.source_ips
            ]

            # Get destination IPs
            dest_ips = [
                {
                    "ip": ip.ip_address,
                    "count": ip.count,
                    "location": ip.location,
                    "latency": ip.latency
                }
                for ip in metric.dest_ips
            ]

            # Get port traffic
            port_traffic = [
                {
                    "port": pt.port,
                    "bytes": pt.bytes
                }
                for pt in metric.port_traffic
            ]

            # Parse protocols JSON
            try:
                protocols = json.loads(metric.protocols) if isinstance(metric.protocols, str) else metric.protocols
            except (json.JSONDecodeError, TypeError):
                # Fallback to default protocol distribution
                protocols = {"tcp": 80, "udp": 20}

            # Add to result
            result.append({
                "timestamp": metric.timestamp,
                "incoming_traffic": metric.incoming_traffic,
                "outgoing_traffic": metric.outgoing_traffic,
                "active_connections": metric.active_connections,
                "average_latency": metric.average_latency,
                "packet_loss": metric.packet_loss,
                "top_source_ips": source_ips,
                "top_dest_ips": dest_ips,
                "protocols": protocols,
                "port_traffic": port_traffic
            })
        except Exception as e:
            logger.error(f"Error processing metric {metric.id}: {e}")
            # Continue with next metric
            continue

    return result

def save_metrics_to_db(db: Session, metrics: Dict[str, Any]) -> None:
    """
    Save network metrics to the database
    """
    try:
        # Ensure protocols is serializable
        protocols = metrics.get("protocols", {"tcp": 0, "udp": 0})
        if not isinstance(protocols, (dict, str)):
            # Convert to dict if it's not already
            try:
                protocols = {"tcp": float(protocols.get("tcp", 0)), "udp": float(protocols.get("udp", 0))}
            except (AttributeError, ValueError):
                # Fallback to default
                protocols = {"tcp": 0, "udp": 0}

        # Create new NetworkMetrics record
        db_metrics = NetworkMetrics(
            timestamp=metrics.get("timestamp", datetime.now()),
            incoming_traffic=float(metrics.get("incoming_traffic", 0)),
            outgoing_traffic=float(metrics.get("outgoing_traffic", 0)),
            active_connections=int(metrics.get("active_connections", 0)),
            average_latency=float(metrics.get("average_latency", 0)),
            packet_loss=float(metrics.get("packet_loss", 0)),
            protocols=protocols
        )

        # Add to session
        db.add(db_metrics)
        db.flush()  # Flush to get the ID

        # Add source IPs
        for ip_info in metrics.get("top_source_ips", []):
            try:
                source_ip = SourceIP(
                    metrics_id=db_metrics.id,
                    ip_address=ip_info.get("ip", "unknown"),
                    count=int(ip_info.get("count", 0)),
                    location=ip_info.get("location"),
                    latency=float(ip_info.get("latency", 0))
                )
                db.add(source_ip)
            except Exception as e:
                logger.warning(f"Error adding source IP: {e}")
                # Continue with next IP
                continue

        # Add destination IPs
        for ip_info in metrics.get("top_dest_ips", []):
            try:
                dest_ip = DestinationIP(
                    metrics_id=db_metrics.id,
                    ip_address=ip_info.get("ip", "unknown"),
                    count=int(ip_info.get("count", 0)),
                    location=ip_info.get("location"),
                    latency=float(ip_info.get("latency", 0))
                )
                db.add(dest_ip)
            except Exception as e:
                logger.warning(f"Error adding destination IP: {e}")
                # Continue with next IP
                continue

        # Add port traffic
        for port_info in metrics.get("port_traffic", []):
            try:
                port_traffic = PortTraffic(
                    metrics_id=db_metrics.id,
                    port=int(port_info.get("port", 0)),
                    bytes=int(port_info.get("bytes", 0))
                )
                db.add(port_traffic)
            except Exception as e:
                logger.warning(f"Error adding port traffic: {e}")
                # Continue with next port
                continue

        # Commit changes
        db.commit()
        logger.debug(f"Saved metrics to database with ID {db_metrics.id}")
    except Exception as e:
        try:
            db.rollback()
        except Exception as rollback_error:
            logger.error(f"Error during rollback: {rollback_error}")

        logger.error(f"Error saving metrics to database: {e}")
        # Re-raise the exception to be handled by the decorator
        raise

def analyze_traffic_patterns(
    db: Session,
    start_time: datetime,
    end_time: datetime
) -> Dict[str, Any]:
    """
    Analyze traffic patterns over a time period
    """
    try:
        # Get historical metrics
        metrics = get_historical_metrics(db, start_time, end_time)

        if not metrics:
            return {
                "average_incoming": 0,
                "average_outgoing": 0,
                "peak_incoming": 0,
                "peak_outgoing": 0,
                "total_connections": 0,
                "average_latency": 0
            }

        # Calculate statistics
        incoming_values = [m["incoming_traffic"] for m in metrics]
        outgoing_values = [m["outgoing_traffic"] for m in metrics]
        latency_values = [m["average_latency"] for m in metrics]
        connection_values = [m["active_connections"] for m in metrics]

        # Return analysis
        return {
            "average_incoming": sum(incoming_values) / len(incoming_values),
            "average_outgoing": sum(outgoing_values) / len(outgoing_values),
            "peak_incoming": max(incoming_values),
            "peak_outgoing": max(outgoing_values),
            "total_connections": sum(connection_values) / len(connection_values),
            "average_latency": sum(latency_values) / len(latency_values)
        }
    except Exception as e:
        logger.error(f"Error analyzing traffic patterns: {e}")
        raise
