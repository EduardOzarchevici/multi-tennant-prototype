from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import List

from models.tenant_models_specific import get_tenant_base
from auth import *
from routers.tenant_routes import get_tenant_session, get_tenant_model
from schemas.transaction_schema import *
from controllers.transaction_controller import *

transaction_router = APIRouter()


@transaction_router.post('/transactions', response_model=TransactionOut)
def create_transaction(
        data: TransactionCreate = Body(),
        session_and_tenant: tuple = Depends(get_tenant_session),
        user_data=Depends(token_required)
):
    session, tenant = session_and_tenant
    *_, Transaction = get_tenant_model(tenant)

    return resolve_create_transaction(session, data, Transaction, user_data)


@transaction_router.get('/transactions', response_model=List[TransactionOut])
def list_transactions(
        session_and_tenant: tuple = Depends(get_tenant_session),
        user_data=Depends(token_required)
):
    session, tenant = session_and_tenant
    *_, Transaction = get_tenant_model(tenant)

    return resolve_get_transactions(session, Transaction)


@transaction_router.delete('/transactions/{transaction_id}')
def delete_transaction(
        transaction_id: int,
        session_and_tenant: tuple = Depends(get_tenant_session),
        user_data=Depends(token_required)
):
    session, tenant = session_and_tenant
    *_, Transaction = get_tenant_model(tenant)

    return resolve_delete_transaction(session, transaction_id, Transaction)