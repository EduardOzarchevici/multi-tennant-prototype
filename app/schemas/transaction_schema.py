from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionCreate(BaseModel):
    amount: float
    projectKey: int
    type: Optional[str] = None
    donator: Optional[str] = None
    detalii: Optional[str] = None
    fromAccount: Optional[str] = None
    toAccount: Optional[str] = None

class TransactionUpdate(BaseModel):
    amount: Optional[float]
    projectKey: Optional[int]
    type: Optional[str]
    donator: Optional[str]
    detalii: Optional[str]
    fromAccount: Optional[str]
    toAccount: Optional[str]

class TransactionOut(BaseModel):
    id: int
    amount: float
    projectKey: Optional[int]
    type: Optional[str]
    creationdate: Optional[datetime]
    donator: Optional[str]
    detalii: Optional[str]
    ownerKey: Optional[int]
    fromAccount: Optional[str]
    toAccount: Optional[str]

    class Config:
        from_attributes = True
