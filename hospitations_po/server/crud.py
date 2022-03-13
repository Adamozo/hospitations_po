from decimal import Decimal
from ntpath import join
from pyexpat import model
from sqlite3 import Date
from sqlalchemy.orm import Session, Query
from sqlalchemy import and_, false, true
from hospitations_po.server import models
from hospitations_po.server import schemas
from typing import Any, Optional, Union


def get_protocols_tutor(user_id: int, db: Session) -> list[schemas.ProtocolShort]:

    res: list[tuple[str, bool, int, str, str, float]] = db.query(models.Audit.date, models.Protocol.is_approved, models.Protocol.id,\
          models.Protocol.mark,  models.Course.code,  models.Course.name)\
        .join( models.Protocol,  models.Audit.protocol_fk ==  models.Protocol.id)\
            .join( models.Course,  models.Course.id ==  models.Audit.course_fk)\
                .filter( models.Audit.user_fk == user_id).all()

    return [
        schemas.ProtocolShort(date=r[0],
                              is_approved=r[1],
                              id=r[2],
                              mark=r[3],
                              course_number=r[4],
                              course_name=r[5]) for r in res
    ]


def get_protocol(protocol_id: int, db: Session) -> Optional[schemas.Protocol]:

    protocol: Optional[models.Protocol] = db.query(
        models.Protocol).filter(models.Protocol.id == protocol_id).first()

    if protocol is None:
        return None

    return schemas.Protocol(date=protocol.date,
                            is_approved=protocol.is_approved,
                            mark=protocol.mark,
                            justification=protocol.justification,
                            conclusions_and_recommendations=protocol.conclusions_and_recommendations,
                            read_date=protocol.read_date,
                            is_sent=protocol.is_sent,
                            presentation_mark_fk=protocol.presentation_mark_fk,
                            explanation_mark_fk=protocol.explanation_mark_fk,
                            realization_mark_fk=protocol.realization_mark_fk,
                            inspiration_mark_fk=protocol.inspiration_mark_fk,
                            participation_mark_fk=protocol.participation_mark_fk,
                            use_of_learning_methods_mark_fk=protocol.use_of_learning_methods_mark_fk,
                            use_of_tools_mark_fk=protocol.use_of_tools_mark_fk,
                            control_mark_fk=protocol.control_mark_fk,
                            creation_mark_fk=protocol.creation_mark_fk)


def get_appeal(protocol_id: int, db: Session) -> Optional[models.Appeal]:
    return db.query(models.Appeal).filter(models.Appeal.protocol_fk == protocol_id).first()


def insert_appeal(appeal: schemas.AppealCreate, user_id: int, protocol_id: int, db: Session) -> models.Appeal:

    new_appeal: models.Appeal = models.Appeal(text=appeal.text,
                                              user_fk=user_id,
                                              protocol_fk=protocol_id,
                                              date=appeal.date)
    db.add(new_appeal)
    db.commit()
    db.refresh(new_appeal)

    return new_appeal


def get_course_protocol(protocol_id: int, db: Session) -> Optional[schemas.Course]:

    audit_course: Optional[tuple[int]] = db.query(
        models.Audit.course_fk).filter(models.Audit.protocol_fk == protocol_id).first()

    if audit_course is not None:
        course: Optional[models.Course] = db.query(
            models.Course).filter(models.Course.id == audit_course[0]).first()

        if course is not None:
            return schemas.Course(id=course.id,
                                  user_fk=course.user_fk,
                                  name=course.name,
                                  code=course.code,
                                  level_and_form_of_study=course.level_and_form_of_study,
                                  didactic_form=course.didactic_form,
                                  date=course.date,
                                  participants_number=course.participants_number,
                                  place=course.place,
                                  organizational_entity=course.organizational_entity,
                                  term=course.term)

    return None


def get_protocols_comission_head(user_id: int, db: Session) -> list[schemas.ProtocolEdit]:
    
    res: Optional[list[tuple[str, bool, int, str, str, str, str, bool]]] = \
        db.query(models.Audit.date, models.Protocol.is_approved, models.Protocol.id, models.Course.code, models.Course.name, models.User.name, models.User.surname, models.Protocol.is_sent)\
        .join( models.Protocol,  models.Audit.protocol_fk ==  models.Protocol.id)\
            .join( models.Course,  models.Audit.course_fk ==  models.Course.id)\
                .join( models.User,  models.Audit.user_fk ==  models.User.id)\
                    .join( models.Audit_commission,  models.Audit.audit_commission_fk ==  models.Audit_commission.id)\
                        .filter( models.Audit_commission.user_fk == user_id).all()

    if res is not None:
        return [
            schemas.ProtocolEdit(date=r[0],
                                 is_approved=r[1],
                                 id=r[2],
                                 course_number=r[3],
                                 course_name=r[4],
                                 audited_name=r[5],
                                 audited_surname=r[6],
                                 is_sent=r[7]) for r in res
        ]

    return []


def update_protocol(protocol: models.Protocol, protocol_id: int, db: Session) -> Optional[schemas.Protocol]:
    
    prot: Optional[models.Protocol] = db.query(
        models.Protocol).filter(models.Protocol.id == protocol_id).first()
    
    if prot is None:
        return None

    db.query(models.Protocol).filter(models.Protocol.id == protocol_id).update({
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

    prot = db.query(models.Protocol).filter(models.Protocol.id == protocol_id).first()

    return schemas.Protocol(date=prot.date,
                            is_approved=prot.is_approved,
                            mark=prot.mark,
                            justification=prot.justification,
                            conclusions_and_recommendations=prot.conclusions_and_recommendations,
                            read_date=prot.read_date,
                            is_sent=prot.is_sent,
                            presentation_mark_fk=prot.presentation_mark_fk,
                            explanation_mark_fk=prot.explanation_mark_fk,
                            realization_mark_fk=prot.realization_mark_fk,
                            inspiration_mark_fk=prot.inspiration_mark_fk,
                            participation_mark_fk=prot.participation_mark_fk,
                            use_of_learning_methods_mark_fk=prot.use_of_learning_methods_mark_fk,
                            use_of_tools_mark_fk=prot.use_of_tools_mark_fk,
                            control_mark_fk=prot.control_mark_fk,
                            creation_mark_fk=prot.creation_mark_fk)


def get_protocol_appeal(protocol_id: int, db: Session) -> bool:
    
    appeal: Optional[tuple[int]] = db.query(
        models.Appeal.id).filter(models.Appeal.protocol_fk == protocol_id).first()

    return appeal is not None


def get_audits_schedule(user_id: int, db: Session) -> Optional[list[schemas.AuditsSchedule]]:
    
    temp: Query[tuple[int]] = db.query(
        models.Audit_commission.id).filter(models.Audit_commission.user_fk == user_id)
    
    komisje: Optional[list[int]] = [id[0] for id in temp]
    temp = db.query(models.Audit.id).filter(models.Audit.audit_commission_fk.in_(komisje))
    
    hospitacje: Optional[list[int]] = [id[0] for id in temp]
    temp = db.query(models.Audit.course_fk).filter(models.Audit.id.in_(hospitacje))
    
    courses: Optional[list[int]] = [course[0] for course in temp]
    res: Optional[list[tuple[Date, int, str, str, str, str]]] = db.query( models.Audit.date,  models.Audit.id,  models.Course.code, models.Course.name, models.User.name,
      models.User.surname).join( models.Course, models.Course.id ==  models.Audit.course_fk)\
     .join( models.User,  models.User.id ==  models.Audit.user_fk)\
     .filter(and_( models.Course.id.in_(courses),  models.Audit.id.in_(hospitacje))).all()

    if res is not None:
        return [
            schemas.AuditsSchedule(date=r[0],
                                   id=r[1],
                                   course_number=r[2],
                                   course_name=r[3],
                                   appealed_name=r[4],
                                   appealed_surname=r[5]) for r in res
        ]

    return []


def get_audits_details(audit_id: int, db: Session) -> Optional[schemas.AuditsDetails]:
    temp: Optional[tuple[int]] = db.query(models.Audit.course_fk).filter(models.Audit.id == audit_id).first()
    
    if temp is None:
        return None

    course: int = temp[0]

    t: Optional[tuple[int]] = db.query(models.User.id).filter(
        and_(models.Course.id == course, models.User.id == models.Course.user_fk)).first()

    user: int = t[0]

    r = db.query(models.Audit.date, models.Audit.id, models.Course.code, models.Course.name, models.User.name,
                 models.User.surname, models.Course.level_and_form_of_study, models.Course.didactic_form,
                 models.Course.date, models.Course.participants_number, models.Course.place,
                 models.Course.organizational_entity).filter(
                     and_(models.Course.id == course, models.Audit.id == audit_id,
                          models.User.id == user)).first()

    if r is not None:
        return schemas.AuditsDetails(date=r[0],
                                     id=r[1],
                                     course_number=r[2],
                                     course_name=r[3],
                                     appealed_name=r[4],
                                     appealed_surname=r[5],
                                     level_and_form_of_study=r[6],
                                     didactic_form=r[7],
                                     course_date=r[8],
                                     participants_number=r[9],
                                     place=r[10],
                                     organizational_entity=r[11])

    return None


def put_confirm_protocol(protocol_id: int, db: Session) -> bool:
    
    prot: Optional[models.Protocol] = db.query(
        models.Protocol).filter(models.Protocol.id == protocol_id).first()
    
    if prot is None:
        return False

    db.query(models.Protocol).filter(models.Protocol.id == protocol_id).update(
        {models.Protocol.is_approved: True})
    db.commit()

    prot = db.query(models.Protocol).filter(
        and_(models.Protocol.id == protocol_id, models.Protocol.is_approved == True)).first()
    
    if prot is None:
        return False

    return True


def delete_appeal(protocol_id: int, user_id: int, db: Session) -> bool:
    
    appeal: Optional[models.Appeal] = db.query(models.Appeal).filter(
        and_(models.Appeal.protocol_fk == protocol_id, models.Appeal.user_fk == user_id)).first()
    
    db.delete(appeal)
    db.commit()
    
    appeal = db.query(models.Appeal).filter(
        and_(models.Appeal.protocol_fk == protocol_id, models.Appeal.user_fk == user_id)).first()
    
    if appeal is None:
        return True
    
    return False


def put_unconfirm_protocol(protocol_id: int, db: Session) -> bool:
    
    prot: Optional[models.Protocol] = db.query(
        models.Protocol).filter(models.Protocol.id == protocol_id).first()
    
    if prot is None:
        return False

    db.query(models.Protocol).filter(models.Protocol.id == protocol_id).update(
        {models.Protocol.is_approved: False})
    db.commit()

    prot = db.query(models.Protocol).filter(
        and_(models.Protocol.id == protocol_id, models.Protocol.is_approved == False)).first()
    
    if prot is None:
        return False

    return True
