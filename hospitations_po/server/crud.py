from decimal import Decimal
from ntpath import join
from pyexpat import model
from sqlite3 import Date
from sqlalchemy.orm import Session, Query
from sqlalchemy import and_, false, true
from hospitations_po.server.models import *
from hospitations_po.server.schemas import *
from typing import Any, Optional, Union
from datetime import datetime


def get_protocols_tutor(
        user_id: int, db: Session) -> list[dict[str, Union[str, int, float]]]:
    res: list[tuple[str, bool, int, str, str, float]] = db.query(Audit.date, Protocol.is_approved, Protocol.id,\
          Protocol.mark,  Course.code,  Course.name)\
        .join( Protocol,  Audit.protocol_fk ==  Protocol.id)\
            .join( Course,  Course.id ==  Audit.course_fk)\
                .filter( Audit.user_fk == user_id).all()

    return [{
        "date": r[0],
        "czy_zatwierdzony": r[1],
        "id": r[2],
        "nr_kursu": r[4],
        "nazwa_kursu": r[5],
        "mark": r[3]
    } for r in res]


def get_protocol(protocol_id: int, db: Session) -> Optional[dict[str, Any]]:
    protocol: Optional[ Protocol] = db.query(
         Protocol).filter( Protocol.id == protocol_id).first()
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


def get_appeal(protocol_id: int, db: Session) -> Optional[ Appeal]:
    return db.query( Appeal).filter(
         Appeal.protocol_fk == protocol_id).first()


def insert_appeal(appeal:  AppealCreate, user_id: int, protocol_id: int,
                  db: Session) ->  Appeal:
    new_appeal:  Appeal =  Appeal(text=appeal.text,
                                              user_fk=user_id,
                                              protocol_fk=protocol_id,
                                              date=appeal.date)
    db.add(new_appeal)
    db.commit()
    db.refresh(new_appeal)
    return new_appeal


def get_course_protocol(
        protocol_id: int,
        db: Session) -> Optional[dict[str, Union[str, int, None]]]:
    audit_course: Optional[tuple[int]] = db.query(
         Audit.course_fk).filter(
             Audit.protocol_fk == protocol_id).first()
    if audit_course is not None:
        course: Optional[ Course] = db.query(
             Course).filter( Course.id == audit_course[0]).first()
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
        db.query( Audit.date,  Protocol.is_approved,  Protocol.id,  Course.code,  Course.name,  User.name\
            ,  User.surname,  Protocol.is_sent)\
        .join( Protocol,  Audit.protocol_fk ==  Protocol.id)\
            .join( Course,  Audit.course_fk ==  Course.id)\
                .join( User,  Audit.user_fk ==  User.id)\
                    .join( Audit_commission,  Audit.audit_commission_fk ==  Audit_commission.id)\
                        .filter( Audit_commission.user_fk == user_id).all()

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
        protocol:  Protocol, protocol_id: int, db: Session
) -> Optional[dict[str, Union[int, str, Decimal, Date, None]]]:
    prot: Optional[ Protocol] = db.query(
         Protocol).filter( Protocol.id == protocol_id).first()
    if prot is None:
        return None

    db.query(
         Protocol).filter( Protocol.id == protocol_id).update({
             Protocol.justification:
            protocol.justification,
             Protocol.mark:
            protocol.mark,
             Protocol.conclusions_and_recommendations:
            protocol.conclusions_and_recommendations,
             Protocol.read_date:
            protocol.read_date,
             Protocol.is_approved:
            protocol.is_approved,
             Protocol.is_sent:
            protocol.is_sent,
             Protocol.presentation_mark_fk:
            protocol.presentation_mark_fk,
             Protocol.explanation_mark_fk:
            protocol.explanation_mark_fk,
             Protocol.realization_mark_fk:
            protocol.realization_mark_fk,
             Protocol.inspiration_mark_fk:
            protocol.inspiration_mark_fk,
             Protocol.participation_mark_fk:
            protocol.participation_mark_fk,
             Protocol.use_of_learning_methods_mark_fk:
            protocol.use_of_learning_methods_mark_fk,
             Protocol.use_of_tools_mark_fk:
            protocol.use_of_tools_mark_fk,
             Protocol.control_mark_fk:
            protocol.control_mark_fk,
             Protocol.creation_mark_fk:
            protocol.creation_mark_fk
        })
    db.commit()

    prot = db.query(
         Protocol).filter( Protocol.id == protocol_id).first()

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
    appeal: Optional[tuple[int]] = db.query( Appeal.id).filter(
         Appeal.protocol_fk == protocol_id).first()

    return appeal is not None


def get_audits_schedule(
    user_id: int, db: Session
) -> Optional[list[dict[str, Union[Date, str, bool, int, None]]]]:
    temp: Query[tuple[int]] = db.query( Audit_commission.id).filter(
         Audit_commission.user_fk == user_id)
    komisje: Optional[list[int]] = [id[0] for id in temp]
    temp = db.query( Audit.id).filter(
         Audit.audit_commission_fk.in_(komisje))
    hospitacje: Optional[list[int]] = [id[0] for id in temp]
    temp = db.query( Audit.course_fk).filter(
         Audit.id.in_(hospitacje))
    courses: Optional[list[int]] = [course[0] for course in temp]
    res: Optional[list[tuple[Date, int, str, str, str, str]]] = db.query( Audit.date,  Audit.id,  Course.code,  Course.name,  User.name,
      User.surname).join( Course,  Course.id ==  Audit.course_fk)\
     .join( User,  User.id ==  Audit.user_fk)\
     .filter(and_( Course.id.in_(courses),  Audit.id.in_(hospitacje))).all()

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
    temp: Optional[tuple[int]] = db.query(
         Audit.course_fk).filter( Audit.id == (audit_id)).first()
    if temp is None:
        return None

    course: int = temp[0]

    temp = db.query( User.id).filter(
        and_( Course.id == course,
              User.id ==  Course.user_fk)).first()
    user: int = temp[0]

    r: Optional[tuple[Date, int, str, str, str, str, str, str, str, str, int,
                      str, str]] = db.query(
                           Audit.date,  Audit.id,
                           Course.code,  Course.name,
                           User.name,  User.surname,
                           Course.level_and_form_of_study,
                           Course.didactic_form,  Course.date,
                           Course.participants_number,
                           Course.place,
                           Course.organizational_entity).filter(
                              and_( Course.id == course,
                                    Audit.id == audit_id,
                                    User.id == user)).first()

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
    prot: Optional[ Protocol] = db.query(
         Protocol).filter( Protocol.id == protocol_id).first()
    if prot is None:
        return False

    db.query( Protocol).filter( Protocol.id == protocol_id).update(
        { Protocol.is_approved: True})
    db.commit()

    prot = db.query( Protocol).filter(
        and_( Protocol.id == protocol_id,
              Protocol.is_approved == True)).first()
    if prot is None:
        return False

    return True


def delete_appeal(protocol_id: int, user_id: int, db: Session) -> bool:
    appeal: Optional[ Appeal] = db.query( Appeal).filter(
        and_( Appeal.protocol_fk == protocol_id,
              Appeal.user_fk == user_id)).first()
    db.delete(appeal)
    db.commit()
    appeal = db.query( Appeal).filter(
        and_( Appeal.protocol_fk == protocol_id,
              Appeal.user_fk == user_id)).first()
    if appeal is None:
        return True
    return False


def put_unconfirm_protocol(protocol_id: int, db: Session) -> bool:
    prot: Optional[ Protocol] = db.query(
         Protocol).filter( Protocol.id == protocol_id).first()
    if prot is None:
        return False

    db.query( Protocol).filter( Protocol.id == protocol_id).update(
        { Protocol.czy_zatwierdzona: False})
    db.commit()

    prot = db.query( Protocol).filter(
        and_( Protocol.id == protocol_id,
              Protocol.is_approved == False)).first()
    if prot is None:
        return False

    return True
