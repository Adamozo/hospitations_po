from numbers import Real
from tokenize import Double
from typing import List, Optional
from unicodedata import numeric
from xmlrpc.client import Boolean
from pydantic import BaseModel
from datetime import date, datetime


class AppealBase(BaseModel):
    text: str
    date: date


class AppealCreate(AppealBase):

    class Config:
        orm_mode = True


class Appeal(AppealBase):
    user_fk: int
    protocol_fk: int

    class Config:
        orm_mode = True


class ProtocolBase(BaseModel):
    date: date
    is_approved: Boolean


class ProtocolCreate(ProtocolBase):

    class Config:
        orm_mode = True


class Protocol(ProtocolBase):
    mark: Optional[str] = None
    justification: Optional[str] = None
    conclusions_and_recommendations: Optional[str] = None
    read_date: Optional[date] = None
    is_sent: Boolean
    presentation_mark_fk: Optional[float] = None
    explanation_mark_fk: Optional[float] = None
    realization_mark_fk: Optional[float] = None
    inspiration_mark_fk: Optional[float] = None
    participation_mark_fk: Optional[float] = None
    use_of_learning_methods_mark_fk: Optional[float] = None
    use_of_tools_mark_fk: Optional[float] = None
    control_mark_fk: Optional[float] = None
    creation_mark_fk: Optional[float] = None

    class Config:
        orm_mode = True


class ProtocolShort(ProtocolBase):
    id: int
    cournse_number: str
    course_name: str
    mark: Optional[str] = None


class ProtocolEdit(ProtocolBase):
    id: int
    cournse_number: str
    course_name: str
    audited_name: str
    audited_surname: str
    is_sent: Boolean


class ProtocolDetails(ProtocolEdit):
    level_and_form_of_study: str
    didactic_form: str
    date: str
    participants_number: int
    place: str
    organizational_entity: str


class Course(BaseModel):
    id: int
    user_fk: int
    name: str
    code: str
    level_and_form_of_study: str
    didactic_form: str
    date: str
    participants_number: int
    place: str
    organizational_entity: str
    term: str
