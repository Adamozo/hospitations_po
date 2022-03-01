from decimal import Decimal
from ntpath import join
from pyexpat import model
from sqlite3 import Date
from sqlalchemy.orm import Session, Query
from sqlalchemy import and_, false, true
import models, schemas
from typing import Any, Optional, Union
from datetime import datetime


def get_protocols_tutor(
        user_id: int,
        db: Session) -> list[dict[str, Union[str, int, float]]]:
    res: list[tuple[str, bool, int, str, str, float]] = db.query(models.Audit.date, models.Protocol.is_approved, models.Protocol.id,\
         models.Protocol.mark, models.Course.code, models.Course.name)\
        .join(models.Protocol, models.Audit.protocol_fk == models.Protocol.id)\
            .join(models.Course, models.Course.id == models.Audit.course_fk)\
                .filter(models.Audit.user_fk == user_id).all()

    return [{
        "date": r[0],
        "czy_zatwierdzony": r[1],
        "id": r[2],
        "nr_kursu": r[4],
        "nazwa_kursu": r[5],
        "mark": r[3]
    } for r in res]


def get_protocol(protocol_id: int, db: Session) -> Optional[dict[str, Any]]:
    protocol: Optional[models.Protocol] = db.query(
        models.Protocol).filter(models.Protocol.id == protocol_id).first()
    if protocol is None:
        return None

    return {
        "date": protocol.date,
        "czy_zatwierdzony": protocol.is_approved,
        "mark": protocol.mark,
        "uzasadnienie": protocol.justification,
        "wnioski_i_zalecenia": protocol.conclusions_and_recommendations,
        "data_zapoznania": protocol.read_date,
        "czy_przeslany": protocol.is_sent,
        "przedstawienie_mark_fk": protocol.presentation_mark_fk,
        "wyjasnienie_mark_fk": protocol.explanation_mark_fk,
        "realizacja_mark_fk": protocol.realization_mark_fk,
        "inspiracja_mark_fk": protocol.inspiration_mark_fk,
        "udzielenie_mark_fk": protocol.participation_mark_fk,
        "stosowanie_mark_fk": protocol.use_of_learning_methods_mark_fk,
        "poslugiwanie_mark_fk": protocol.use_of_tools_mark_fk,
        "panowanie_mark_fk": protocol.control_mark_fk,
        "tworzenie_mark_fk": protocol.creation_mark_fk
    }


def get_appeal(protocol_id: int, db: Session) -> Optional[models.Appeal]:
    return db.query(models.Appeal).filter(
        models.Appeal.protocol_fk == protocol_id).first()


def insert_appeal(appeal: schemas.AppealCreate, user_id: int,
                     protocol_id: int, db: Session) -> models.Appeal:
    new_appeal: models.Appeal = models.Appeal(text=appeal.text, user_fk=user_id, protocol_fk=protocol_id, date=appeal.date)
    db.add(new_appeal)
    db.commit()
    db.refresh(new_appeal)
    return new_appeal


def get_course_protocol(
        protocol_id: int,
        db: Session) -> Optional[dict[str, Union[str, int, None]]]:
    audit_course: Optional[tuple[int]] = db.query(
        models.Audit.course_fk).filter(
            models.Audit.protocol_fk == protocol_id).first()
    if audit_course is not None:
        course: Optional[models.Course] = db.query(
            models.Course).filter(models.Course.id == audit_course[0]).first()
        res: dict[str, Union[int, str, None]] = {
            "id": course.id,
            "user_fk": course.user_fk,
            "nazwa": course.name,
            "kod": course.code,
            "stopien_i_froma_studiow": course.level_and_form_of_study,
            "forma_dydaktyczna": course.didactic_form,
            "termin": course.date,
            "liczba_uczestnikow": course.participants_number,
            "miejsce": course.place,
            "jednostka_organizacyjna": course.organizational_entity,
            "semestr": course.term
        }
        return res

    return None


def get_protocols_comission_head(
        user_id: int,
        db: Session) -> list[dict[str, Union[int, bool, None, str]]]:
    res: Optional[list[tuple[str, bool, int, str, str, str, str, bool]]] = \
        db.query(models.Audit.date, models.Protocol.is_approved, models.Protocol.id, models.Course.code, models.Course.name, models.User.name\
            , models.User.surname, models.Protocol.is_sent)\
        .join(models.Protocol, models.Audit.protocol_fk == models.Protocol.id)\
            .join(models.Course, models.Audit.course_fk == models.Course.id)\
                .join(models.User, models.Audit.user_fk == models.User.id)\
                    .join(models.Audit_commission, models.Audit.audit_commission_fk == models.Audit_commission.id)\
                        .filter(models.Audit_commission.user_fk == user_id).all()

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
        protocol: schemas.Protocol, protocol_id: int, db: Session
) -> Optional[dict[str, Union[int, str, Decimal, Date, None]]]:
    prot: Optional[models.Protocol] = db.query(
        models.Protocol).filter(models.Protocol.id == protocol_id).first()
    if prot is None:
        return None

    db.query(
        models.Protocol).filter(models.Protocol.id == protocol_id).update({
            models.Protocol.justification:
            protocol.justification,
            models.Protocol.mark:
            protocol.mark,
            models.Protocol.conclusions_and_recommendations:
            protocol.conclusions_and_recommendations,
            models.Protocol.read_date:
            protocol.read_date,
            models.Protocol.is_approved:
            protocol.is_approved,
            models.Protocol.is_sent:
            protocol.is_sent,
            models.Protocol.presentation_mark_fk:
            protocol.presentation_mark_fk,
            models.Protocol.explanation_mark_fk:
            protocol.explanation_mark_fk,
            models.Protocol.realization_mark_fk:
            protocol.realization_mark_fk,
            models.Protocol.inspiration_mark_fk:
            protocol.inspiration_mark_fk,
            models.Protocol.participation_mark_fk:
            protocol.participation_mark_fk,
            models.Protocol.use_of_learning_methods_mark_fk:
            protocol.use_of_learning_methods_mark_fk,
            models.Protocol.use_of_tools_mark_fk:
            protocol.use_of_tools_mark_fk,
            models.Protocol.control_mark_fk:
            protocol.control_mark_fk,
            models.Protocol.creation_mark_fk:
            protocol.creation_mark_fk
        })
    db.commit()

    prot = db.query(
        models.Protocol).filter(models.Protocol.id == protocol_id).first()

    return {
        "date": prot.date,
        "czy_zatwierdzony": prot.is_approved,
        "mark": prot.mark,
        "uzasadnienie": prot.justification,
        "wnioski_i_zalecenia": prot.conclusions_and_recommendations,
        "data_zapoznania": prot.read_date,
        "czy_przeslany": prot.is_sent,
        "przedstawienie_mark_fk": prot.presentation_mark_fk,
        "wyjasnienie_mark_fk": prot.explanation_mark_fk,
        "realizacja_mark_fk": prot.realization_mark_fk,
        "inspiracja_mark_fk": prot.inspiration_mark_fk,
        "udzielenie_mark_fk": prot.participation_mark_fk,
        "stosowanie_mark_fk": prot.use_of_learning_methods_mark_fk,
        "poslugiwanie_mark_fk": prot.use_of_tools_mark_fk,
        "panowanie_mark_fk": prot.control_mark_fk,
        "tworzenie_mark_fk": prot.creation_mark_fk
    }


def get_protocol_appeal(protocol_id: int, db: Session) -> bool:
    appeal: Optional[tuple[int]] = db.query(models.Appeal.id).filter(
        models.Appeal.protocol_fk == protocol_id).first()

    return appeal is not None


def get_audits_schedule(
    user_id: int, db: Session
) -> Optional[list[dict[str, Union[Date, str, bool, int, None]]]]:
    temp: Query[tuple[int]] = db.query(models.Audit_commission.id).filter(
        models.Audit_commission.user_fk == user_id)
    komisje: Optional[list[int]] = [id[0] for id in temp]
    temp = db.query(models.Audit.id).filter(
        models.Audit.audit_commission_fk.in_(komisje))
    hospitacje: Optional[list[int]] = [id[0] for id in temp]
    temp = db.query(models.Audit.course_fk).filter(
        models.Audit.id.in_(hospitacje))
    courses: Optional[list[int]] = [course[0] for course in temp]
    res: Optional[list[tuple[Date, int, str, str, str, str]]] = db.query(models.Audit.date, models.Audit.id, models.Course.code, models.Course.name, models.User.name,
     models.User.surname).join(models.Course, models.Course.id == models.Audit.course_fk)\
     .join(models.User, models.User.id == models.Audit.user_fk)\
     .filter(and_(models.Course.id.in_(courses), models.Audit.id.in_(hospitacje))).all()

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


def get_audits_details(
        audit_id: int,
        db: Session) -> Optional[dict[str, Union[Date, str, int, None]]]:
    temp: Optional[tuple[int]] = db.query(models.Audit.course_fk).filter(
        models.Audit.id == (audit_id)).first()
    if temp is None:
        return None

    course: int = temp[0]

    temp = db.query(models.User.id).filter(
        and_(models.Course.id == course,
             models.User.id == models.Course.user_fk)).first()
    user: int = temp[0]

    r: Optional[tuple[Date, int, str, str, str, str, str, str, str, str, int,
                      str, str]] = db.query(
                          models.Audit.date,
                          models.Audit.id, models.Course.code,
                          models.Course.name, models.User.name,
                          models.User.surname,
                          models.Course.level_and_form_of_study,
                          models.Course.didactic_form, models.Course.date,
                          models.Course.participants_number, models.Course.place,
                          models.Course.organizational_entity).filter(
                              and_(
                                  models.Course.id == course,
                                  models.Audit.id == Audit_id,
                                  models.User.id == user)).first()

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


def put_confirm_protocol(protocol_id: int, db: Session) -> bool:
    prot: Optional[models.Protocol] = db.query(
        models.Protocol).filter(models.Protocol.id == protocol_id).first()
    if prot is None:
        return False

    db.query(models.Protocol).filter(models.Protocol.id == protocol_id).update(
        {models.Protocol.is_approved: True})
    db.commit()

    prot = db.query(models.Protocol).filter(
        and_(models.Protocol.id == protocol_id,
             models.Protocol.is_approved == True)).first()
    if prot is None:
        return False

    return True


def delete_appeal(protocol_id: int, user_id: int, db: Session) -> bool:
    appeal: Optional[models.Appeal] = db.query(models.Appeal).filter(
        and_(models.Appeal.protocol_fk == protocol_id,
             models.Appeal.user_fk == user_id)).first()
    db.delete(appeal)
    db.commit()
    appeal = db.query(models.Appeal).filter(
        and_(models.Appeal.protocol_fk == protocol_id,
             models.Appeal.user_fk == user_id)).first()
    if appeal is None:
        return True
    return False


def put_unconfirm_protocol(protocol_id: int, db: Session) -> bool:
    prot: Optional[models.Protocol] = db.query(
        models.Protocol).filter(models.Protocol.id == protocol_id).first()
    if prot is None:
        return False

    db.query(models.Protocol).filter(models.Protocol.id == protocol_id).update(
        {models.Protocol.czy_zatwierdzona: False})
    db.commit()

    prot = db.query(models.Protocol).filter(
        and_(models.Protocol.id == protocol_id,
             models.Protocol.is_approved == False)).first()
    if prot is None:
        return False

    return True
