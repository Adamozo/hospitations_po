from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.schema import CheckConstraint
from hospitations_po.server.database import Base


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


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


class Audit_commission(Base):
    __tablename__ = "audit_commission"

    id = Column(Integer, primary_key=True, index=True)
    user_fk = Column(Integer,
                     ForeignKey('user.id'),
                     index=True,
                     nullable=False)


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


class Mark(Base):
    __tablename__ = "mark"

    mark = Column(Float, primary_key=True, unique=True)


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


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, nullable=False, index=True, primary_key=True)
    term = Column(String(20), nullable=False)
    academic_year = Column(String(10), nullable=False)
    approval_date = Column(Date)
    term_start = Column(Date, nullable=False)
    term_end = Column(Date, nullable=False)


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
