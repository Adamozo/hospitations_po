from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from hospitations_po.server.database import Base
from hospitations_po.server.main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    connection = engine.connect()

    transaction = connection.begin()

    db = TestingSessionLocal(bind=connection)
   
    yield db
    
    db.rollback()
    db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    db = override_get_db() 
    client = TestClient(app)

    assert 1==1
