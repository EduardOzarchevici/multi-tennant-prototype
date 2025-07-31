from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import List

from models.tenant_models_specific import get_tenant_base
from auth import *
from routers.tenant_routes import get_tenant_session, get_tenant_model
from schemas.receipt_schema import *
from controllers.receipt_controller import *


receipt_router = APIRouter()

@receipt_router.post('/receipts', response_model=ReceiptOut)
def create_receipt(
    data: ReceiptCreate = Body(),
    session_and_tenant: tuple = Depends(get_tenant_session),
    user_data = Depends(token_required)
):
    session, tenant = session_and_tenant
    _, _, _, _ , Receipt, *_ = get_tenant_model(tenant)
    return resolve_create_receipt(session, data, Receipt)

@receipt_router.get('/receipts', response_model=List[ReceiptOut])
def list_receipts(
    session_and_tenant: tuple = Depends(get_tenant_session),
    user_data = Depends(token_required)
):
    session, tenant = session_and_tenant
    _, _, _, _ , Receipt, *_ = get_tenant_model(tenant)

    return resolve_get_receipts(session, Receipt)


@receipt_router.delete('/receipts/{receipt_id}')
def delete_receipt(
    receipt_id: int,
    session_and_tenant: tuple = Depends(get_tenant_session),
    user_data = Depends(token_required)
):
    session, tenant = session_and_tenant
    _, _, _, _ , Receipt, *_ = get_tenant_model(tenant)

    return resolve_delete_receipt(session, receipt_id, Receipt)