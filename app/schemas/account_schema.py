from pydantic import BaseModel

class AccountBase(BaseModel):
    id: int
    account_name: str
    balance: str


class AccountCreate(BaseModel):
    account_name: str

class AccountRead(BaseModel):
    account_name: str

