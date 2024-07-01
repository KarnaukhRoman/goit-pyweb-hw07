from sqlalchemy.sql import func, desc
from config.db_connection import session
from config.models import Group, Student, Grade, Subject, Professor


def select_1():  # 5 студентів із найбільшим середнім балом з усіх предметів
    grade_avg = session.query(Student.name, func.round(func.avg(Grade.score), 2).label('average'))\
                .select_from(Student)\
                .join(Grade)\
                .group_by(Student.name).order_by(desc('average')).limit(5).all()
    return grade_avg


def select_2(subj_id: int = 3):  # Студент із найвищим середнім балом з певного предмета(subject_id)
    grade_avg = session.query(Student.name, Subject.name_subject, func.round(func.avg(Grade.score), 2).label('average'))\
        .select_from(Student)\
        .join(Grade).join(Subject)\
        .filter(Subject.id == subj_id)\
        .group_by(Student.name, Subject.name_subject).order_by(desc('average')).limit(1).all()
    return grade_avg


def select_3(subj_id: int = 4):  # Середній бал у групах з певного предмета
    grade_avg = session.query(Group.name_group, Subject.name_subject, func.round(func.avg(Grade.score), 2).label('average'))\
        .select_from(Group)\
        .join(Student).join(Grade).join(Subject)\
        .filter(Subject.id == subj_id)\
        .group_by(Group.name_group, Subject.name_subject).order_by(desc('average')).all()
    return grade_avg


def select_4():  # середній бал на потоці (по всій таблиці оцінок)
    grade_avg = session.query(func.round(func.avg(Grade.score), 2).label('average')).all()
    return grade_avg


def select_5(id_prof: int = 3):  # які курси читає певний викладач.
    subjects = session.query(Subject.name_subject)\
        .join(Subject.professor).filter(Subject.prof_id == id_prof).all()
    return subjects


def select_6(id_group: int = 2):  # список студентів у певній групі
    students = session.query(Student.name, Group.name_group)\
        .join(Group).filter(Group.id == id_group).order_by(Student.name).all()
    return students


def select_7(id_group: int = 2, id_subject: int = 4):  # Оцінки студентів у окремій групі з певного предмета
    students = session.query(Student.name, Group.name_group, Grade.score, Subject.name_subject)\
        .join(Group).join(Grade).join(Subject)\
        .filter(Group.id == id_group, Subject.id == id_subject)\
        .order_by(Group.name_group, Student.name).all()
    return students


def select_8(id_prof: int = 3):  # Середній бал, який ставить певний викладач зі своїх предметів.
    subjects = session.query(Professor.name_prof, Subject.name_subject, func.round(func.avg(Grade.score), 2).label('average'))\
        .select_from(Professor)\
        .join(Subject).join(Grade)\
        .filter(Professor.id == id_prof).group_by(Professor.name_prof, Subject.name_subject).all()
    return subjects


def select_9(id_student: int = 13):  # Список курсів, які відвідує певний студент
    subjects = session.query(Student.name, Subject.name_subject)\
            .select_from(Student)\
            .join(Grade).join(Subject).filter(Student.id == id_student).all()
    return subjects


def select_10(id_student: int = 13, id_prof: int = 1):  # Список курсів, які певному студенту читає певний викладач
    subjects = session.query(Student.name, Subject.name_subject, Professor.name_prof)\
        .select_from(Student)\
        .join(Grade).join(Subject).join(Professor)\
        .filter(Student.id == id_student, Professor.id == id_prof).all()
    return subjects


def select_11(id_prof: int = 1, id_student: int = 13):  # Середній бал, який певний викладач ставить певному студентові
    grades_avg = session.query(func.round(func.avg(Grade.score), 2).label('average'))\
        .select_from(Grade)\
        .join(Student).join(Subject).join(Professor)\
        .filter(Student.id == id_student, Professor.id == id_prof).all()
    return grades_avg


def select_12(id_group: int = 1, id_subj: int = 8):  # Оцінки студентів у певній групі з певного предмета на останньому занятті
    # Підзапит для отримання останньої дати оцінки для предмета
    subquery = session.query(func.max(Grade.score_date).label('max_score_date'))\
               .join(Subject)\
               .filter(Subject.id == id_subj)\
               .scalar_subquery()
    # Основний запит
    results = session.query(Student.name.label('student_name'), Grade.score, Group.name_group)\
        .join(Grade, Grade.student_id == Student.id)\
        .join(Subject, Grade.subject_id == Subject.id)\
        .join(Group, Student.group_id == Group.id)\
        .filter(Group.id == id_group, Subject.id == id_subj, func.date(Grade.score_date) == subquery).all()

    return results


if __name__ == '__main__':
    print('5 студентів із найбільшим середнім балом з усіх предметів')
    print(select_1())
    print('Студент із найвищим середнім балом з певного предмета(subject_id)')
    print(select_2(4))
    print('Середній бал у групах з певного предмета(subject_id)')
    print(select_3(4))
    print('Середній бал на потоці (по всій таблиці оцінок)')
    print(select_4())
    print('Які курси читає певний викладач.')
    print(select_5(3))
    print('Список студентів у певній групі')
    print(select_6(2))
    print('Оцінки студентів у окремій групі з певного предмета')
    print(select_7(2, 4))
    print('Середній бал, який ставить певний викладач зі своїх предметів.')
    print(select_8(3))
    print('Список курсів, які відвідує певний студент')
    print(select_9(13))
    print('Список курсів, які певному студенту читає певний викладач')
    print(select_10(13, 1))
    print('Середній бал, який певний викладач ставить певному студентові')
    print(select_11())
    print('Оцінки студентів у певній групі з певного предмета на останньому занятті')
    print(select_12(1, 8))
