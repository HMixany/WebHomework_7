from sqlalchemy import func, desc, select, and_

from conf.models import Teacher, Grade, Group, Student, Subject
from conf.db import session


def select_01():
    """
    SELECT s.id, s.first_name|| ' ' || s.last_name AS fullname, ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;
    """

    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result


def select_02():
    """
    SELECT s.id, s.first_name|| ' ' || s.last_name AS fullname, ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    WHERE g.subject_id = 1
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;
    """

    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subject_id == 1).group_by(Student.id).order_by(
        desc('average_grade')).limit(1).all()
    return result


def select_03():
    """
    SELECT groups.name AS GroupName, ROUND(AVG(g.grade), 2) AS AverageGrade
    FROM grades g
    JOIN students s ON g.student_id = s.id
    JOIN groups ON s.group_id = groups.id
    WHERE g.subject_id = 1
    GROUP by groups.name
    ORDER by groups.name;
    """
    result = session.query(Group.name.label('GroupName'), func.round(func.avg(Grade.grade), 2).label('AverageGrade'))\
        .select_from(Grade).join(Student).join(Group).filter(Grade.subject_id == 1).group_by(Group.name).order_by(
        Group.name).all()
    return result


def select_04():
    """
    SELECT ROUND(AVG(grade), 2) AS AverageGrade
    FROM grades;
    """
    result = session.query(func.round(func.avg(Grade.grade), 2).label('AverageGrade')).select_from(Grade).all()
    return result


def select_05():
    """
    SELECT first_name || ' ' || last_name AS TeacherName, subjects.name AS CourseName
    FROM teachers t
    JOIN subjects ON t.id = subjects.teacher_id
    WHERE t.id = 1
    ORDER BY TeacherName, CourseName;
    """
    result = session.query(Teacher.fullname, Subject.name.label('CourseName')).select_from(Teacher).join(Subject)\
        .filter(Teacher.id == 1).order_by(Teacher.fullname, 'CourseName').all()
    return result


def select_n():
    result = session.query(Group.id, Group.name).all()
    return result


if __name__ == '__main__':
    print(select_05())

