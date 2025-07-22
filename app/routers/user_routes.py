from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.user_schema import *
from core.db import get_public_session
from controllers.user_controller import *

user_router = APIRouter()

@user_router.post('/login')
def login(user: UserAuth, db: Session = Depends(get_public_session)):
    response = resolve_login(user, db)
    if response==False:
        raise HTTPException(status_code=400, detail=f'Could not auth the user: {user.email} ')
    else:
        return response

@user_router.post('/register')
def register(user: UserCreate, db: Session = Depends(get_public_session)):
    return resolve_register(user, db)

@user_router.get('/me')
def protected_route(userData = Depends(token_required)):
    return userData