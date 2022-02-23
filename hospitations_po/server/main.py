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


# sql
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/protokoly/prowadzacy/{prowadzacy}",
         response_model=List[schemas.ProtokolShort])
def get_protokoly(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> Optional[list[dict[str, Union[str, int, float]]]]:
    try:
        protokoly: list[dict[str,
                             Union[str, int,
                                   float]]] = crud.get_protokoly_prowadzacy(
                                       user_id, db, skip=skip, limit=limit)
        if len(protokoly) == 0:
            raise HTTPException(status_code=404, detail="Protocols not found")
        return protokoly

    except HTTPException as e:
        raise e

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


@app.get("/protokol/{protokol_id}", response_model=schemas.Protokol)
def get_protokol(
    protokol_id: int,
    db: Session = Depends(get_db)) -> Optional[dict[str, Any]]:
    try:
        protokol: Optional[dict[str, Any]] = crud.get_protokol(protokol_id, db)
        if protokol is None:
            raise HTTPException(status_code=404, detail="Protocol not found")
        return protokol

    except HTTPException as e:
        raise e

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


@app.post("/odwolanie/create/{protokol_id}/", response_model=schemas.Odwolanie)
def create_odwolanie(
    odwolanie: schemas.OdwolanieCreate,
    user_id: int,
    protokol_id: int,
    db: Session = Depends(get_db)) -> models.Odwolanie:
    try:
        protokol: Optional[dict[str, Any]] = crud.get_protokol(protokol_id, db)
        if protokol is None:
            raise HTTPException(status_code=404, detail="Protocol not found")
        else:
            if protokol["czy_zatwierdzony"]:
                raise HTTPException(status_code=409,
                                    detail="Protocol already approved")

            temp = crud.get_odwolanie(protokol_id, db)
            if temp is not None:
                raise HTTPException(status_code=409,
                                    detail="Error during odwolanie creation")

            return crud.insert_odwolanie(odwolanie, user_id, protokol_id, db)

    except HTTPException as e:
        raise e

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


@app.get("/protokoly/przewodniczacy/{przewodniczacy}",
         response_model=List[schemas.ProtokolEdit])
def get_protokoly_przewodniczacy(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> list[dict[str, Union[int, bool, None, str]]]:
    try:
        protokoly: list[dict[str,
                             Union[int, bool, None,
                                   str]]] = crud.get_protokoly_przewodniczacy(
                                       user_id, db, skip=skip, limit=limit)
        if len(protokoly) == 0:
            raise HTTPException(status_code=404, detail="Protocols not found")
        return protokoly

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/kurs/{protokol}", response_model=schemas.Kurs)
def get_kurs_protokol(
    protokol_id: int, db: Session = Depends(get_db)
) -> Optional[dict[str, Union[str, int, None]]]:
    try:
        kurs: Optional[dict[str, Union[str, int,
                                       None]]] = crud.get_kurs_protokol(
                                           protokol_id, db)
        if kurs is None:
            raise HTTPException(status_code=404, detail="Kurs not found")
        return kurs

    except HTTPException as e:
        raise e

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


@app.put("/protokol/update/{protokol_id}", response_model=schemas.Protokol)
def update_protokol(
    protokol: schemas.Protokol,
    protokol_id: int,
    db: Session = Depends(get_db)
) -> Optional[dict[str, Union[int, str, Decimal, Date, None]]]:
    try:
        prot: Optional[dict[str, Any]] = crud.get_protokol(protokol_id, db)
        if prot is None:
            raise HTTPException(status_code=404, detail="Protocol not found")

        elif prot["czy_zatwierdzony"]:
            raise HTTPException(status_code=409, detail="Unable to update")

        else:
            res: Optional[dict[str, Union[int, str, Decimal, Date,
                                          None]]] = crud.update_protocol(
                                              protokol, protokol_id, db)
            if res is None:
                raise HTTPException(status_code=409, detail="Unable to update")

            return res

    except HTTPException as e:
        raise e

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Inner server error")


@app.get("/odwolanie/{protokol}", response_model=Boolean)
def get_czy_odwolanie_istnieje(
    protokol_id: int, db: Session = Depends(get_db)) -> bool:
    try:
        return crud.get_protokol_odwolanie(protokol_id=protokol_id, db=db)

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


@app.get("/hospitacje/{user}", response_model=List[schemas.ProtokolEdit])
def get_hospitacje_do_zhospitowania(
    user_id, db: Session = Depends(get_db)
) -> Optional[list[dict[str, Union[Date, str, bool, int, None]]]]:
    try:
        hospitacyjki: Optional[list[dict[
            str, Union[Date, str, bool, int,
                       None]]]] = crud.get_terminarz_hospitacji(user_id, db)
        if len(hospitacyjki) == 0:
            raise HTTPException(status_code=404, detail="Protocols not found")
        return hospitacyjki

    except HTTPException as e:
        raise e

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


@app.get("/hospitacja/detal/{hospitacja_id}",
         response_model=schemas.ProtokolDetails)
def get_hospitacja_detale(
    hospitacja_id, db: Session = Depends(get_db)
) -> Optional[dict[str, Union[Date, str, int, None]]]:
    try:
        hospitacja: Optional[dict[str,
                                  Union[Date, str, int,
                                        None]]] = crud.get_detalerz_hospitacji(
                                            hospitacja_id, db)
        if hospitacja is None:
            raise HTTPException(status_code=404, detail="Hospitacja not found")
        return hospitacja

    except HTTPException as e:
        raise e

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


@app.put("/protokol/set_true/{protokol_id}", response_model=Boolean)
def accept_protokol(protokol_id: int, db: Session = Depends(get_db)) -> bool:
    try:
        is_success: bool = crud.put_zatwierdz_protokol(protokol_id, db)
        if is_success:
            return True
        raise HTTPException(status_code=404, detail="Protocols not found")

    except HTTPException as e:
        raise e

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


@app.delete('/odwolanie/delete/{protokol_id}', response_model=Boolean)
def delete_odowlanie(protokol_id: int,
                     user_id: int,
                     db: Session = Depends(get_db)) -> bool:
    try:
        result = crud.delete_odwolanie(protokol_id, user_id, db=db)
        return result

    except HTTPException as e:
        raise e

    except:
        return False


@app.put("/protokol/set_false/{protokol_id}", response_model=Boolean)
def unaccept_protokol(
    protokol_id: int, db: Session = Depends(get_db)) -> Optional[bool]:
    try:
        is_success: bool = crud.put_odtwierdz_protokol(protokol_id, db)
        if is_success:
            return True
        raise HTTPException(status_code=404, detail="Protocols not found")

    except HTTPException as e:
        raise e

    except:
        raise HTTPException(status_code=500, detail="Inner server error")


if __name__ == '__main__':
    uvicorn.run("main:app")
