from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)

    subjects = relationship('Subject', back_populates='teacher')

    # student = relationship('Student', back_populates='teacher')

    # створемо гібридне(віртуальне) поле
    @hybrid_property
    def fullname(self):
        return self.first_name + ' ' + self.last_name


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    students = relationship('Student', back_populates='group')


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    group_id = Column('group_id', ForeignKey('groups_id', ondelete='CASCADE'))
    group = relationship('Group', back_populates='students')

    grade = relationship('Grade', back_populates='student')

    # student = relationship('Student', secondary='teachers_to_students', back_populates='teacher')

    # створемо гібридне(віртуальне) поле
    @hybrid_property
    def fullname(self):
        return self.first_name + ' ' + self.last_name


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    teacher_id = Column('teacher_id', ForeignKey('teachers_id', ondelete='CASCADE'))
    teacher = relationship('Teacher', back_populates='subjects')
    grade = relationship('Grade', back_populates='subject')


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    grade_date = Column('grade_date', Date, nullable=True)
    student_id = Column('student_id', ForeignKey('students_id', ondelete='CASCADE'))
    subject_id = Column('subject_id', ForeignKey('subjects_id', ondelete='CASCADE'))
    student = relationship('Student', back_populates='grade')
    subject = relationship('Subject', back_populates='grade')