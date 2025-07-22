from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base

user_tenant_association = Table(
    'user_tenant_association',
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("tenant_id", ForeignKey("tenants.id"), primary_key=True),
)

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

    users = relationship(
        "User",
        secondary=user_tenant_association,
        back_populates="tenants"
    )

