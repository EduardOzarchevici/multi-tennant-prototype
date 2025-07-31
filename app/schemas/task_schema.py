from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    tasktype: str
    assignedto: Optional[int] = 0
    tasktitle: str
    duedate: Optional[datetime] = None
    completed: Optional[bool] = False
    completedate: Optional[datetime] = None
    projectKey: Optional[int] = None

class TaskUpdate(BaseModel):
    tasktype: Optional[str]
    assignedto: Optional[int]
    tasktitle: Optional[str]
    duedate: Optional[datetime]
    completed: Optional[bool]
    completedate: Optional[datetime]
    projectKey: Optional[int]

class TaskOut(BaseModel):
    id: int
    createdby: int
    tasktype: str
    assignedto: int
    tasktitle: str
    duedate: Optional[datetime]
    completed: bool
    completedate: Optional[datetime]
    projectKey: Optional[int]
    creationdate: Optional[datetime]

    class Config:
        from_attributes = True
