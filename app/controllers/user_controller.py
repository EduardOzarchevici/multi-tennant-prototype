from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import select

from schemas.user_schema import *
from auth import *
from models.user_model import User, UserRole

def resolve_login(user: UserAuth, db: Session):
    user = authenticate_user(db, user.email, user.password)
    if user:
        token = create_access_token({
            "sub": user.email,
            "role": user.role
        })
        return {'token': token,
                'userdata': user}

def resolve_register(user: UserCreate, db: Session):
    result = db.execute(select(User).where(User.email == user.email)).first()

    if result:
        raise HTTPException(status_code=400, detail='Email already in use')

    try:
        new_user = User(
            name=user.name,
            email=user.email,
            role=user.role.lower(),
            hashed_password=get_password_hash(user.password)
        )

        db.add(new_user)
        db.commit()
    except Exception as e:
        raise e

    return new_user

