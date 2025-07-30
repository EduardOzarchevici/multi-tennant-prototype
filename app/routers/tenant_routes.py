from fastapi import APIRouter, Depends, Path, Body, Header, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from typing import Annotated

from schemas.tenant_schema import *
from schemas.account_schema import *
from core.db import get_public_session, engine
from controllers.tenant_controller import *
from models.tenant_models_specific import get_tenant_base
from auth import *

tenant_router = APIRouter()

class TodoCreate(BaseModel):
    title: str

def get_tenant_session(tenant: Annotated[str, Header(alias="X-Tenant")]):
    session = Session(bind=engine)
    try:
        # Verifică dacă schema există în pg_namespace
        result = session.execute(
            text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = :tenant"),
            {"tenant": tenant}
        ).scalar()

        if result is None:
            raise HTTPException(status_code=400, detail=f"Schema '{tenant}' does not exist.")

        # Setează search_path la schema respectivă
        session.execute(text(f"SET search_path TO {tenant}"))
        yield session, tenant
    finally:
        session.close()

def get_tenant_model(tenant_name: str):
    _, account_owner_table, Account, Activity, Project, Receipt, Task, ShoppingItem, Transaction = get_tenant_base(tenant_name)
    return Account, account_owner_table, Activity, Project, Receipt, Task, ShoppingItem, Transaction


''''--------------TENANTS--------------'''

@tenant_router.post('/tenants')
def create_tenant(tenant_data: TenantCreate, user_data = Depends(token_required), db: Session = Depends(get_public_session)):
    # return [tenant_data, user_data['email']]
    return resolve_create_tenant(tenant_data, user_data, db)

@tenant_router.get('/tenants')
def read_tenant(user_data=Depends(token_required), db: Session = Depends(get_public_session)):
    if user_data['role'] != 'admin':
        raise HTTPException(status_code=403, detail='Not allowed')
    return resolve_read_tenant(db)

@tenant_router.delete('/tenants/{tenant_id}')
def delete_tenant(tenant_id: int ,user_data=Depends(token_required), db: Session = Depends(get_public_session)):
    if user_data['role'] != 'admin':
        raise HTTPException(status_code=403, detail='Not allowed')
    return resolve_delete_tenant(db, tenant_id)


''''--------------ACCOUNTS--------------'''

@tenant_router.post('/accounts')
def create_account(
        account_data: AccountCreate = Body(),
        session_and_tenant: tuple = Depends(get_tenant_session),
        user_data = Depends(token_required)
):
    session, tenant = session_and_tenant
    Account, account_owner_table, *_ = get_tenant_model(tenant)
    return resolve_create_account(account_data, session, user_data, Account, account_owner_table)

@tenant_router.get('/accounts')
def read_accounts(
        session_and_tenant: tuple = Depends(get_tenant_session),
        user_data = Depends(token_required)
):
    if user_data['role'] != 'admin':
        raise HTTPException(status_code=403, detail='Not allowed')

    session, tenant = session_and_tenant
    Account, *_ = get_tenant_model(tenant)

    return resolve_read_accounts(Account, session)

@tenant_router.patch('/accounts/{account_id}')
def change_account_balance(
        account_id: int,
        data: AccountBalanceUpdate = Body(),
        session_and_tenant: tuple = Depends(get_tenant_session),
        user_data = Depends(token_required),
):
    session, tenant = session_and_tenant
    Account, *_ = get_tenant_model(tenant)

    return  resolve_change_account_balance(account_id, data.account_balance, session, Account)
