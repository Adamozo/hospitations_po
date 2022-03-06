from cgi import test
import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime

from hospitations_po.server.database import Base
from hospitations_po.server.models import *
from hospitations_po.server.main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///tests/test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)

# Base.metadata.create_all(bind=engine)


def override_get_db():
    connection = engine.connect()

    transaction = connection.begin()

    db = TestingSessionLocal(bind=connection)

    yield db

    db.rollback()
    db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_api_get_protocols_tutor():
    # tutor with course
    response = client.get("/protokoly/prowadzacy/1?tutor_id=1")
    assert response.status_code == 200

    # tutor from database without course
    response = client.get("/protokoly/prowadzacy/2?tutor_id=2")
    assert response.status_code == 404

    # tutor not even in database
    response = client.get("/protokoly/prowadzacy7?tutor_id=7")
    assert response.status_code == 404


def test_api_get_protocol_info():
    # protocole that exists
    response = client.get("/protokol/1?protocol_id=1")
    assert response.status_code == 200

    # protocole that does not exist
    response = client.get("/protokol/100?protocol_id=100")
    assert response.status_code == 404


def test_api_post_appeal():
    # appeal that exists
    response = client.post("/odwolanie/create/1/?user_id=1&protocol_id=1",
                           json={
                               "text": "string",
                               "date": "2022-02-02"
                           })
    assert response.status_code == 409

    # protocol that does not exists
    response = client.post("/odwolanie/create/1/?user_id=1&protocol_id=100",
                           json={
                               "text": "string",
                               "date": "2022-02-02"
                           })
    assert response.status_code == 404

    # protocol that is approved
    response = client.post("/odwolanie/create/1/?user_id=4&protocol_id=2",
                           json={
                               "text": "string",
                               "date": "2022-02-02"
                           })
    assert response.status_code == 409

    # appeal can be posted
    response = client.post("/odwolanie/create/1/?user_id=5&protocol_id=3",
                           json={
                               "text": "string",
                               "date": "2022-04-03"
                           })
    assert response.status_code == 200


def test_api_get_protocols_comission_head():
    # user that has protocols
    response = client.get("/protokoly/przewodniczacy/1?user_id=1")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # user without protocols
    response = client.get("/protokoly/przewodniczacy/100?user_id=100")
    assert response.status_code == 404


def test_api_get_course_protocol():
    # user that has protocols
    response = client.get("/kurs/1?protocol_id=1")
    assert response.status_code == 200

    # user without protocols
    response = client.get("/kurs/100?protocol_id=100")
    assert response.status_code == 404


def test_api_put_protocol():
    # protocol that does not exist
    response = client.put("/protokol/update/200?protocol_id=200",
                          json={
                              "date": "2022-03-05",
                              "is_approved": True,
                              "mark": "string",
                              "justification": "string",
                              "conclusions_and_recommendations": "string",
                              "read_date": "2022-03-05",
                              "is_sent": True,
                              "presentation_mark_fk": 0,
                              "explanation_mark_fk": 0,
                              "realization_mark_fk": 0,
                              "inspiration_mark_fk": 0,
                              "participation_mark_fk": 0,
                              "use_of_learning_methods_mark_fk": 0,
                              "use_of_tools_mark_fk": 0,
                              "control_mark_fk": 0,
                              "creation_mark_fk": 0
                          })
    assert response.status_code == 404

    # protocol that is acceppted
    response = client.put("/protokol/update/2?protocol_id=2",
                          json={
                              "date": "2022-03-05",
                              "is_approved": True,
                              "mark": "string",
                              "justification": "string",
                              "conclusions_and_recommendations": "string",
                              "read_date": "2022-03-05",
                              "is_sent": True,
                              "presentation_mark_fk": 0,
                              "explanation_mark_fk": 0,
                              "realization_mark_fk": 0,
                              "inspiration_mark_fk": 0,
                              "participation_mark_fk": 0,
                              "use_of_learning_methods_mark_fk": 0,
                              "use_of_tools_mark_fk": 0,
                              "control_mark_fk": 0,
                              "creation_mark_fk": 0
                          })
    assert response.status_code == 409

    # protocol that can be updated
    response = client.put("/protokol/update/3?protocol_id=3",
                          json={
                              "date": "2022-03-05",
                              "is_approved": True,
                              "mark": "string",
                              "justification": "string",
                              "conclusions_and_recommendations": "string",
                              "read_date": "2022-03-05",
                              "is_sent": True,
                              "presentation_mark_fk": 0,
                              "explanation_mark_fk": 0,
                              "realization_mark_fk": 0,
                              "inspiration_mark_fk": 0,
                              "participation_mark_fk": 0,
                              "use_of_learning_methods_mark_fk": 0,
                              "use_of_tools_mark_fk": 0,
                              "control_mark_fk": 0,
                              "creation_mark_fk": 0
                          })
    assert response.status_code == 200


def test_api_get_does_appeal_exists():
    # appeal that exists
    response = client.get("/odwolanie/1?protocol_id=1")
    assert response.status_code == 200
    assert response.json() == True

    # appeal that does not exist
    response = client.get("/odwolanie/100?protocol_id=100")
    assert response.status_code == 200
    assert response.json() == False


def test_api_get_audits_to_do():
    # user with audits
    response = client.get("/hospitacje/1?user_id=1")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # user without audits
    response = client.get("/hospitacje/100?user_id=100")
    assert response.status_code == 404


def test_api_get_audit_details():
    # audit that does not exist
    response = client.get("/hospitacja/detal/100?audit_id=100")
    assert response.status_code == 404

    # audit that does exists
    response = client.get("/hospitacja/detal/1?audit_id=1")
    assert response.status_code == 200


def test_api_put_accept_protocol():
    # protocol that does not exist
    response = client.put("/protokol/set_true/100?protocol_id=100")
    assert response.status_code == 404

    # protocol that does exists
    response = client.put("/protokol/set_true/1?protocol_id=1")
    assert response.status_code == 200


def test_api_delete_appeal():
    response = client.delete("/odwolanie/delete/1?protocol_id=1&user_id=1")
    assert response.status_code == 200
    assert response.json() == True

    response = client.delete(
        "/odwolanie/delete/900?protocol_id=900&user_id=200")
    assert response.status_code == 200
    assert response.json() == False


def test_api_put_unaccept_protocol():
    # protocol that does not exist
    response = client.put("/protokol/set_false/100?protocol_id=100")
    assert response.status_code == 404

    # protocol that does exists
    response = client.put("/protokol/set_false/1?protocol_id=1")
    assert response.status_code == 200
