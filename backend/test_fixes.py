#!/usr/bin/env python
"""
Test script to verify the fixes for the backend components.
This script tests each component individually to ensure they work correctly.
"""

import os
import sys
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_packet_collector():
    """Test the packet collector module"""
    logger.info("Testing packet_collector.py...")
    try:
        from collectors.packet_collector import get_current_stats, start_packet_collection, stop_packet_collection
        
        # Start packet collection
        start_packet_collection()
        logger.info("Packet collection started successfully")
        
        # Get current stats
        stats = get_current_stats()
        logger.info(f"Got current stats: {stats.get('timestamp')}")
        
        # Stop packet collection
        stop_packet_collection()
        logger.info("Packet collection stopped successfully")
        
        logger.info("✅ packet_collector.py is working correctly")
        return True
    except Exception as e:
        logger.error(f"❌ Error testing packet_collector.py: {e}")
        return False

def test_db_connector():
    """Test the database connector module"""
    logger.info("Testing db_connector.py...")
    try:
        from database.db_connector import init_db, get_db, Base, engine
        
        # Initialize database
        import asyncio
        asyncio.run(init_db())
        logger.info("Database initialized successfully")
        
        # Test database connection
        db = next(get_db())
        logger.info("Database connection established successfully")
        db.close()
        
        logger.info("✅ db_connector.py is working correctly")
        return True
    except Exception as e:
        logger.error(f"❌ Error testing db_connector.py: {e}")
        return False

def test_traffic_analyzer():
    """Test the traffic analyzer module"""
    logger.info("Testing traffic_analyzer.py...")
    try:
        from processors.traffic_analyzer import get_network_metrics, get_historical_metrics
        from database.db_connector import get_db
        
        # Get database connection
        db = next(get_db())
        
        # Get current metrics
        metrics = get_network_metrics(db)
        logger.info(f"Got current metrics: {metrics.get('timestamp')}")
        
        # Get historical metrics
        now = datetime.now()
        start_time = now - timedelta(minutes=15)
        historical_metrics = get_historical_metrics(db, start_time=start_time, end_time=now)
        logger.info(f"Got {len(historical_metrics)} historical metrics")
        
        db.close()
        
        logger.info("✅ traffic_analyzer.py is working correctly")
        return True
    except Exception as e:
        logger.error(f"❌ Error testing traffic_analyzer.py: {e}")
        return False

def test_network_data():
    """Test the network data API routes"""
    logger.info("Testing network_data.py...")
    try:
        from api.routes.network_data import get_current_metrics, get_metrics_history
        from api.models.network_models import TimeRange
        from database.db_connector import get_db
        
        # Create a mock request
        class MockRequest:
            def __init__(self):
                self.query_params = {}
        
        # Get database connection
        db = next(get_db())
        
        # Test get_current_metrics
        import asyncio
        metrics = asyncio.run(get_current_metrics(db))
        logger.info(f"Got current metrics: {metrics.get('timestamp')}")
        
        # Test get_metrics_history
        now = datetime.now()
        start_time = now - timedelta(minutes=15)
        historical_metrics = asyncio.run(get_metrics_history(TimeRange.FIFTEEN_MIN, start_time, now, db))
        logger.info(f"Got {len(historical_metrics)} historical metrics")
        
        db.close()
        
        logger.info("✅ network_data.py is working correctly")
        return True
    except Exception as e:
        logger.error(f"❌ Error testing network_data.py: {e}")
        return False

def main():
    """Main function"""
    logger.info("Starting tests...")
    
    # Add the current directory to the Python path
    sys.path.insert(0, os.path.abspath('.'))
    
    # Test each component
    results = {
        "packet_collector.py": test_packet_collector(),
        "db_connector.py": test_db_connector(),
        "traffic_analyzer.py": test_traffic_analyzer(),
        "network_data.py": test_network_data()
    }
    
    # Print summary
    logger.info("\nTest Results:")
    for component, result in results.items():
        logger.info(f"{component}: {'✅ PASS' if result else '❌ FAIL'}")
    
    # Return success if all tests passed
    return all(results.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
