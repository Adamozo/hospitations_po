from http.client import HTTPResponse
from decimal import Decimal
from tkinter.font import BOLD
from typing import List
from unicodedata import name
from unittest import result
from xmlrpc.client import Boolean
from typing import Any, Optional, Union
from sqlite3 import Date
import uvicorn    # type: ignore

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import null
from sqlalchemy.orm import Session
from datetime import datetime

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI(title="Twoje hospitacje")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/protokoly/prowadzacy/{prowadzacy}",
         response_model=List[schemas.ProtocolShort])
def get_protocols_tutor(
    tutor_id: int,
    db: Session = Depends(get_db)
) -> Optional[list[dict[str, Union[str, int, float]]]]:
    try:
        protocols: list[dict[str,
                             Union[str, int,
                                   float]]] = crud.get_protocols_tutor(tutor_id, db)
        if len(protocols) == 0:
            raise HTTPException(status_code=404, detail="Protocols not found")
        return protocols

    except HTTPException as e:
        raise e

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


@app.get("/protokol/{protokol_id}", response_model=schemas.Protocol)
def get_protocol_info(
    protocol_id: int,
    db: Session = Depends(get_db)) -> Optional[dict[str, Any]]:
    try:
        protocol: Optional[dict[str, Any]] = crud.get_protocol(protocol_id, db)
        if protocol is None:
            raise HTTPException(status_code=404, detail="Protocol not found")
        return protocol

    except HTTPException as e:
        raise e

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


@app.post("/odwolanie/create/{protokol_id}/", response_model=schemas.Appeal)
def post_appeal(
    appeal: schemas.AppealCreate,
    user_id: int,
    protocol_id: int,
    db: Session = Depends(get_db)) -> models.Appeal:
    try:
        protocol: Optional[dict[str, Any]] = crud.get_protocol(protocol_id, db)
        if protocol is None:
            raise HTTPException(status_code=404, detail="Protocol not found")
        else:
            if protocol["czy_zatwierdzony"]:
                raise HTTPException(status_code=409,
                                    detail="Protocol already approved")

            temp = crud.get_appeal(protocol_id, db)
            if temp is not None:
                raise HTTPException(status_code=409,
                                    detail="Error during odwolanie creation")

            return crud.insert_appeal(appeal, user_id, protocol_id, db)

    except HTTPException as e:
        raise e

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


@app.get("/protokoly/przewodniczacy/{przewodniczacy}",
         response_model=List[schemas.ProtocolEdit])
def get_protocols_comission_head(
    user_id: int,
    db: Session = Depends(get_db)
) -> list[dict[str, Union[int, bool, None, str]]]:
    try:
        protocols: list[dict[str,
                             Union[int, bool, None,
                                   str]]] = crud.get_protocols_comission_head(user_id, db)
        if len(protocols) == 0:
            raise HTTPException(status_code=404, detail="Protocols not found")
        return protocols

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/kurs/{protokol}", response_model=schemas.Course)
def get_course_protocol(
    protocol_id: int, db: Session = Depends(get_db)
) -> Optional[dict[str, Union[str, int, None]]]:
    try:
        course: Optional[dict[str, Union[str, int,
                                       None]]] = crud.get_course_protocol(
                                           protocol_id, db)
        if course is None:
            raise HTTPException(status_code=404, detail="Kurs not found")
        return course

    except HTTPException as e:
        raise e

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


@app.put("/protokol/update/{protokol_id}", response_model=schemas.Protocol)
def put_protocol(
    protocol: schemas.Protocol,
    protocol_id: int,
    db: Session = Depends(get_db)
) -> Optional[dict[str, Union[int, str, Decimal, Date, None]]]:
    try:
        prot: Optional[dict[str, Any]] = crud.get_protocol(protocol_id, db)
        if prot is None:
            raise HTTPException(status_code=404, detail="Protocol not found")

        elif prot["is_accepted"]:
            raise HTTPException(status_code=409, detail="Unable to update")

        else:
            res: Optional[dict[str, Union[int, str, Decimal, Date,
                                          None]]] = crud.update_protocol(
                                              protocol, protocol_id, db)
            if res is None:
                raise HTTPException(status_code=409, detail="Unable to update")

            return res

    except HTTPException as e:
        raise e

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Inner server error")


@app.get("/odwolanie/{protokol}", response_model=Boolean)
def get_does_appeal_exists(
    protocol_id: int, db: Session = Depends(get_db)) -> bool:
    try:
        return crud.get_protocol_appeal(protokol_id=protocol_id, db=db)

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


@app.get("/hospitacje/{user}", response_model=List[schemas.ProtocolEdit])
def get_audits_to_do(
    user_id, db: Session = Depends(get_db)
) -> Optional[list[dict[str, Union[Date, str, bool, int, None]]]]:
    try:
        audits: Optional[list[dict[
            str, Union[Date, str, bool, int,
                       None]]]] = crud.get_audits_schedule(user_id, db)
        if len(audits) == 0:
            raise HTTPException(status_code=404, detail="Protocols not found")
        return audits

    except HTTPException as e:
        raise e

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


@app.get("/hospitacja/detal/{hospitacja_id}",
         response_model=schemas.ProtocolDetails)
def get_audit_details(
    audit_id, db: Session = Depends(get_db)
) -> Optional[dict[str, Union[Date, str, int, None]]]:
    try:
        audit: Optional[dict[str,
                                  Union[Date, str, int,
                                        None]]] = crud.get_audits_details(
                                            audit_id, db)
        if audit is None:
            raise HTTPException(status_code=404, detail="Audit not found")
        return audit

    except HTTPException as e:
        raise e

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


@app.put("/protokol/set_true/{protokol_id}", response_model=Boolean)
def put_accept_protocol(protocol_id: int, db: Session = Depends(get_db)) -> bool:
    try:
        is_success: bool = crud.put_confirm_protocol(protocol_id, db)
        if is_success:
            return True
        raise HTTPException(status_code=404, detail="Protocols not found")

    except HTTPException as e:
        raise e

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


@app.delete('/odwolanie/delete/{protokol_id}', response_model=Boolean)
def delete_appeal(protocol_id: int,
                     user_id: int,
                     db: Session = Depends(get_db)) -> bool:
    try:
        result = crud.delete_appeal(protocol_id, user_id, db=db)
        return result

    except HTTPException as e:
        raise e

    except:
        return False


@app.put("/protokol/set_false/{protokol_id}", response_model=Boolean)
def put_unaccept_protocol(
    protocol_id: int, db: Session = Depends(get_db)) -> Optional[bool]:
    try:
        is_success: bool = crud.put_unconfirm_protocol(protocol_id, db)
        if is_success:
            return True
        raise HTTPException(status_code=404, detail="Protocols not found")

    except HTTPException as e:
        raise e

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


if __name__ == '__main__':
    uvicorn.run("main:app")
