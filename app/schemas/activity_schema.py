from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ActivityCreate(BaseModel):
    userName: str
    event: str
    creationdate: datetime
    parentkey: Optional[int] = None

class ActivityUpdate(BaseModel):
    event: Optional[str] = None
    parentkey: Optional[int] = None

class ActivityOut(BaseModel):
    id: int
    userName: str
    event: str
    creationdate: datetime
    parentkey: Optional[int]

    class Config:
        from_attributes = True
