from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import select, text

from models.tenant_model import Tenant
from models.user_model import User
from models.tenant_models_specific import create_tenant_schema_and_tables
from core.db import engine
from schemas.tenant_schema import TenantCreate
from schemas.account_schema import *


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

def resolve_read_tenant(db: Session):
    return db.query(Tenant).all()

def resolve_delete_tenant(db:Session, tenant_id):
    tenant = db.scalar(select(Tenant).where(Tenant.id == tenant_id))

    # Dacă nu există, returnează eroare 404
    if tenant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")

    schema_name = tenant.name
    db.execute(text(f'DROP SCHEMA IF EXISTS "{schema_name}" CASCADE'))

    # Șterge tenantul
    db.delete(tenant)
    db.commit()

    return {"message": f"Tenant with id {tenant_id} deleted successfully"}


def resolve_create_account(account_data: AccountCreate, db: Session, user_data, Account):
    account = db.execute(select(Account).where(Account.accountName == account_data.account_name)).first()

    if account:
        raise HTTPException(status_code=400, detail='Account name already exists')

    new_account = Account(
        balance=0,
        accountName=account_data.account_name,
    )

    try:

        user = db.scalar(select(User).where(User.email == user_data['email']))
        if not user:
            raise HTTPException(status_code=400, detail='User not found')

        # new_account.owners.append(user)

        db.add(new_account)
        db.commit()
        db.refresh(new_account)
    except Exception as e:
        db.rollback()
        raise e

    return new_account

def resolve_read_accounts(Account, db):

    return db.query(Account).all()

