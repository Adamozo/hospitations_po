from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL: str = "postgresql://postgres:postgres@127.0.0.1/po"
#SQLALCHEMY_DATABASE_URL: str = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal: sessionmaker = sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=engine)

Base = declarative_base()
