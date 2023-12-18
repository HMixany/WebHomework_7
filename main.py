import argparse
import random
from datetime import date
from sqlalchemy.exc import SQLAlchemyError

from conf.db import session
from conf.models import Teacher, Group, Student, Subject, Grade


parser = argparse.ArgumentParser(description='CLI program for CRUD operations on a PostgreSQL database')
parser.add_argument('--action', '-a', choices=['create', 'list', 'update', 'remove'], required=True,
                    help='Operation to perform')
parser.add_argument('--model', '-m', choices=['Teacher', 'Group', 'Student', 'Subject', 'Grade'],
                    required=True, help='Model on which to perform the operation')

# Optional arguments for specific operations
parser.add_argument('--id', type=int, help='ID of the record (for update and remove operations)')
parser.add_argument('--name', '-n', help='Name of the record (for add and update operations)')
parser.add_argument('--grade', '-g', help='Grade of the record (for add and update grades)',
                    default=random.randint(0, 100))
parser.add_argument('--sub_id', help='Subject_id of the record (for add and update grades)')
parser.add_argument('--student_id', help='Student_id of the record (for add and update grades)')
parser.add_argument('--group_id', help='Group_id of the record (for add and update students)')
parser.add_argument('--teacher_id', help='Teacher_id of the record (for add and update subjects)')


def session_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as err:
            print(err)
            session.rollback()
        finally:
            session.close()

    return inner


@session_error
def create_record(**kwargs):
    model = kwargs.get('model')
    name = kwargs.get('name')
    match model:
        case "Teacher":
            if not name:
                parser.error('--name is required for create operation')
            first_name, last_name = name.split()
            teacher = Teacher(first_name=first_name, last_name=last_name)
            session.add(teacher)
        case "Group":
            if not name:
                parser.error('--name is required for create operation')
            group = Group(name=name)
            session.add(group)
        case "Subject":
            teacher_id = kwargs.get('teacher_id')
            if not name or not teacher_id:
                parser.error('--name and --teacher_id is required for create operation')
            subject = Subject(name=kwargs.get('name'), teacher_id=int(teacher_id))
            session.add(subject)
        case "Student":
            group_id = kwargs.get('group_id')
            if not name or not group_id:
                parser.error('--name and --group_id is required for create operation')
            first_name, last_name = name.split()
            student = Student(first_name=first_name, last_name=last_name, group_id=int(group_id))
            session.add(student)
        case "Grade":
            student_id = kwargs.get('student_id')
            subject_id = kwargs.get('subject_id')
            grade = kwargs.get('grade')
            if not student_id or not subject_id:
                parser.error('--student_id and --subject_id is required for create operation')
            grade_data = Grade(
                grade=int(grade),
                grade_date=date.today(),
                student_id=int(student_id),
                subject_id=int(subject_id)
            )
            session.add(grade_data)
    session.commit()


@session_error
def list_records(**kwargs):
    result = 'Нічого не знайдено'
    model = kwargs.get('model')
    match model:
        case "Teacher":
            result = session.query(Teacher.fullname).select_from(Teacher).all()
        case "Group":
            result = session.query(Group.name).select_from(Group).all()
        case "Subject":
            result = session.query(Subject.name, Subject.teacher_id).select_from(Subject).all()
        case "Student":
            result = session.query(Student.fullname, Student.group_id).select_from(Student).all()
        case "Grade":
            result = session.query(Grade.grade, Grade.grade_date, Grade.student_id, Grade.subject_id)\
                .select_from(Grade).all()
    print(result)


@session_error
def update_record(**kwargs):
    model = kwargs.get('model')
    name = kwargs.get('name')
    record_id = kwargs.get('id')
    if not record_id:
        parser.error('--id is required for update operation')
    match model:
        case "Teacher":
            if not name:
                parser.error('--name and --id is required for update operation')
            teacher = session.query(Teacher).filter_by(id=int(record_id)).first()
            teacher.first_name, teacher.last_name = name.split()
            session.commit()
        case "Group":
            if not name:
                parser.error('--name and --id is required for update operation')
            group = session.query(Group).filter_by(id=int(record_id)).first()
            group.name = name
            session.commit()
        case "Subject":
            teacher_id = kwargs.get('teacher_id')
            subject = session.query(Subject).filter_by(id=int(record_id)).first()
            if name:
                subject.name = name
            if teacher_id:
                subject.teacher_id = int(teacher_id)
            session.commit()
        case "Student":
            group_id = kwargs.get('group_id')
            student = session.query(Student).filter_by(id=int(record_id)).first()
            if name:
                student.first_name, student.last_name = name.split()
            if group_id:
                student.group_id = int(group_id)
            session.commit()
        case "Grade":
            grade = kwargs.get('grade')
            if not grade:
                parser.error('--grade and --id is required for update operation')
            record_grade = session.query(Grade).filter_by(id=int(record_id)).first()
            record_grade.grade = int(grade)
            session.commit()


@session_error
def remove_record(**kwargs):
    model = kwargs.get('model')
    record_id = kwargs.get('id')
    if not record_id:
        parser.error('--id is required for remove operation')
    match model:
        case "Teacher":
            record = session.query(Teacher).filter_by(id=int(record_id)).first()
            session.delete(record)
        case "Group":
            record = session.query(Group).filter_by(id=int(record_id)).first()
            session.delete(record)
        case "Subject":
            record = session.query(Subject).filter_by(id=int(record_id)).first()
            session.delete(record)
        case "Student":
            record = session.query(Student).filter_by(id=int(record_id)).first()
            session.delete(record)
        case "Grade":
            record = session.query(Grade).filter_by(id=int(record_id)).first()
            session.delete(record)
    session.commit()


COMMANDS = {'create': create_record,  'list': list_records, 'update': update_record, 'remove': remove_record}


def get_handler(command):
    return COMMANDS.get(command)


if __name__ == '__main__':
    args = vars(parser.parse_args())
    # print(args)
    handler = get_handler(args.get('action'))
    handler(**args)
