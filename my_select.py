from sqlalchemy import func, desc, and_

from conf.models import Teacher, Grade, Group, Student, Subject
from conf.db import session


def select_1():
    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів
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


def select_2():
    # Знайти студента із найвищим середнім балом з певного предмета
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


def select_3():
    # Знайти середній бал у групах з певного предмета
    """
    SELECT groups.name AS GroupName, ROUND(AVG(g.grade), 2) AS AverageGrade
    FROM grades g
    JOIN students s ON g.student_id = s.id
    JOIN groups ON s.group_id = groups.id
    WHERE g.subject_id = 1
    GROUP by groups.name
    ORDER by groups.name;
    """
    result = session.query(Group.name.label('GroupName'), func.round(func.avg(Grade.grade), 2).label('AverageGrade')) \
        .select_from(Grade).join(Student).join(Group).filter(Grade.subject_id == 1).group_by(Group.name).order_by(
        Group.name).all()
    return result


def select_4():
    # Знайти середній бал на потоці (по всій таблиці оцінок)
    """
    SELECT ROUND(AVG(grade), 2) AS AverageGrade
    FROM grades;
    """
    result = session.query(func.round(func.avg(Grade.grade), 2).label('AverageGrade')).select_from(Grade).all()
    return result


def select_5():
    # Знайти які курси читає певний викладач
    """
    SELECT t.first_name || ' ' || t.last_name AS fullname, subjects.name AS CourseName
    FROM teachers t
    JOIN subjects ON t.id = subjects.teacher_id
    WHERE t.id = 1
    ORDER BY fullname, CourseName;
    """
    result = session.query(Teacher.fullname, Subject.name.label('CourseName')).select_from(Teacher).join(Subject) \
        .filter(Teacher.id == 1).order_by(Teacher.fullname, 'CourseName').all()
    return result


def select_6():
    # Знайти список студентів у певній групі
    """
    SELECT s.first_name|| ' ' || s.last_name AS fullname
    FROM groups g
    JOIN students s ON g.id = s.group_id
    WHERE g.id = 2
    ORDER BY fullname;
    """
    result = session.query(Student.fullname).select_from(Group).join(Student).filter(Group.id == 2).order_by(
        Student.fullname).all()
    return result


def select_7():
    # Знайти оцінки студентів у окремій групі з певного предмета.
    """
    SELECT s.first_name|| ' ' || s.last_name AS StudentName, grades.grade AS Grade, subjects.name AS SubjectName
    FROM students s
    JOIN grades ON s.id = grades.student_id
    JOIN subjects ON grades.subject_id = subjects.id
    JOIN groups ON s.group_id = groups.id
    WHERE groups.id  = 1 AND subjects.id  = 1
    ORDER by StudentName;
    """
    result = session.query(
        Student.fullname.label('StudentName'), Grade.grade.label('Grade'), Subject.name.label('SubjectName')) \
        .select_from(Student).join(Grade).join(Subject).join(Group).filter(and_(Group.id == 1, Subject.id == 1)) \
        .order_by('StudentName').all()
    return result


def select_8():
    # Знайти середній бал, який ставить певний викладач зі своїх предметів
    """
    SELECT t.first_name || ' ' || t.last_name AS TeacherName, subjects.name AS SubjectName, ROUND(AVG(grades.grade), 2)
    AS AverageGrade
    FROM teachers t
    JOIN subjects ON t.id = subjects.teacher_id
    JOIN grades ON subjects.id = grades.subject_id
    JOIN students ON grades.student_id = students.id
    WHERE t.id = 1
    GROUP by TeacherName, SubjectName
    ORDER by TeacherName, SubjectName;
    """
    result = (session.query(
        Teacher.fullname.label('TeacherName'), Subject.name.label('SubjectName'), func.round(func.avg(Grade.grade), 2)
        .label('AverageGrade')).select_from(Teacher).join(Subject).join(Grade).join(Student).filter(Teacher.id == 1)
              .group_by("TeacherName", "SubjectName").order_by("TeacherName", "SubjectName").all())
    return result


def select_9():
    # Знайти список курсів, які відвідує певний студент
    """
    SELECT DISTINCT s.first_name|| ' ' || s.last_name AS StudentName, subjects.name AS CourseName
    FROM students s
    JOIN grades ON s.id = grades.student_id
    JOIN subjects ON grades.subject_id = subjects.id
    WHERE s.id = 1
    ORDER BY CourseName;
    """
    result = session.query(Student.fullname.label('StudentName'), Subject.name.label('CourseName')) \
        .select_from(Student).join(Grade).join(Subject).filter(Student.id == 1).distinct().order_by("CourseName").all()
    return result


def select_10():
    # Список курсів, які певному студенту читає певний викладач
    """
    SELECT DISTINCT subjects.name AS CourseName
    FROM students s
    JOIN grades ON s.id = grades.student_id
    JOIN subjects ON grades.subject_id = subjects.id
    JOIN teachers ON subjects.teacher_id = teachers.id
    WHERE s.id = 1 AND teachers.id = 1
    ORDER BY CourseName;
    """
    result = session.query(Subject.name.label("CourseName")).select_from(Student).join(Grade).join(Subject) \
        .join(Teacher).filter(and_(Student.id == 1, Teacher.id == 1)).distinct().order_by("CourseName").all()
    return result


if __name__ == '__main__':
    print(select_1())
    print(select_2())
    print(select_3())
    print(select_4())
    print(select_5())
    print(select_6())
    print(select_7())
    print(select_8())
    print(select_9())
    print(select_10())
