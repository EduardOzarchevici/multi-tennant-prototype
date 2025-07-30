from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import List

from models.tenant_models_specific import get_tenant_base
from auth import *
from routers.tenant_routes import get_tenant_session, get_tenant_model
from schemas.project_schema import *
from controllers.project_controller import *


project_router = APIRouter()

@project_router.post('/projects', response_model=ProjectOut)
def create_project(
    data: ProjectCreate = Body(),
    session_and_tenant: tuple = Depends(get_tenant_session),
    user_data = Depends(token_required)
):
    session, tenant = session_and_tenant
    _, _, _, Project, *_ = get_tenant_model(tenant)

    return resolve_create_project(session, data, Project)

@project_router.get('/projects', response_model=List[ProjectOut])
def list_projects(
    session_and_tenant: tuple = Depends(get_tenant_session),
    user_data = Depends(token_required)
):
    session, tenant = session_and_tenant
    _, _, _, Project, *_ = get_tenant_model(tenant)

    return resolve_get_projects(session, Project)


@project_router.delete('/projects/{project_id}')
def delete_project(
    project_id: int,
    session_and_tenant: tuple = Depends(get_tenant_session),
    user_data = Depends(token_required)
):
    session, tenant = session_and_tenant
    _, _, _, Project, *_ = get_tenant_model(tenant)

    return resolve_delete_project(session, project_id, Project)
