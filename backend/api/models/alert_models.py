from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class AlertType(str, Enum):
    WARNING = "warning"
    CRITICAL = "critical"

class Alert(BaseModel):
    id: str
    message: str
    timestamp: datetime
    type: AlertType
    acknowledged: bool = False

class AlertCreate(BaseModel):
    message: str
    type: AlertType = AlertType.WARNING
    
class AlertUpdate(BaseModel):
    message: Optional[str] = None
    type: Optional[AlertType] = None
    acknowledged: Optional[bool] = None
