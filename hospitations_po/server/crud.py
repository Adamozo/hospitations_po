from decimal import Decimal
from ntpath import join
from pyexpat import model
from sqlite3 import Date
from sqlalchemy.orm import Session, Query
from sqlalchemy import and_, false, true
import models, schemas
from typing import Any, Optional, Union
from datetime import datetime


def get_protokoly_prowadzacy(
        user_id: int,
        db: Session,
        skip: int = 0,
        limit: int = 100) -> list[dict[str, Union[str, int, float]]]:
    res: list[tuple[str, bool, int, str, str, float]] = db.query(models.Hospitacja.data_hospitacji, models.Protokol.czy_zatwierdzona, models.Protokol.id, models.Protokol.ocena, models.Kurs.kod, models.Kurs.nazwa)\
        .join(models.Protokol, models.Hospitacja.protokol_fk == models.Protokol.id)\
            .join(models.Kurs, models.Kurs.id == models.Hospitacja.kurs_fk)\
                .filter(models.Hospitacja.uzytkownik_fk == user_id).all()

    return [{
        "date": r[0],
        "czy_zatwierdzony": r[1],
        "id": r[2],
        "nr_kursu": r[4],
        "nazwa_kursu": r[5],
        "ocena": r[3]
    } for r in res]


def get_protokol(protokol_id: int, db: Session) -> Optional[dict[str, Any]]:
    protokol: Optional[models.Protokol] = db.query(
        models.Protokol).filter(models.Protokol.id == protokol_id).first()
    if protokol is None:
        return None

    return {
        "date": protokol.data_protokol,
        "czy_zatwierdzony": protokol.czy_zatwierdzona,
        "ocena": protokol.ocena,
        "uzasadnienie": protokol.uzasadnienie,
        "wnioski_i_zalecenia": protokol.wnioski_i_zalecenia,
        "data_zapoznania": protokol.data_zapoznania,
        "czy_przeslany": protokol.czy_przeslany,
        "przedstawienie_ocena_fk": protokol.przedstawienie_ocena_fk,
        "wyjasnienie_ocena_fk": protokol.wyjasnienie_ocena_fk,
        "realizacja_ocena_fk": protokol.realizacja_ocena_fk,
        "inspiracja_ocena_fk": protokol.inspiracja_ocena_fk,
        "udzielenie_ocena_fk": protokol.udzielenie_ocena_fk,
        "stosowanie_ocena_fk": protokol.stosowanie_ocena_fk,
        "poslugiwanie_ocena_fk": protokol.poslugiwanie_ocena_fk,
        "panowanie_ocena_fk": protokol.panowanie_ocena_fk,
        "tworzenie_ocena_fk": protokol.tworzenie_ocena_fk
    }


def get_odwolanie(protokol_id: int, db: Session) -> Optional[models.Odwolanie]:
    return db.query(models.Odwolanie).filter(
        models.Odwolanie.protokol_fk == protokol_id).first()


def insert_odwolanie(odwolanie: schemas.OdwolanieCreate, user_id: int,
                     protokol_id: int, db: Session) -> models.Odwolanie:
    new_odwolanie: models.Odwolanie = models.Odwolanie(
        tekst=odwolanie.tekst,
        uzytkownik_fk=user_id,
        protokol_fk=protokol_id,
        data_odwolanie=odwolanie.data_odwolanie)
    db.add(new_odwolanie)
    db.commit()
    db.refresh(new_odwolanie)
    return new_odwolanie


def get_kurs_protokol(
        protokol_id: int,
        db: Session) -> Optional[dict[str, Union[str, int, None]]]:
    hospitacja_kurs: Optional[tuple[int]] = db.query(
        models.Hospitacja.kurs_fk).filter(
            models.Hospitacja.protokol_fk == protokol_id).first()
    if hospitacja_kurs is not None:
        kurs: Optional[models.Kurs] = db.query(
            models.Kurs).filter(models.Kurs.id == hospitacja_kurs[0]).first()
        res: dict[str, Union[int, str, None]] = {
            "id": kurs.id,
            "uzytkownik_fk": kurs.uzytkownik_fk,
            "nazwa": kurs.nazwa,
            "kod": kurs.kod,
            "stopien_i_froma_studiow": kurs.stopien_i_froma_studiow,
            "forma_dydaktyczna": kurs.forma_dydaktyczna,
            "termin": kurs.termin,
            "liczba_uczestnikow": kurs.liczba_uczestnikow,
            "miejsce": kurs.miejsce,
            "jednostka_organizacyjna": kurs.jednostka_organizacyjna,
            "semestr": kurs.semestr
        }
        return res

    return None


def get_protokoly_przewodniczacy(
        user_id: int,
        db: Session,
        skip: int = 0,
        limit: int = 100) -> list[dict[str, Union[int, bool, None, str]]]:
    res: Optional[list[tuple[str, bool, int, str, str, str, str, bool]]] = db.query(models.Hospitacja.data_hospitacji, models.Protokol.czy_zatwierdzona, models.Protokol.id, models.Kurs.kod, models.Kurs.nazwa, models.Uzytkownik.imie, models.Uzytkownik.nazwisko, models.Protokol.czy_przeslany)\
        .join(models.Protokol, models.Hospitacja.protokol_fk == models.Protokol.id)\
            .join(models.Kurs, models.Hospitacja.kurs_fk == models.Kurs.id)\
                .join(models.Uzytkownik, models.Hospitacja.uzytkownik_fk == models.Uzytkownik.id)\
                    .join(models.Komisja_hospitacyjna, models.Hospitacja.komisja_hospitacyjna_fk == models.Komisja_hospitacyjna.id)\
                        .filter(models.Komisja_hospitacyjna.uzytkownik_fk == user_id).all()

    return [{
        "date": r[0],
        "czy_zatwierdzony": r[1],
        "id": r[2],
        "nr_kursu": r[3],
        "nazwa_kursu": r[4],
        "hospitowany_imie": r[5],
        "hospitowany_nazwisko": r[6],
        "czy_przeslany": r[7]
    } for r in res]


def update_protocol(
        protocol: schemas.Protokol, protokol_id: int, db: Session
) -> Optional[dict[str, Union[int, str, Decimal, Date, None]]]:
    prot: Optional[models.Protokol] = db.query(
        models.Protokol).filter(models.Protokol.id == protokol_id).first()
    if prot is None:
        return None

    db.query(
        models.Protokol).filter(models.Protokol.id == protokol_id).update({
            models.Protokol.uzasadnienie:
            protocol.uzasadnienie,
            models.Protokol.ocena:
            protocol.ocena,
            models.Protokol.wnioski_i_zalecenia:
            protocol.wnioski_i_zalecenia,
            models.Protokol.data_zapoznania:
            protocol.data_zapoznania,
            models.Protokol.czy_zatwierdzona:
            protocol.czy_zatwierdzony,
            models.Protokol.czy_przeslany:
            protocol.czy_przeslany,
            models.Protokol.przedstawienie_ocena_fk:
            protocol.przedstawienie_ocena_fk,
            models.Protokol.wyjasnienie_ocena_fk:
            protocol.wyjasnienie_ocena_fk,
            models.Protokol.realizacja_ocena_fk:
            protocol.realizacja_ocena_fk,
            models.Protokol.inspiracja_ocena_fk:
            protocol.inspiracja_ocena_fk,
            models.Protokol.udzielenie_ocena_fk:
            protocol.udzielenie_ocena_fk,
            models.Protokol.stosowanie_ocena_fk:
            protocol.stosowanie_ocena_fk,
            models.Protokol.poslugiwanie_ocena_fk:
            protocol.poslugiwanie_ocena_fk,
            models.Protokol.panowanie_ocena_fk:
            protocol.panowanie_ocena_fk,
            models.Protokol.tworzenie_ocena_fk:
            protocol.tworzenie_ocena_fk
        })
    db.commit()

    prot = db.query(
        models.Protokol).filter(models.Protokol.id == protokol_id).first()

    return {
        "date": prot.data_protokol,
        "czy_zatwierdzony": prot.czy_zatwierdzona,
        "ocena": prot.ocena,
        "uzasadnienie": prot.uzasadnienie,
        "wnioski_i_zalecenia": prot.wnioski_i_zalecenia,
        "data_zapoznania": prot.data_zapoznania,
        "czy_przeslany": prot.czy_przeslany,
        "przedstawienie_ocena_fk": prot.przedstawienie_ocena_fk,
        "wyjasnienie_ocena_fk": prot.wyjasnienie_ocena_fk,
        "realizacja_ocena_fk": prot.realizacja_ocena_fk,
        "inspiracja_ocena_fk": prot.inspiracja_ocena_fk,
        "udzielenie_ocena_fk": prot.udzielenie_ocena_fk,
        "stosowanie_ocena_fk": prot.stosowanie_ocena_fk,
        "poslugiwanie_ocena_fk": prot.poslugiwanie_ocena_fk,
        "panowanie_ocena_fk": prot.panowanie_ocena_fk,
        "tworzenie_ocena_fk": prot.tworzenie_ocena_fk
    }


def get_protokol_odwolanie(protokol_id: int, db: Session) -> bool:
    odwolanie: Optional[tuple[int]] = db.query(models.Odwolanie.id).filter(
        models.Odwolanie.protokol_fk == protokol_id).first()

    return odwolanie is not None


def get_terminarz_hospitacji(
    user_id: int, db: Session
) -> Optional[list[dict[str, Union[Date, str, bool, int, None]]]]:
    temp: Query[tuple[int]] = db.query(models.Komisja_hospitacyjna.id).filter(
        models.Komisja_hospitacyjna.uzytkownik_fk == user_id)
    komisje: Optional[list[int]] = [id[0] for id in temp]
    temp = db.query(models.Hospitacja.id).filter(
        models.Hospitacja.komisja_hospitacyjna_fk.in_(komisje))
    hospitacje: Optional[list[int]] = [id[0] for id in temp]
    temp = db.query(models.Hospitacja.kurs_fk).filter(
        models.Hospitacja.id.in_(hospitacje))
    kursy: Optional[list[int]] = [kurs[0] for kurs in temp]
    res: Optional[list[tuple[Date, int, str, str, str, str]]] = db.query(models.Hospitacja.data_hospitacji, models.Hospitacja.id, models.Kurs.kod, models.Kurs.nazwa, models.Uzytkownik.imie,
     models.Uzytkownik.nazwisko).join(models.Kurs, models.Kurs.id == models.Hospitacja.kurs_fk)\
     .join(models.Uzytkownik, models.Uzytkownik.id == models.Hospitacja.uzytkownik_fk)\
     .filter(and_(models.Kurs.id.in_(kursy), models.Hospitacja.id.in_(hospitacje))).all()

    return [{
        "date": r[0],
        "czy_zatwierdzony": True,
        "id": r[1],
        "nr_kursu": r[2],
        "nazwa_kursu": r[3],
        "hospitowany_imie": r[4],
        "hospitowany_nazwisko": r[5],
        "czy_przeslany": True
    } for r in res]


def get_detalerz_hospitacji(
        hospitacja_id: int,
        db: Session) -> Optional[dict[str, Union[Date, str, int, None]]]:
    temp: Optional[tuple[int]] = db.query(models.Hospitacja.kurs_fk).filter(
        models.Hospitacja.id == (hospitacja_id)).first()
    if temp is None:
        return None

    kurs: int = temp[0]

    temp = db.query(models.Uzytkownik.id).filter(
        and_(models.Kurs.id == kurs,
             models.Uzytkownik.id == models.Kurs.uzytkownik_fk)).first()
    uzytkownik: int = temp[0]

    r: Optional[tuple[Date, int, str, str, str, str, str, str, str, str, int,
                      str, str]] = db.query(
                          models.Hospitacja.data_hospitacji,
                          models.Hospitacja.id, models.Kurs.kod,
                          models.Kurs.nazwa, models.Uzytkownik.imie,
                          models.Uzytkownik.nazwisko,
                          models.Kurs.stopien_i_froma_studiow,
                          models.Kurs.forma_dydaktyczna, models.Kurs.termin,
                          models.Kurs.liczba_uczestnikow, models.Kurs.miejsce,
                          models.Kurs.jednostka_organizacyjna).filter(
                              and_(
                                  models.Kurs.id == kurs,
                                  models.Hospitacja.id == hospitacja_id,
                                  models.Uzytkownik.id == uzytkownik)).first()

    return {
        "date": r[0],
        "czy_zatwierdzony": True,
        "id": r[1],
        "nr_kursu": r[2],
        "nazwa_kursu": r[3],
        "hospitowany_imie": r[4],
        "hospitowany_nazwisko": r[5],
        "czy_przeslany": True,
        "stopien_i_froma_studiow": r[6],
        "forma_dydaktyczna": r[7],
        "termin": r[8],
        "liczba_uczestnikow": r[9],
        "miejsce": r[10],
        "jednostka_organizacyjna": r[11]
    }


def put_zatwierdz_protokol(protokol_id: int, db: Session) -> bool:
    prot: Optional[models.Protokol] = db.query(
        models.Protokol).filter(models.Protokol.id == protokol_id).first()
    if prot is None:
        return False

    db.query(models.Protokol).filter(models.Protokol.id == protokol_id).update(
        {models.Protokol.czy_zatwierdzona: True})
    db.commit()

    prot = db.query(models.Protokol).filter(
        and_(models.Protokol.id == protokol_id,
             models.Protokol.czy_zatwierdzona == True)).first()
    if prot is None:
        return False

    return True


def delete_odwolanie(protocol_id: int, user_id: int, db: Session) -> bool:
    odwolanie: Optional[models.Odwolanie] = db.query(models.Odwolanie).filter(
        and_(models.Odwolanie.protokol_fk == protocol_id,
             models.Odwolanie.uzytkownik_fk == user_id)).first()
    db.delete(odwolanie)
    db.commit()
    odwolanie = db.query(models.Odwolanie).filter(
        and_(models.Odwolanie.protokol_fk == protocol_id,
             models.Odwolanie.uzytkownik_fk == user_id)).first()
    if odwolanie is None:
        return True
    return False


def put_odtwierdz_protokol(protokol_id: int, db: Session) -> bool:
    prot: Optional[models.Protokol] = db.query(
        models.Protokol).filter(models.Protokol.id == protokol_id).first()
    if prot is None:
        return False

    db.query(models.Protokol).filter(models.Protokol.id == protokol_id).update(
        {models.Protokol.czy_zatwierdzona: False})
    db.commit()

    prot = db.query(models.Protokol).filter(
        and_(models.Protokol.id == protokol_id,
             models.Protokol.czy_zatwierdzona == False)).first()
    if prot is None:
        return False

    return True
