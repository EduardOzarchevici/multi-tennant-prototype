from pydantic import BaseModel

class UserBase(BaseModel):
    id: int
    name: str
    email: str
    password: str
    role: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

class UserAuth(BaseModel):
    email: str
    password: str
    role: str

class UserOut(UserBase):
    pass