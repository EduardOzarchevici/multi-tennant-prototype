from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base

user_tenant_association = Table(
    'user_tenant_association',
    Base.metadata,
    Column("user_id", ForeignKey("public.users.id"), primary_key=True),
    Column("tenant_id", ForeignKey("public.tenants.id"), primary_key=True),
    schema='public'
)

class Tenant(Base):
    __tablename__ = "tenants"
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

    users = relationship(
        "User",
        secondary=user_tenant_association,
        back_populates="tenants"
    )

