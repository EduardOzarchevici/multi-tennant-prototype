import enum
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import ENUM as PGEnum

from .tenant_model import user_tenant_association
from core.db import Base


class UserRole(enum.Enum):
    ADMIN = 'admin'
    USER = 'user'
user_role_enum = PGEnum('admin', 'user', name='userrole', create_type=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(user_role_enum, nullable=False, default='user')
    tenants = relationship(
        "Tenant",
        secondary=user_tenant_association,
        back_populates="users"
    )

