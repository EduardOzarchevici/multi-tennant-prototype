from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel

from schemas.tenant_schema import *
from core.db import get_public_session, engine
from controllers.tenant_controller import *
from models.tenant_models_specific import get_tenant_base
from auth import *

tenant_router = APIRouter()

class TodoCreate(BaseModel):
    title: str

def get_tenant_session(tenant: str):
    session = Session(bind=engine)
    try:
        session.execute(text(f"SET search_path TO {tenant}"))
        yield session
    finally:
        session.close()

def get_tenant_model(tenant_name: str):
    _, Todo = get_tenant_base(tenant_name)
    return Todo


@tenant_router.post('/tenants')
def create_tenant(tenant_data: TenantCreate, user_data = Depends(token_required), db: Session = Depends(get_public_session)):
    # return [tenant_data, user_data['email']]
    return resolve_create_tenant(tenant_data, user_data, db)


@tenant_router.get("/tenants/{tenant}/todos")
def read_todos(tenant: str, session: Session = Depends(get_tenant_session)):
    Todo = get_tenant_model(tenant)
    return session.query(Todo).all()

@tenant_router.post("/tenants/{tenant_name}/todos")
def create_todo(
    tenant_name: str = Path(...),
    todo_data: TodoCreate = Body(...),
    session: Session = Depends(get_tenant_session),
):
    Todo = get_tenant_model(tenant_name)

    todo = Todo(title=todo_data.title)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    return {"id": todo.id, "title": todo.title}