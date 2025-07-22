from pydantic import BaseModel

class TenantBase(BaseModel):
    id: int
    name: str
    email: str

class TenantCreate(BaseModel):
    tenant_name: str
    tenant_email: str
    
