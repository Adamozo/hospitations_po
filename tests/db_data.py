from hospitations_po.server.models import *
import datetime


def get_roles():
    roles = []
    roles.append(Role('tutor'))
    roles.append(Role('admin'))
    roles.append(Role('test1'))

    return roles


def get_users():
    users = []
    users.append(
        User(login="tutor1",
             password="tutor1password",
             phone_number="111-111-111",
             email="tutor1@email.com",
             role_fk=1,
             name="tutor1name",
             surname="tutor1surname"))

    users.append(
        User(login="admin1",
             password="admin1password",
             phone_number="222-222-222",
             email="admin1@email.com",
             role_fk=2,
             name="admin1name",
             surname="admin1surname"))

    users.append(
        User(login="test1",
             password="tutor1password",
             phone_number="333-333-333",
             email="test1@email.com",
             role_fk=3,
             name="test1name",
             surname="test1surname"))

    users.append(
        User(login="tutor2",
             password="tutor2password",
             phone_number="444-444-444",
             email="test1@email.com",
             role_fk=1,
             name="tutor2name",
             surname="tutor2surname"))

    users.append(
        User(login="tutor3",
             password="tutor3password",
             phone_number="555-555-555",
             email="tutor3@email.com",
             role_fk=1,
             name="tutor3name",
             surname="tutor3surname"))

    return users


def get_audit_commisons():
    audit_commisions = []

    audit_commisions.append(Audit_commission(commitetee_lider=4))

    audit_commisions.append(Audit_commission(commitetee_lider=5))

    audit_commisions.append(Audit_commission(commitetee_lider=1))

    return audit_commisions


def get_audit_commision_users():
    audit_commision_users = []

    return audit_commision_users


def get_marks():
    marks = []
    marks.append(Mark(0.0))
    marks.append(Mark(2.0))
    marks.append(Mark(3.0))
    marks.append(Mark(4.0))
    marks.append(Mark(5.0))
    marks.append(Mark(5.5))

    return marks


def get_protocols():
    protocols = []
    protocols.append(
        Protocol(date=datetime.date(2022, 2, 1),
                 mark="negatywna",
                 justification="some text",
                 conclusions_and_recommendations="some text",
                 read_date=datetime.date(2022, 2, 2),
                 is_approved=False,
                 is_sent=True,
                 presentation_mark_fk=2.0,
                 explanation_mark_fk=2.0,
                 realization_mark_fk=5.5,
                 inspiration_mark_fk=2.0,
                 participation_mark_fk=2.0,
                 use_of_learning_methods_mark_fk=2.0,
                 use_of_tools_mark_fk=2.0,
                 control_mark_fk=2.0,
                 creation_mark_fk=2.0))

    protocols.append(
        Protocol(date=datetime.date(2022, 3, 2),
                 mark="wzorowa",
                 justification="some text",
                 conclusions_and_recommendations="some text",
                 read_date=datetime.date(2022, 3, 3),
                 is_approved=True,
                 is_sent=True,
                 presentation_mark_fk=5.0,
                 explanation_mark_fk=5.0,
                 realization_mark_fk=5.5,
                 inspiration_mark_fk=5.0,
                 participation_mark_fk=5.0,
                 use_of_learning_methods_mark_fk=5.0,
                 use_of_tools_mark_fk=5.0,
                 control_mark_fk=5.0,
                 creation_mark_fk=5.0))

    protocols.append(
        Protocol(date=datetime.date(2022, 2, 3),
                 mark="dostateczna",
                 justification="some text",
                 conclusions_and_recommendations="some text",
                 read_date=datetime.date(2022, 2, 4),
                 is_approved=False,
                 is_sent=True,
                 presentation_mark_fk=5.0,
                 explanation_mark_fk=4.0,
                 realization_mark_fk=5.5,
                 inspiration_mark_fk=3.0,
                 participation_mark_fk=3.0,
                 use_of_learning_methods_mark_fk=3.0,
                 use_of_tools_mark_fk=3.0,
                 control_mark_fk=2.0,
                 creation_mark_fk=2.0))

    return protocols


def get_courses():
    courses = []
    courses.append(
        Course(user_fk=1,
               name="course1",
               code="INZ001P",
               level_and_form_of_study="some text 1",
               didactic_form="Project",
               date="PN TP 09:15-11:00",
               participants_number=0,
               place="A1 s320",
               organizational_entity="random text",
               term="summer 2021/2022"))

    courses.append(
        Course(user_fk=4,
               name="course4",
               code="INZ004P",
               level_and_form_of_study="some text 4",
               didactic_form="Lecture",
               date="WT TP 09:15-11:00",
               participants_number=0,
               place="A1 s320",
               organizational_entity="random text",
               term="summer 2021/2022"))

    courses.append(
        Course(user_fk=5,
               name="course5",
               code="INZ005P",
               level_and_form_of_study="some text 5",
               didactic_form="Project",
               date="PN TP 19:15-21:00",
               participants_number=0,
               place="A1 s320",
               organizational_entity="random text",
               term="summer 2021/2022"))

    return courses


def get_user_courses():
    user_courses = []

    return user_courses


def get_schedules():
    schedules = []
    schedules.append(
        Schedule(term="summer",
                 academic_year="2021/2022",
                 approval_date=datetime.date(2022, 9, 1),
                 term_start=datetime.date(2022, 2, 1),
                 term_end=datetime.date(2022, 9, 12)))

    return schedules


def get_audits():
    audits = []
    audits.append(
        Audit(audit_comission_fk=1,
              schedule_fk=1,
              user_fk=1,
              date=datetime.date(2022, 2, 1),
              course_fk=1,
              protcol_fk=1))
    audits.append(
        Audit(audit_comission_fk=2,
              schedule_fk=1,
              user_fk=4,
              date=datetime.date(2022, 3, 1),
              course_fk=2,
              protcol_fk=2))
    audits.append(
        Audit(audit_comission_fk=3,
              schedule_fk=1,
              user_fk=5,
              date=datetime.date(2022, 3, 1),
              course_fk=3,
              protcol_fk=3))

    return audits


def get_appeals():
    appeals = []
    appeals.append(
        Appeal(user_fk=1,
               date=datetime.date(2022, 2, 2),
               text="because I can",
               protocol_fk=1))

    return appeals
