from fastapi import APIRouter, Depends, Path, Body, Header
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from typing import Annotated

from schemas.tenant_schema import *
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
    _, Todo = get_tenant_base(tenant_name)
    return Todo

def get_tenant_model_from_header():
    pass

@tenant_router.post('/tenants')
def create_tenant(tenant_data: TenantCreate, user_data = Depends(token_required), db: Session = Depends(get_public_session)):
    # return [tenant_data, user_data['email']]
    return resolve_create_tenant(tenant_data, user_data, db)


@tenant_router.get("/tenants/todos")
def read_todos(session_and_tenant: tuple = Depends(get_tenant_session), userData = Depends(token_required)):
    session, tenant = session_and_tenant
    Todo = get_tenant_model(tenant)
    return session.query(Todo).all()


@tenant_router.post("/tenants/todos")
def create_todo(
    todo_data: TodoCreate = Body(...),
    session_and_tenant: tuple = Depends(get_tenant_session),
    userData = Depends(token_required)):

    session, tenant = session_and_tenant
    Todo = get_tenant_model(tenant)

    todo = Todo(title=todo_data.title)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    return {"id": todo.id, "title": todo.title}