from sqlalchemy import func, desc, select, and_

from conf.models import Teacher, Grade, Group, Student, Subject
from conf.db import session


def select_01():
    '''
    SELECT s.id, s.full_name, ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;
    :return:
    '''

    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return result


def select_02():
    '''
    SELECT s.id, s.full_name, ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    WHERE g.subject_id = 1
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;
    :return:
    '''

    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).lable('avg_grade'))