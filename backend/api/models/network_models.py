from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class TimeRange(str, Enum):
    FIVE_MIN = "5m"
    FIFTEEN_MIN = "15m"
    THIRTY_MIN = "30m"
    ONE_HOUR = "1h"
    SIX_HOURS = "6h"
    ONE_DAY = "24h"

class IPInfo(BaseModel):
    ip: str
    count: int
    location: Optional[str] = None
    latency: Optional[float] = None

class PortTraffic(BaseModel):
    port: int
    bytes: int

class ProtocolDistribution(BaseModel):
    tcp: float
    udp: float

class NetworkMetricsResponse(BaseModel):
    timestamp: datetime
    incoming_traffic: float = Field(..., description="Incoming traffic in Mbps")
    outgoing_traffic: float = Field(..., description="Outgoing traffic in Mbps")
    active_connections: int
    top_source_ips: List[IPInfo]
    top_dest_ips: List[IPInfo]
    protocols: ProtocolDistribution
    port_traffic: List[PortTraffic]
    average_latency: float = Field(..., description="Average latency in ms")
    packet_loss: float = Field(..., description="Packet loss percentage")

class NetworkMetricsCreate(BaseModel):
    timestamp: datetime
    incoming_traffic: float
    outgoing_traffic: float
    active_connections: int
    top_source_ips: List[IPInfo]
    top_dest_ips: List[IPInfo]
    protocols: ProtocolDistribution
    port_traffic: List[PortTraffic]
    average_latency: float
    packet_loss: float

class Filter(BaseModel):
    port: Optional[int] = None
    protocol: Optional[str] = None
    min_traffic: Optional[float] = None
    max_latency: Optional[float] = None
