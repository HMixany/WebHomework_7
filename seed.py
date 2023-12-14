import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from conf.db import session
from conf.models import Teacher, Group, Student, Subject, Grade

fake = Faker('uk-UA')


# Додавання груп
def insert_groups():
    for _ in range(3):
        group = Group(name=fake.word())
        session.add(group)


# Додавання викладачів
def insert_teachers():
    for _ in range(4):
        teacher = Teacher(
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        session.add(teacher)


# Додавання предметів із вказівкою викладача
def insert_subjects():
    for teacher_id in range(1, 5):
        for _ in range(2):
            subject = Subject(
                name=fake.word(),
                teacher_id=teacher_id
            )
            session.add(subject)


# додавання студентів із вказівкою групи
def insert_students():
    for group_id in range(1, 4):
        for _ in range(15):
            student = Student(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                group_id=group_id
            )
            session.add(student)


# Додавання оцінок із вказівкою студента, предмета та дати
def insert_grades():
    for student_id in range(1, 46):
        for subject_id in range(1, 9):
            for _ in range(3):
                grade_data = Grade(
                    grade=random.randint(0, 100),
                    grade_date=fake.date_this_decade(),
                    student_id=student_id,
                    subject_id=subject_id
                )
                session.add(grade_data)


def remove_student(s_id):
    student = session.query(Student).filter_by(id=s_id).first()
    session.delete(student)
    session.commit()


if __name__ == '__main__':
    try:
        insert_groups()
        insert_teachers()
        session.commit()
        insert_subjects()
        insert_students()
        session.commit()
        insert_grades()
        session.commit()
    except SQLAlchemyError as err:
        print(err)
        session.rollback()
    finally:
        session.close()