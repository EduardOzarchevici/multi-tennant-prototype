from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import List

from models.tenant_models_specific import get_tenant_base
from auth import *
from routers.tenant_routes import get_tenant_session, get_tenant_model
from schemas.activity_schema import ActivityCreate, ActivityUpdate, ActivityOut
from controllers.activity_controller import *

activity_router = APIRouter()

@activity_router.post('/activities', response_model=ActivityOut)
def create_activity(
    data: ActivityCreate = Body(),
    session_and_tenant: tuple = Depends(get_tenant_session),
    user_data = Depends(token_required)
):
    session, tenant = session_and_tenant
    _, _, Activity , *_ = get_tenant_model(tenant)
    return resolve_create_activity(data, Activity, session)

@activity_router.get('/activities', response_model=List[ActivityOut])
def list_activities(
    session_and_tenant: tuple = Depends(get_tenant_session),
    user_data = Depends(token_required)
):
    session, tenant = session_and_tenant
    _, _, Activity, *_ = get_tenant_model(tenant)
    return resolve_get_activities(Activity, session)


@activity_router.delete('/activities/{activity_id}')
def delete_activity(
    activity_id: int,
    session_and_tenant: tuple = Depends(get_tenant_session),
    user_data = Depends(token_required)
):
    session, tenant = session_and_tenant
    _, _, Activity, *_ = get_tenant_model(tenant)
    return resolve_delete_activity(session, activity_id, Activity)