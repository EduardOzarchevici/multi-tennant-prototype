from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class ProjectCreate(BaseModel):
    name: str
    creationDate: datetime
    status: str
    projectType: str
    amountdonated: Optional[Decimal] = 0.00
    amountspent: Optional[Decimal] = 0.00

class ProjectUpdate(BaseModel):
    name: Optional[str]
    status: Optional[str]
    projectType: Optional[str]
    amountdonated: Optional[Decimal]
    amountspent: Optional[Decimal]

class ProjectOut(BaseModel):
    id: int
    name: str
    creationDate: datetime
    status: str
    projectType: str
    amountdonated: Decimal
    amountspent: Decimal

    class Config:
        orm_mode = True
