from sqlalchemy import MetaData, Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Table, Numeric, text
from sqlalchemy.orm import declarative_base, relationship, registry

from models.user_model import User

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
    metadata = MetaData(schema=tenant_schema_name)  # setăm schema aici

    mapper_registry = registry(metadata=metadata)  # aici punem metadata la registry

    Base = mapper_registry.generate_base()

    account_owner_table = Table(
        'AccountOwners',
        Base.metadata,
        Column('accountId', Integer, ForeignKey(f'{tenant_schema_name}.account.id'), primary_key=True),
        Column('ownerId', Integer, primary_key=True),
        schema=tenant_schema_name,
        extend_existing=True
    )

    class Account(Base):
        __tablename__ = 'account'
        __table_args__ = {'schema': tenant_schema_name, 'extend_existing': True}

        id = Column(Integer, primary_key=True)
        balance = Column(Numeric(10, 2))
        accountName = Column(String(45))

        # ✅ Relație cu User din public
        # owners = relationship(
        #     "User",
        #     secondary=account_owner_table,
        #     backref="accounts"
        # )

    # restul claselor: la fel, dar adaugă __table_args__ cu schema
    class Activity(Base):
        __tablename__ = 'activity'
        __table_args__ = {'schema': tenant_schema_name, 'extend_existing': True}
        id = Column(Integer, primary_key=True, autoincrement=True)
        userName = Column(String(255), nullable=False)
        event = Column(String(255), nullable=False)
        creationdate = Column(DateTime, nullable=False)
        parentkey = Column(Integer)

    class Project(Base):
        __tablename__ = 'projects'
        __table_args__ = {'schema': tenant_schema_name, 'extend_existing': True}
        id = Column(Integer, primary_key=True)
        name = Column(String(255), nullable=False)
        creationDate = Column(DateTime, nullable=False)
        status = Column(String(255), nullable=False)
        projectType = Column(String(255), nullable=False)
        amountdonated = Column(Numeric(10, 2), default=0.00)
        amountspent = Column(Numeric(10, 2), default=0.00)

        tasks = relationship("Task", back_populates="project")
        transactions = relationship("Transaction", back_populates="project")

    class Receipt(Base):
        __tablename__ = 'receipt'
        __table_args__ = {'schema': tenant_schema_name, 'extend_existing': True}
        id = Column(Integer, primary_key=True)
        path = Column(Text, nullable=False)
        parentkey = Column(String(45), nullable=False)

    class Task(Base):
        __tablename__ = 'task'
        __table_args__ = {'schema': tenant_schema_name, 'extend_existing': True}
        id = Column(Integer, primary_key=True)
        createdby = Column(Integer, nullable=False)
        tasktype = Column(String(45), nullable=False)
        assignedto = Column(Integer, default=0)
        tasktitle = Column(String(255), nullable=False)
        duedate = Column(DateTime)
        completed = Column(Boolean, default=False)
        completedate = Column(DateTime)
        projectKey = Column(Integer, ForeignKey(f'{tenant_schema_name}.projects.id'))
        creationdate = Column(DateTime)

        project = relationship("Project", back_populates="tasks")
        items = relationship("ShoppingItem", back_populates="task")

    class ShoppingItem(Base):
        __tablename__ = 'shoppingitems'
        __table_args__ = {'schema': tenant_schema_name, 'extend_existing': True}
        id = Column(Integer, primary_key=True)
        taskid = Column(Integer, ForeignKey(f'{tenant_schema_name}.task.id'), nullable=False)
        name = Column(String(255), nullable=False)
        quantity = Column(Integer)
        purchased = Column(Boolean, default=False)
        userid = Column(Integer)

        task = relationship("Task", back_populates="items")

    class Transaction(Base):
        __tablename__ = 'transactions'
        __table_args__ = {'schema': tenant_schema_name, 'extend_existing': True}
        id = Column(Integer, primary_key=True)
        amount = Column(Numeric(10, 2), nullable=False)
        projectKey = Column(Integer, ForeignKey(f'{tenant_schema_name}.projects.id'))
        type = Column(String(255))
        creationdate = Column(DateTime)
        donator = Column(String(255))
        detalii = Column(String(255))
        ownerKey = Column(Integer)
        fromAccount = Column(String(45))
        toAccount = Column(String(45))

        project = relationship("Project", back_populates="transactions")

    return Base, account_owner_table, Account, Activity, Project, Receipt, Task, ShoppingItem, Transaction

# cand creezi schema noua pentru tenant
def create_tenant_schema_and_tables(engine, tenant_schema_name):
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {tenant_schema_name}"))
        conn.commit()

    TenantBase, *_ = get_tenant_base(tenant_schema_name)
    TenantBase.metadata.create_all(bind=engine)
