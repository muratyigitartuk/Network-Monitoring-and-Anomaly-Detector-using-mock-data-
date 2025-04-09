from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment variables
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Import local modules
try:
    # Try importing with 'backend.' prefix first
    from backend.api.routes import network_data, alerts, users, config
    from backend.collectors.packet_collector import start_packet_collection, stop_packet_collection
    from backend.database.db_connector import init_db
    print("Imported modules with 'backend.' prefix")
except ImportError:
    try:
        # If that fails, try importing directly
        from api.routes import network_data, alerts, users, config
        from collectors.packet_collector import start_packet_collection, stop_packet_collection
        from database.db_connector import init_db
        print("Imported modules directly")
    except ImportError as e:
        print(f"Error importing modules: {e}")
        # Define dummy functions as fallback
        async def init_db():
            print("Using dummy init_db function")
            pass

        def start_packet_collection():
            print("Using dummy start_packet_collection function")
            pass

        def stop_packet_collection():
            print("Using dummy stop_packet_collection function")
            pass

        # These will be imported later when needed

app = FastAPI(
    title="Network Anomaly Detection API",
    description="API for collecting and analyzing network traffic data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(network_data.router, prefix="/api/network", tags=["Network Data"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(config.router, prefix="/api/config", tags=["Configuration"])

# Mount static files directory
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    print(f"Mounted static files directory: {static_dir}")
else:
    print(f"Static directory not found: {static_dir}")
    # Create the directory
    static_dir.mkdir(exist_ok=True)
    print(f"Created static directory: {static_dir}")

# Use lifespan context manager instead of deprecated on_event
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    # Startup
    try:
        print("Initializing application...")
        await init_db()
        print("Database initialized")
        start_packet_collection()
        print("Packet collection started")
        yield
    except Exception as e:
        print(f"Error during startup: {e}")
        yield
    finally:
        # Shutdown
        try:
            print("Shutting down application...")
            stop_packet_collection()
            print("Packet collection stopped")
        except Exception as e:
            print(f"Error during shutdown: {e}")

# Assign lifespan to app
app.router.lifespan_context = lifespan

@app.get("/")
async def root():
    # Serve the simplified charts if it exists
    simple_charts_path = Path(__file__).parent / "static" / "simple-charts.html"
    if simple_charts_path.exists():
        return FileResponse(simple_charts_path)

    # Try the simplified dashboard
    simple_dashboard_path = Path(__file__).parent / "static" / "simple-dashboard.html"
    if simple_dashboard_path.exists():
        return FileResponse(simple_dashboard_path)

    # Try the regular dashboard
    index_path = Path(__file__).parent / "static" / "index.html"
    if index_path.exists():
        return FileResponse(index_path)

    # Fallback to API info
    return {"message": "Network Anomaly Detection API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    print(f"Starting API server on {API_HOST}:{API_PORT}")
    print(f"Debug mode: {DEBUG}")
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=DEBUG)
