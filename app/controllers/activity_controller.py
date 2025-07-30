from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import select, text

from models.tenant_model import Tenant
from models.user_model import User
from models.tenant_models_specific import create_tenant_schema_and_tables
from core.db import engine
from schemas.activity_schema import *

def resolve_create_activity(data: ActivityCreate, Activity, session: Session):

    new_activity = Activity(**data.dict())
    session.add(new_activity)
    session.commit()
    session.refresh(new_activity)
    return new_activity


def resolve_get_activities(Activity, session: Session):
    return session.query(Activity).all()

def resolve_delete_activity(session: Session, activity_id: int, Activity):

    activity = session.query(Activity).get(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    session.delete(activity)
    session.commit()
    return {"message": "Activity deleted"}