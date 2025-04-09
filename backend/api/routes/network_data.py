from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
import logging
import os
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import SQLAlchemy Session type
try:
    from sqlalchemy.orm import Session
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    # Define a dummy Session type for type hints
    class Session:
        pass
    SQLALCHEMY_AVAILABLE = False
    logger.warning("SQLAlchemy not available. Using dummy Session type.")

# Try both import paths to handle different execution contexts
try:
    # When running from project root
    from backend.database.db_connector import get_db
    from backend.api.models.network_models import NetworkMetricsResponse, TimeRange
    from backend.processors.traffic_analyzer import get_network_metrics, get_historical_metrics
    IMPORTS_SUCCESSFUL = True
except ImportError:
    try:
        # When running from backend directory
        from database.db_connector import get_db
        from api.models.network_models import NetworkMetricsResponse, TimeRange
        from processors.traffic_analyzer import get_network_metrics, get_historical_metrics
        IMPORTS_SUCCESSFUL = True
    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}. Some functionality may be limited.")
        IMPORTS_SUCCESSFUL = False

        # Define dummy classes and functions for fallback
        class TimeRange(str, Enum):
            FIVE_MIN = "5m"
            FIFTEEN_MIN = "15m"
            THIRTY_MIN = "30m"
            ONE_HOUR = "1h"
            SIX_HOURS = "6h"
            ONE_DAY = "24h"

        class NetworkMetricsResponse(Dict[str, Any]):
            pass

        def get_db():
            class DummySession:
                def close(self):
                    pass
                def commit(self):
                    pass
                def rollback(self):
                    pass
            dummy = DummySession()
            yield dummy

        def get_network_metrics(db=None):
            """Generate mock network metrics"""
            return generate_mock_metrics()

        def get_historical_metrics(db=None, start_time=None, end_time=None):
            """Generate mock historical metrics"""
            # Generate a list of metrics with timestamps between start_time and end_time
            if not start_time:
                start_time = datetime.now() - timedelta(minutes=15)
            if not end_time:
                end_time = datetime.now()

            # Calculate number of data points (1 per minute)
            minutes = int((end_time - start_time).total_seconds() / 60) + 1
            metrics = []

            for i in range(minutes):
                metric_time = start_time + timedelta(minutes=i)
                metric = generate_mock_metrics(metric_time)
                metrics.append(metric)

            return metrics

# Import Enum for TimeRange if needed
try:
    from enum import Enum
except ImportError:
    # Define a simple Enum class if the import fails
    class Enum:
        pass

# Function to generate mock metrics for testing
def generate_mock_metrics(timestamp=None):
    """Generate mock network metrics for testing"""
    import random

    if timestamp is None:
        timestamp = datetime.now()

    # Generate random values with some variation but consistency
    base_incoming = 100.0 + (timestamp.hour * 10)
    base_outgoing = 50.0 + (timestamp.hour * 5)

    return {
        "timestamp": timestamp,
        "incoming_traffic": base_incoming + random.uniform(-20, 20),
        "outgoing_traffic": base_outgoing + random.uniform(-10, 10),
        "active_connections": random.randint(5, 20),
        "average_latency": 20.0 + random.uniform(-5, 15),
        "packet_loss": random.uniform(0, 2),
        "top_source_ips": [
            {"ip": "192.168.1.1", "count": random.randint(50, 150), "location": "Local", "latency": random.uniform(5, 15)},
            {"ip": "192.168.1.2", "count": random.randint(30, 100), "location": "Local", "latency": random.uniform(5, 15)},
            {"ip": "10.0.0.1", "count": random.randint(20, 80), "location": "VPN", "latency": random.uniform(10, 30)},
        ],
        "top_dest_ips": [
            {"ip": "8.8.8.8", "count": random.randint(30, 100), "location": "Google DNS", "latency": random.uniform(20, 40)},
            {"ip": "1.1.1.1", "count": random.randint(20, 80), "location": "Cloudflare DNS", "latency": random.uniform(15, 35)},
            {"ip": "172.217.169.78", "count": random.randint(10, 50), "location": "Google", "latency": random.uniform(25, 45)},
        ],
        "protocols": {"tcp": random.uniform(70, 90), "udp": random.uniform(10, 30)},
        "port_traffic": [
            {"port": 80, "bytes": random.randint(500, 1500)},
            {"port": 443, "bytes": random.randint(1000, 3000)},
            {"port": 53, "bytes": random.randint(200, 800)},
        ]
    }

router = APIRouter()

@router.get("/metrics/current", response_model=NetworkMetricsResponse)
async def get_current_metrics(db: Session = Depends(get_db)):
    """
    Get the most recent network metrics
    """
    try:
        metrics = get_network_metrics(db)
        logger.info(f"Retrieved current metrics: {metrics.get('timestamp') if isinstance(metrics, dict) else 'unknown timestamp'}")
        return metrics
    except Exception as e:
        logger.error(f"Failed to retrieve metrics: {str(e)}")
        # Return mock data as fallback
        try:
            from datetime import datetime
            mock_data = {
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
            logger.info("Returning mock data as fallback")
            return mock_data
        except Exception as mock_error:
            logger.error(f"Failed to generate mock data: {str(mock_error)}")
            raise HTTPException(status_code=500, detail=f"Failed to retrieve metrics: {str(e)}")

@router.get("/metrics/historical", response_model=List[NetworkMetricsResponse])
async def get_metrics_history(
    time_range: TimeRange = Query(TimeRange.FIFTEEN_MIN),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    Get historical network metrics based on time range or specific start/end times
    """
    try:
        # If specific start/end times are provided, use those instead of time_range
        if start_time and end_time:
            logger.info(f"Fetching historical metrics from {start_time} to {end_time}")
            metrics = get_historical_metrics(db, start_time=start_time, end_time=end_time)
        else:
            # Calculate start time based on time_range
            now = datetime.now()

            # Handle time range
            try:
                if time_range == TimeRange.FIVE_MIN:
                    start_time = now - timedelta(minutes=5)
                elif time_range == TimeRange.FIFTEEN_MIN:
                    start_time = now - timedelta(minutes=15)
                elif time_range == TimeRange.THIRTY_MIN:
                    start_time = now - timedelta(minutes=30)
                elif time_range == TimeRange.ONE_HOUR:
                    start_time = now - timedelta(hours=1)
                elif time_range == TimeRange.SIX_HOURS:
                    start_time = now - timedelta(hours=6)
                elif time_range == TimeRange.ONE_DAY:
                    start_time = now - timedelta(days=1)
                else:
                    # Default to 15 minutes if time_range is invalid
                    logger.warning(f"Invalid time range: {time_range}, defaulting to 15 minutes")
                    start_time = now - timedelta(minutes=15)
            except Exception as time_error:
                logger.error(f"Error calculating time range: {time_error}")
                # Default to 15 minutes
                start_time = now - timedelta(minutes=15)

            logger.info(f"Fetching historical metrics from {start_time} to {now} (time range: {time_range})")
            metrics = get_historical_metrics(db, start_time=start_time, end_time=now)

        # Check if metrics is empty
        if not metrics:
            logger.warning("No historical metrics found, generating mock data")
            # Generate mock historical data
            mock_metrics = []
            now = datetime.now()

            # Determine number of data points based on time range
            num_points = 15  # Default
            interval_minutes = 1  # Default

            if time_range == TimeRange.FIVE_MIN:
                num_points = 5
                interval_minutes = 1
            elif time_range == TimeRange.FIFTEEN_MIN:
                num_points = 15
                interval_minutes = 1
            elif time_range == TimeRange.THIRTY_MIN:
                num_points = 30
                interval_minutes = 1
            elif time_range == TimeRange.ONE_HOUR:
                num_points = 60
                interval_minutes = 1
            elif time_range == TimeRange.SIX_HOURS:
                num_points = 72
                interval_minutes = 5
            elif time_range == TimeRange.ONE_DAY:
                num_points = 96
                interval_minutes = 15

            # Generate data points
            for i in range(num_points):
                point_time = now - timedelta(minutes=(num_points - i - 1) * interval_minutes)
                mock_metrics.append(generate_mock_metrics(point_time))

            logger.info(f"Generated {len(mock_metrics)} mock historical metrics")
            return mock_metrics

        logger.info(f"Retrieved {len(metrics)} historical metrics")
        return metrics
    except Exception as e:
        logger.error(f"Failed to retrieve historical metrics: {str(e)}")
        # Return empty list as fallback
        return []

@router.get("/top-ips/source")
async def get_top_source_ips(
    limit: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get the top source IPs by traffic volume
    """
    try:
        # Implementation will be added
        return {"message": "Not yet implemented"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve top source IPs: {str(e)}")

@router.get("/top-ips/destination")
async def get_top_destination_ips(
    limit: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get the top destination IPs by traffic volume
    """
    try:
        # Implementation will be added
        return {"message": "Not yet implemented"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve top destination IPs: {str(e)}")

@router.get("/protocols")
async def get_protocol_distribution(db: Session = Depends(get_db)):
    """
    Get the distribution of network traffic by protocol
    """
    try:
        # Implementation will be added
        return {"message": "Not yet implemented"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve protocol distribution: {str(e)}")

@router.get("/port-traffic")
async def get_port_traffic(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get traffic statistics by port
    """
    try:
        # Implementation will be added
        return {"message": "Not yet implemented"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve port traffic: {str(e)}")
