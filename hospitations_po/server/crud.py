from decimal import Decimal
from ntpath import join
from pyexpat import model
from sqlite3 import Date
from sqlalchemy.orm import Session, Query
from sqlalchemy import and_, false, true
from hospitations_po.server.models import *
from hospitations_po.server import schemas
from typing import Any, Optional, Union


def get_protocols_tutor(
        user_id: int, db: Session) -> list[dict[str, Union[str, int, float]]]:
    res: list[tuple[str, bool, int, str, str, float]] = db.query(Audit.date, Protocol.is_approved, Protocol.id,\
          Protocol.mark,  Course.code,  Course.name)\
        .join( Protocol,  Audit.protocol_fk ==  Protocol.id)\
            .join( Course,  Course.id ==  Audit.course_fk)\
                .filter( Audit.user_fk == user_id).all()

    return [schemas.ProtocolShort(date=r[0], is_approved=r[1], id=r[2], mark=r[3], course_number=r[4], course_name=r[5]) for r in res]


def get_protocol(protocol_id: int, db: Session) -> Optional[dict[str, Any]]:
    protocol: Optional[ Protocol] = db.query(
         Protocol).filter( Protocol.id == protocol_id).first()
    if protocol is None:
        return None

    return schemas.Protocol(date=protocol.date, is_approved=protocol.is_approved, mark=protocol.mark, justification=protocol.justification, conclusions_and_recommendations=protocol.conclusions_and_recommendations,
    read_date=protocol.read_date, is_sent=protocol.is_sent, presentation_mark_fk=protocol.presentation_mark_fk, explanation_mark_fk=protocol.explanation_mark_fk,  
    realization_mark_fk=protocol.realization_mark_fk, inspiration_mark_fk=protocol.inspiration_mark_fk, participation_mark_fk=protocol.participation_mark_fk,
    use_of_learning_methods_mark_fk=protocol.use_of_learning_methods_mark_fk, use_of_tools_mark_fk=protocol.use_of_tools_mark_fk, control_mark_fk=protocol.control_mark_fk,
    creation_mark_fk=protocol.creation_mark_fk)


def get_appeal(protocol_id: int, db: Session) -> Optional[ Appeal]:
    return db.query(Appeal).filter(
         Appeal.protocol_fk == protocol_id).first()


def insert_appeal(appeal:  schemas.AppealCreate, user_id: int, protocol_id: int,
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
        course: Optional[ Course] = db.query(Course).filter( Course.id == audit_course[0]).first()

        return schemas.Course(id=course.id, user_fk=course.user_fk, name=course.name, code=course.code, level_and_form_of_study=course.level_and_form_of_study,
        didactic_form=course.didactic_form, date=course.date, participants_number=course.participants_number, place=course.place,
        organizational_entity=course.organizational_entity, term=course.term)

    return None


def get_protocols_comission_head(user_id: int,db: Session) -> list[dict[str, Union[int, bool, None, str]]]:
    res: Optional[list[tuple[str, bool, int, str, str, str, str, bool]]] = \
        db.query(Audit.date, Protocol.is_approved, Protocol.id, Course.code, Course.name, User.name, User.surname, Protocol.is_sent)\
        .join( Protocol,  Audit.protocol_fk ==  Protocol.id)\
            .join( Course,  Audit.course_fk ==  Course.id)\
                .join( User,  Audit.user_fk ==  User.id)\
                    .join( Audit_commission,  Audit.audit_commission_fk ==  Audit_commission.id)\
                        .filter( Audit_commission.user_fk == user_id).all()

    return [schemas.ProtocolEdit(date = r[0], is_approved=r[1], id=r[2], course_number=r[3], course_name=r[4], audited_name = r[5], audited_surname = r[6], is_sent=r[7]) for r in res]


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

    prot = db.query(Protocol).filter( Protocol.id == protocol_id).first()

    return schemas.Protocol(date=prot.date, is_approved=prot.is_approved, mark=prot.mark, justification=prot.justification, conclusions_and_recommendations=prot.conclusions_and_recommendations,
    read_date=prot.read_date, is_sent=prot.is_sent, presentation_mark_fk=prot.presentation_mark_fk, explanation_mark_fk=prot.explanation_mark_fk, realization_mark_fk=prot.realization_mark_fk,
    inspiration_mark_fk=prot.inspiration_mark_fk, participation_mark_fk=prot.participation_mark_fk, use_of_learning_methods_mark_fk=prot.use_of_learning_methods_mark_fk, use_of_tools_mark_fk=prot.use_of_tools_mark_fk,
    control_mark_fk=prot.control_mark_fk, creation_mark_fk=prot.creation_mark_fk)


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

    return [schemas.AuditsSchedule(date=r[0], id=r[1], course_number = r[2], course_name = r[3], appealed_name = r[4], appealed_surname = r[5] ) for r in res]
    

def get_audits_details(
        audit_id: int,
        db: Session) -> Optional[dict[str, Union[Date, str, int, None]]]:
    temp: Optional[tuple[int]] = db.query(
         Audit.course_fk).filter( Audit.id == audit_id).first()
    if temp is None:
        return None

    course: int = temp[0]

    t = db.query(User.id).filter(
        and_( Course.id == course, User.id ==  Course.user_fk)).first()
    
    user: int = t[0]
    
    r = db.query(Audit.date, Audit.id, Course.code, Course.name, User.name, 
     User.surname, Course.level_and_form_of_study, Course.didactic_form, Course.date, Course.participants_number,
     Course.place, Course.organizational_entity).filter(and_(Course.id == course, Audit.id == audit_id,
     User.id == user)).first()

    return schemas.AuditsDetails(date=r[0], id=r[1], course_number = r[2], course_name = r[3], appealed_name = r[4], appealed_surname = r[5],
    level_and_form_of_study=r[6], didactic_form=r[7], course_date=r[8], participants_number=r[9], place=r[10], organizational_entity=r[11])
    


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
        { Protocol.is_approved: False})
    db.commit()

    prot = db.query( Protocol).filter(
        and_( Protocol.id == protocol_id,
              Protocol.is_approved == False)).first()
    if prot is None:
        return False

    return True
