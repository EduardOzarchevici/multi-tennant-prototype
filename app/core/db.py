from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base


from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"sslmode":"require"}
)

def get_public_session():
    session = Session(bind=engine)
    yield session

def get_tennant_session(tennat_name: str):
    pass

Base = declarative_base()


#Base.metadata.create_all(bind=engine)
