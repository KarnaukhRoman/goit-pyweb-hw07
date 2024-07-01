from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, SmallInteger, TIMESTAMP
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from config.db_connection import engine

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column('id', Integer, primary_key=True)
    name_group: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    student: Mapped[list['Student']] = relationship('Student', back_populates='group')


class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    group_id: Mapped[int] = mapped_column('group_id', Integer,
                                          ForeignKey('groups.id', ondelete='CASCADE', onupdate='CASCADE'))

    group: Mapped['Group'] = relationship('Group', back_populates='student')
    grade: Mapped['Grade'] = relationship('Grade', back_populates='student')


class Professor(Base):
    __tablename__ = 'professors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_prof: Mapped[str] = mapped_column(String(50), nullable=False)

    subject: Mapped['Subject'] = relationship('Subject', back_populates='professor')


class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_subject: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    prof_id: Mapped[int] = mapped_column('prof_id', Integer,
                                         ForeignKey('professors.id', ondelete='CASCADE', onupdate='CASCADE'))


    professor: Mapped['Professor'] = relationship('Professor', back_populates='subject')
    grade: Mapped['Grade'] = relationship('Grade', back_populates='subject')


class Grade(Base):
    __tablename__ = 'grades'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column('student_id', Integer,
                                            ForeignKey('students.id', ondelete='CASCADE', onupdate='CASCADE'))
    subject_id: Mapped[int] = mapped_column('subject_id', Integer,
                                            ForeignKey('subjects.id', ondelete='CASCADE', onupdate='CASCADE'))
    score: Mapped[SmallInteger] = mapped_column(SmallInteger, nullable=False)
    score_date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now(), nullable=False)

    # Relationships with Student and Subject models
    student: Mapped['Student'] = relationship('Student', back_populates='grade')
    subject: Mapped['Subject'] = relationship('Subject', back_populates='grade')

Base.metadata.create_all(engine)
