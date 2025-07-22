from sqlalchemy import MetaData, Column, Integer, String, text
from sqlalchemy.orm import declarative_base

# metadata global, fără schema setată încă
# tenant_metadata = MetaData()
#
# Base = declarative_base(metadata=tenant_metadata)

#
# class Todo(Base):
#     __tablename__ = 'todo'
#     id = Column(Integer, primary_key=True)
#     title = Column(String)

def get_tenant_base(tenant_schema_name: str):
    metadata = MetaData(schema=tenant_schema_name)
    Base = declarative_base(metadata=metadata)

    class Todo(Base):
        __tablename__ = 'todo'
        id = Column(Integer, primary_key=True)
        title = Column(String)

    return Base, Todo

# cand creezi schema noua pentru tenant
def create_tenant_schema_and_tables(engine, tenant_schema_name):
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {tenant_schema_name}"))
        conn.commit()

    TenantBase, Todo = get_tenant_base(tenant_schema_name)
    TenantBase.metadata.create_all(bind=engine)
