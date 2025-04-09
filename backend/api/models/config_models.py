from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class MetricType(str, Enum):
    INCOMING_TRAFFIC = "incomingTraffic"
    OUTGOING_TRAFFIC = "outgoingTraffic"
    ACTIVE_CONNECTIONS = "activeConnections"
    AVERAGE_LATENCY = "averageLatency"
    PACKET_LOSS = "packetLoss"

class ThresholdType(str, Enum):
    WARNING = "warning"
    CRITICAL = "critical"

class Threshold(BaseModel):
    id: str
    name: str
    metric: MetricType
    value: float
    type: ThresholdType
    enabled: bool = True

class ThresholdCreate(BaseModel):
    name: str
    metric: MetricType
    value: float
    type: ThresholdType = ThresholdType.WARNING
    enabled: bool = True

class ThresholdUpdate(BaseModel):
    name: Optional[str] = None
    metric: Optional[MetricType] = None
    value: Optional[float] = None
    type: Optional[ThresholdType] = None
    enabled: Optional[bool] = None
