from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import List

from models.tenant_models_specific import get_tenant_base
from auth import *
from routers.tenant_routes import get_tenant_session, get_tenant_model
from schemas.task_schema import *
from controllers.task_controller import *


task_router = APIRouter()

@task_router.post('/tasks', response_model=TaskOut)
def create_task(
    data: TaskCreate = Body(),
    session_and_tenant: tuple = Depends(get_tenant_session),
    user_data = Depends(token_required)
):
    session, tenant = session_and_tenant
    _, _, _, _ , _, Task, *_ = get_tenant_model(tenant)

    return resolve_create_task(session, data, Task, user_data)

@task_router.get('/tasks', response_model=List[TaskOut])
def list_tasks(
    session_and_tenant: tuple = Depends(get_tenant_session),
    user_data = Depends(token_required)
):
    session, tenant = session_and_tenant
    _, _, _, _ , _, Task, *_ = get_tenant_model(tenant)

    return resolve_get_tasks(session, Task)


@task_router.delete('/tasks/{task_id}')
def delete_task(
    task_id: int,
    session_and_tenant: tuple = Depends(get_tenant_session),
    user_data = Depends(token_required)
):
    session, tenant = session_and_tenant
    _, _, _, _ , _, Task, *_ = get_tenant_model(tenant)

    return resolve_delete_task(session, task_id, Task)