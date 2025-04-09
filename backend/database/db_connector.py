import os
import logging
from datetime import datetime
from typing import Generator, AsyncGenerator, Dict, Any, Optional, List, Union

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Try to import SQLAlchemy
try:
    from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, relationship
    SQLALCHEMY_AVAILABLE = True
    logger.info("SQLAlchemy successfully imported")

    # Try to import async SQLAlchemy components
    try:
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.future import select
        ASYNC_AVAILABLE = True
        logger.info("Async SQLAlchemy components successfully imported")
    except ImportError as e:
        logger.warning(f"Async SQLAlchemy not available: {e}. Using synchronous operations only.")
        ASYNC_AVAILABLE = False
except ImportError as e:
    logger.error(f"SQLAlchemy not available: {e}. Database functionality will be limited.")
    SQLALCHEMY_AVAILABLE = False
    ASYNC_AVAILABLE = False

    # Define dummy classes and functions for fallback
    class Column:
        def __init__(self, *args, **kwargs):
            pass

    class Integer:
        pass

    class String:
        pass

    class Float:
        pass

    class Boolean:
        pass

    class DateTime:
        pass

    class ForeignKey:
        def __init__(self, *args, **kwargs):
            pass

    class JSON:
        pass

    def relationship(*args, **kwargs):
        pass

    def create_engine(*args, **kwargs):
        pass

    def declarative_base():
        class Base:
            pass
        return Base

    def sessionmaker(*args, **kwargs):
        class Session:
            def __init__(self):
                pass
            def close(self):
                pass
            def commit(self):
                pass
            def rollback(self):
                pass
            def add(self, obj):
                pass
            def query(self, *args):
                class Query:
                    def filter(self, *args):
                        return self
                    def first(self):
                        return None
                return Query()
        return Session

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./network_monitor.db")
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL", "sqlite+aiosqlite:///./network_monitor.db")

# Initialize variables
engine = None
SessionLocal = None
AsyncSessionLocal = None
Base = None
JSON_TYPE = None

# Only proceed with SQLAlchemy setup if it's available
if SQLALCHEMY_AVAILABLE:
    # Check if JSON type is supported
    try:
        from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
        JSON_TYPE = JSON
    except ImportError:
        # Fallback for older SQLAlchemy versions
        logger.warning("JSON type not available in SQLAlchemy. Using String instead.")
        JSON_TYPE = String

    # Create declarative base
    Base = declarative_base()

    # For SQLite, use this engine for synchronous operations
    try:
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        logger.info(f"Created database engine for {DATABASE_URL}")
    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")
        # Create a memory SQLite database as fallback
        DATABASE_URL = "sqlite:///:memory:"
        try:
            engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
            logger.info("Using in-memory SQLite database as fallback")
        except Exception as inner_e:
            logger.error(f"Failed to create in-memory database: {inner_e}")
            engine = None

    # Session factory for synchronous operations
    if engine is not None:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # For asynchronous operations (if available)
    if ASYNC_AVAILABLE:
        try:
            async_engine = create_async_engine(ASYNC_DATABASE_URL)
            AsyncSessionLocal = sessionmaker(class_=AsyncSession, expire_on_commit=False, bind=async_engine)
            logger.info(f"Created async database engine for {ASYNC_DATABASE_URL}")
        except Exception as e:
            logger.error(f"Failed to create async database engine: {e}")
            ASYNC_AVAILABLE = False
else:
    # Create dummy base class if SQLAlchemy is not available
    class DummyBase:
        pass

    Base = DummyBase
    JSON_TYPE = String  # Use the dummy String class defined earlier

# Base is now defined above

# Only define database models if SQLAlchemy is available
if SQLALCHEMY_AVAILABLE:
    # Database models
    class NetworkMetrics(Base):
        __tablename__ = "network_metrics"

        id = Column(Integer, primary_key=True, index=True)
        timestamp = Column(DateTime, default=datetime.now)
        incoming_traffic = Column(Float)
        outgoing_traffic = Column(Float)
        active_connections = Column(Integer)
        average_latency = Column(Float)
        packet_loss = Column(Float)
        protocols = Column(JSON_TYPE)  # Store protocol distribution as JSON

        # Relationships
        source_ips = relationship("SourceIP", back_populates="metrics")
        dest_ips = relationship("DestinationIP", back_populates="metrics")
        port_traffic = relationship("PortTraffic", back_populates="metrics")

    class SourceIP(Base):
        __tablename__ = "source_ips"

        id = Column(Integer, primary_key=True, index=True)
        metrics_id = Column(Integer, ForeignKey("network_metrics.id"))
        ip_address = Column(String)
        count = Column(Integer)
        location = Column(String, nullable=True)
        latency = Column(Float, nullable=True)

        metrics = relationship("NetworkMetrics", back_populates="source_ips")

    class DestinationIP(Base):
        __tablename__ = "destination_ips"

        id = Column(Integer, primary_key=True, index=True)
        metrics_id = Column(Integer, ForeignKey("network_metrics.id"))
        ip_address = Column(String)
        count = Column(Integer)
        location = Column(String, nullable=True)
        latency = Column(Float, nullable=True)

        metrics = relationship("NetworkMetrics", back_populates="dest_ips")

    class PortTraffic(Base):
        __tablename__ = "port_traffic"

        id = Column(Integer, primary_key=True, index=True)
        metrics_id = Column(Integer, ForeignKey("network_metrics.id"))
        port = Column(Integer)
        bytes = Column(Integer)

        metrics = relationship("NetworkMetrics", back_populates="port_traffic")

    class Alert(Base):
        __tablename__ = "alerts"

        id = Column(Integer, primary_key=True, index=True)
        message = Column(String)
        timestamp = Column(DateTime, default=datetime.now)
        type = Column(String)  # "warning" or "critical"
        acknowledged = Column(Boolean, default=False)

    class User(Base):
        __tablename__ = "users"

        id = Column(Integer, primary_key=True, index=True)
        username = Column(String, unique=True, index=True)
        email = Column(String, unique=True, index=True)
        hashed_password = Column(String)
        role = Column(String)  # "admin", "analyst", or "user"
        created_at = Column(DateTime, default=datetime.now)

    class Threshold(Base):
        __tablename__ = "thresholds"

        id = Column(Integer, primary_key=True, index=True)
        name = Column(String)
        metric = Column(String)  # "incomingTraffic", "outgoingTraffic", etc.
        value = Column(Float)
        type = Column(String)  # "warning" or "critical"
        enabled = Column(Boolean, default=True)
else:
    # Define dummy classes for type hints
    class NetworkMetrics:
        pass

    class SourceIP:
        pass

    class DestinationIP:
        pass

    class PortTraffic:
        pass

    class Alert:
        pass

    class User:
        pass

    class Threshold:
        pass

# Database initialization
async def init_db():
    if not SQLALCHEMY_AVAILABLE:
        logger.warning("SQLAlchemy not available. Skipping database initialization.")
        return

    if engine is None:
        logger.error("Database engine not available. Skipping database initialization.")
        return

    try:
        # Create tables if they don't exist
        # Use sync engine for simplicity
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")

        # Create default admin user if it doesn't exist
        try:
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

            db = SessionLocal()
            try:
                # Check if admin user exists
                admin = db.query(User).filter(User.username == "admin").first()
                if not admin:
                    # Create admin user
                    hashed_password = pwd_context.hash("password")
                    admin_user = User(
                        username="admin",
                        email="admin@example.com",
                        hashed_password=hashed_password,
                        role="admin"
                    )
                    db.add(admin_user)
                    db.commit()
                    logger.info("Default admin user created")
            except Exception as e:
                logger.error(f"Error creating admin user: {e}")
                # This might be because the User table doesn't exist yet
                # or because passlib is not installed
                pass
            finally:
                db.close()
        except ImportError as e:
            logger.warning(f"passlib not installed: {e}. Skipping admin user creation.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        # Don't raise the exception, just log it
        # This allows the application to start even if the database initialization fails

# Dependency to get DB session (synchronous)
def get_db() -> Generator:
    if not SQLALCHEMY_AVAILABLE or SessionLocal is None:
        # Return a dummy session that does nothing
        class DummySession:
            def close(self):
                pass
            def commit(self):
                pass
            def rollback(self):
                pass
            def add(self, obj):
                pass
            def query(self, *args):
                class Query:
                    def filter(self, *args):
                        return self
                    def first(self):
                        return None
                    def all(self):
                        return []
                return Query()

        logger.warning("Database not available, using dummy session")
        dummy = DummySession()
        try:
            yield dummy
        finally:
            pass
    else:
        # Use real SQLAlchemy session
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

# Dependency to get async DB session (if available)
if ASYNC_AVAILABLE and AsyncSessionLocal is not None:
    async def get_async_db() -> AsyncGenerator:
        async_session = AsyncSessionLocal()
        try:
            yield async_session
        finally:
            await async_session.close()
else:
    # Fallback for when async is not available
    async def get_async_db() -> Generator:
        logger.warning("Async database not available, using synchronous session instead")
        return get_db()
