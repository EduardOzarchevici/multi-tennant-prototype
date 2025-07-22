from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import select, text
from models.tenant_model import Tenant
from models.user_model import User
from models.tenant_models_specific import create_tenant_schema_and_tables
from core.db import engine

from schemas.tenant_schema import TenantCreate

def resolve_create_tenant(tenant_data: TenantCreate, user_data, db: Session):
    result = db.execute(select(Tenant).where(Tenant.email == tenant_data.tenant_email)).first()
    if result:
        raise HTTPException(status_code=400, detail='Email already in use')

    try:
        new_tenant = Tenant(
            name=tenant_data.tenant_name,
            email=tenant_data.tenant_email,
        )
        user = db.scalar(select(User).where(User.email == user_data['email']))
        if not user:
            raise HTTPException(status_code=400, detail='User not found')

        new_tenant.users.append(user)

        db.add(new_tenant)
        db.commit()
        db.refresh(new_tenant)

        create_tenant_schema_and_tables(engine, tenant_data.tenant_name)
    except Exception as e:
        db.rollback()
        raise e

    return new_tenant

