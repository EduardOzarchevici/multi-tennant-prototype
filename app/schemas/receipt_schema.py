from pydantic import BaseModel
from typing import Optional

class ReceiptCreate(BaseModel):
    path: str
    parentkey: str

class ReceiptUpdate(BaseModel):
    path: Optional[str]
    parentkey: Optional[str]

class ReceiptOut(BaseModel):
    id: int
    path: str
    parentkey: str

    class Config:
        from_attributes = True
