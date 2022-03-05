from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.schema import CheckConstraint
from hospitations_po.server.database import Base


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    def __init__(self, name: str) -> None:
        self.name = name


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role_fk = Column(Integer,
                     ForeignKey('role.id'),
                     index=True,
                     nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    def __init__(self, login:str, password:str, phone_number:str, email:str, role_fk: int, name:str, surname:str) -> None:
        self.login = login
        self.password = password
        self.phone_number = phone_number
        self.email = email
        self.role_fk = role_fk
        self.name = name
        self.surname = surname


class Audit_commission(Base):
    __tablename__ = "audit_commission"

    id = Column(Integer, primary_key=True, index=True)
    user_fk = Column(Integer,
                     ForeignKey('user.id'),
                     index=True,
                     nullable=False)

    def __init__(self, commitetee_lider:int) -> None:
        self.user_fk = commitetee_lider


class Audit_commission_User(Base):
    __tablename__ = "audit_commission_user"

    audit_commission_fk = Column(Integer,
                                 ForeignKey('audit_commission.id'),
                                 index=True,
                                 nullable=False,
                                 primary_key=True)
    user_fk = Column(Integer,
                     ForeignKey('user.id'),
                     index=True,
                     nullable=False,
                     primary_key=True)

    def __init__(self, audit_commission_fk: str, user_fk:str) -> None:
        self.audit_commission_fk = audit_commission_fk
        self.user_fk = user_fk


class Mark(Base):
    __tablename__ = "mark"

    mark = Column(Float, primary_key=True, unique=True)

    def __init__(self, mark:float) -> None:
        self.mark = mark


class Protocol(Base):
    __tablename__ = "protocol"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    mark = Column(String)
    justification = Column(String)
    conclusions_and_recommendations = Column(String)
    read_date = Column(Date)
    is_approved = Column(Boolean, nullable=False)
    is_sent = Column(Boolean, nullable=False)
    presentation_mark_fk = Column(Float, ForeignKey('mark.mark'))
    explanation_mark_fk = Column(Float, ForeignKey('mark.mark'))
    realization_mark_fk = Column(Float, ForeignKey('mark.mark'))
    inspiration_mark_fk = Column(Float, ForeignKey('mark.mark'))
    participation_mark_fk = Column(Float, ForeignKey('mark.mark'))
    use_of_learning_methods_mark_fk = Column(Float, ForeignKey('mark.mark'))
    use_of_tools_mark_fk = Column(Float, ForeignKey('mark.mark'))
    control_mark_fk = Column(Float, ForeignKey('mark.mark'))
    creation_mark_fk = Column(Float, ForeignKey('mark.mark'))

    def __init__(self, date: Date,is_approved: bool, is_sent: bool, mark: float = None,  justification: str = None, conclusions_and_recommendations: str = None, read_date: Date = None,
    presentation_mark_fk: float = None, explanation_mark_fk: float = None, realization_mark_fk: float = None, inspiration_mark_fk: float = None, participation_mark_fk: float = None,
    use_of_learning_methods_mark_fk: float = None, use_of_tools_mark_fk: float = None, control_mark_fk: float = None, creation_mark_fk: float = None) -> None:
        self.date = date
        self.mark = mark
        self.justification = justification
        self.conclusions_and_recommendations = conclusions_and_recommendations
        self.read_date = read_date
        self.is_approved = is_approved
        self.is_sent = is_sent
        self.presentation_mark_fk = presentation_mark_fk
        self.explanation_mark_fk = explanation_mark_fk
        self.realization_mark_fk = realization_mark_fk
        self.inspiration_mark_fk = inspiration_mark_fk
        self.participation_mark_fk = participation_mark_fk
        self.use_of_learning_methods_mark_fk = use_of_learning_methods_mark_fk
        self.use_of_tools_mark_fk = use_of_tools_mark_fk
        self.control_mark_fk = control_mark_fk
        self.creation_mark_fk = creation_mark_fk 


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    user_fk = Column(Integer,
                     ForeignKey('user.id'),
                     index=True,
                     nullable=False)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)
    level_and_form_of_study = Column(String, nullable=False)
    didactic_form = Column(String, nullable=False)
    date = Column(String, nullable=False)
    participants_number = Column(Integer, nullable=False)
    place = Column(String, nullable=False)
    organizational_entity = Column(String, nullable=False)
    term = Column(String, nullable=False)

    def __init__(self, user_fk: int, name: str, code: str, level_and_form_of_study: str, didactic_form: str, date:str, participants_number: str, place: str, organizational_entity: str, term: str) -> None:
        self.user_fk = user_fk
        self.name = name
        self.code = code
        self.level_and_form_of_study = level_and_form_of_study
        self.didactic_form = didactic_form
        self.date = date
        self.participants_number = participants_number
        self.place = place
        self.organizational_entity = organizational_entity
        self.term = term


class User_Course(Base):
    __tablename__ = "user_course"

    course_fk = Column(Integer,
                       ForeignKey('course.id'),
                       index=True,
                       nullable=False,
                       primary_key=True)
    user_fk = Column(Integer,
                     ForeignKey('user.id'),
                     index=True,
                     nullable=False,
                     primary_key=True)

    def __init__(self, course_fk: int, user_fk:int) -> None:
        self.course_fk = course_fk
        self.user_fk = user_fk


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, nullable=False, index=True, primary_key=True)
    term = Column(String(20), nullable=False)
    academic_year = Column(String(10), nullable=False)
    approval_date = Column(Date)
    term_start = Column(Date, nullable=False)
    term_end = Column(Date, nullable=False)

    def __init__(self, term: str, academic_year: str, term_start: Date, term_end: Date, approval_date: Date = None) -> None:
        self.term = term
        self. academic_year = academic_year
        self.approval_date = approval_date
        self.term_start = term_start
        self.term_end = term_end


class Audit(Base):
    __tablename__ = "audit"

    id = Column(Integer, primary_key=True, index=True)
    audit_commission_fk = Column(Integer,
                                 ForeignKey('audit_commission.id'),
                                 index=True,
                                 nullable=False)
    schedule_fk = Column(Integer,
                         ForeignKey('schedule.id'),
                         index=True,
                         nullable=False)
    user_fk = Column(Integer,
                     ForeignKey('user.id'),
                     index=True,
                     nullable=False)
    date = Column(Date, nullable=False)
    course_fk = Column(Integer,
                       ForeignKey('course.id'),
                       index=True,
                       nullable=False)
    protocol_fk = Column(Integer,
                         ForeignKey('protocol.id'),
                         index=True,
                         nullable=False)

    def __init__(self, audit_comission_fk: int, schedule_fk: int, user_fk: int, date: Date, course_fk: int, protcol_fk: int) -> None:
        self.audit_commission_fk = audit_comission_fk
        self.schedule_fk = schedule_fk
        self.user_fk = user_fk
        self.date = date
        self.course_fk = course_fk
        self.protocol_fk = protcol_fk


class Appeal(Base):
    __tablename__ = "appeal"

    id = Column(Integer, primary_key=True, index=True)
    user_fk = Column(Integer,
                     ForeignKey('user.id'),
                     index=True,
                     nullable=False)
    date = Column(Date, nullable=False)
    text = Column(String, nullable=False)
    protocol_fk = Column(Integer,
                         ForeignKey('protocol.id'),
                         index=True,
                         nullable=False)

    def __init__(self, user_fk:int, date:Date, text:str, protocol_fk:str) -> None:
        self.user_fk = user_fk
        self.date = date
        self.text = text
        self.protocol_fk = protocol_fk
