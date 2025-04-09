#!/usr/bin/env python
"""
Run script for the Network Anomaly Detection backend.
This script handles common errors and provides better error messages.
"""

import os
import sys
import subprocess
import time
import logging

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("dotenv not installed, using default environment variables")

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO")
log_file = os.getenv("LOG_FILE", "backend.log")

log_level_map = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

logging.basicConfig(
    level=log_level_map.get(log_level, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file)
    ]
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "dotenv",
        "scapy",
        "passlib",
        "python-jose",
        "python-multipart",
        "aiosqlite"
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)

    if not missing_packages:
        logger.info("All core dependencies are installed")
        return True

    logger.warning(f"Missing dependencies: {', '.join(missing_packages)}")
    logger.info("Installing dependencies...")

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("Dependencies installed successfully")

        # Verify installation
        still_missing = []
        for package in missing_packages:
            try:
                __import__(package.replace("-", "_"))
            except ImportError:
                still_missing.append(package)

        if still_missing:
            logger.warning(f"Some dependencies could not be installed: {', '.join(still_missing)}")
            logger.info("Continuing anyway, some features may not work")

        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        logger.info("Continuing anyway, some features may not work")
        return True

def check_database():
    """Check if the database file exists and is accessible"""
    from dotenv import load_dotenv
    load_dotenv()

    db_url = os.getenv("DATABASE_URL", "sqlite:///./network_monitor.db")
    if db_url.startswith("sqlite:///"):
        db_path = db_url.replace("sqlite:///", "")
        if not os.path.exists(db_path):
            logger.info(f"Database file {db_path} does not exist, it will be created on startup")
        else:
            logger.info(f"Database file {db_path} exists")
    else:
        logger.info(f"Using database: {db_url}")

def run_backend():
    """Run the backend server"""
    try:
        logger.info("Starting backend server...")

        # Get configuration from environment variables
        host = os.getenv("API_HOST", "0.0.0.0")
        port = int(os.getenv("API_PORT", "8000"))
        debug = os.getenv("DEBUG", "false").lower() == "true"

        # Check if we should enable authentication
        enable_auth = os.getenv("ENABLE_AUTHENTICATION", "true").lower() == "true"
        if not enable_auth:
            logger.warning("Authentication is disabled. This is not recommended for production.")
            os.environ["ENABLE_AUTHENTICATION"] = "false"

        # Check if we should enable WebSockets
        enable_ws = os.getenv("ENABLE_WEBSOCKETS", "true").lower() == "true"
        if not enable_ws:
            logger.warning("WebSockets are disabled. Real-time updates will not be available.")
            os.environ["ENABLE_WEBSOCKETS"] = "false"

        # Check if we should enable ML
        enable_ml = os.getenv("ENABLE_ML", "true").lower() == "true"
        if not enable_ml:
            logger.warning("Machine learning is disabled. Anomaly detection will use simple statistical methods.")
            os.environ["ENABLE_ML"] = "false"

        # Import the app after setting environment variables
        try:
            from main import app
            import uvicorn

            logger.info(f"Starting server on {host}:{port} (debug: {debug})")
            uvicorn.run(app, host=host, port=port, reload=debug)
        except ImportError as e:
            logger.error(f"Failed to import app: {e}")
            logger.info("Trying to run with module name instead...")

            # Try running with module name instead
            import uvicorn
            uvicorn.run("main:app", host=host, port=port, reload=debug)
    except Exception as e:
        logger.error(f"Failed to start backend server: {e}")
        return False
    return True

def main():
    """Main entry point"""
    logger.info("Starting Network Anomaly Detection backend")

    # Check dependencies
    if not check_dependencies():
        logger.error("Failed to check or install dependencies")
        return 1

    # Check database
    try:
        check_database()
    except Exception as e:
        logger.error(f"Database check failed: {e}")
        logger.info("Continuing anyway...")

    # Run backend
    try:
        run_backend()
    except KeyboardInterrupt:
        logger.info("Backend server stopped by user")
    except Exception as e:
        logger.error(f"Backend server failed: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
