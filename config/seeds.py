from datetime import datetime, date, time
import faker
import random
from random import randint

from db_connection import session
from models import Group, Student, Professor, Subject, Grade

NUMBER_GROUPS = 3
NUMBER_PROFESSORS = 8
NUMBER_SUBJECTS = 8
NUMBER_STUDENTS = 50
NUMBER_SCORES = 100


def generate_fake_data(num_groups, num_students, num_professors, num_subjects, num_scores) -> tuple():
    fake_data = faker.Faker("uk_UA")
    fake_data2 = faker.Faker()
    fake_groups = [
        f"{random.choice(['IT', 'PyWeb', 'ME', 'CEO', 'BIO', 'CHE'])}-{random.randint(20, 28)}-{fake_data2.word().capitalize()}"
        for _ in range(num_groups)
    ]
    fake_students = [fake_data.name() for _ in range(num_students)]
    fake_professors = [fake_data.name() for _ in range(num_professors)]
    fake_subject = [fake_data2.job() for _ in range(num_subjects)]
    fake_scores = [
        (randint(1, NUMBER_STUDENTS),
         randint(1, NUMBER_SUBJECTS),
         randint(3, 12),
         datetime.combine(
             fake_data.date_between(date(2020, 9, 1), date(2024, 5, 31)),
             time(randint(9, 16), randint(0, 59), randint(0, 59))
         ))
        for _ in range(num_scores)
    ]

    return fake_groups, fake_students, fake_professors, fake_subject, fake_scores


def prepare_data(groups, students, professors, subjects, scores) -> tuple():
    for_groups = [(group,) for group in groups]
    for_students = [(student, randint(1, NUMBER_GROUPS)) for student in students]
    for_professors = [(professor,) for professor in professors]
    for_subjects = [(subject, randint(1, NUMBER_PROFESSORS)) for subject in subjects]
    for_scores = scores

    return for_groups, for_students, for_professors, for_subjects, for_scores


def insert_data_to_db(groups, students, professors, subjects, grades) -> None:
    # Створимо з'єднання з нашою БД та отримаємо об'єкт курсору для маніпуляцій з даними
    try:
        for group in groups:
            table_group = Group(name_group=group[0])
            session.add(table_group)

        for student in students:
            table_student = Student(name=student[0], group_id=student[1])
            session.add(table_student)

        for professor in professors:
            table_professor = Professor(name_prof=professor[0])
            session.add(table_professor)

        for subject in subjects:
            table_subject = Subject(name_subject=subject[0], prof_id=subject[1])
            session.add(table_subject)

        for grade in grades:
            table_grade = Grade(student_id=grade[0], subject_id=grade[1], score=grade[2], score_date=grade[3])
            session.add(table_grade)

        session.commit()

    except Exception as err:
        print(err)
        session.rollback()




if __name__ == "__main__":
    groups, students, professors, subjects, grades = prepare_data(*generate_fake_data(NUMBER_GROUPS, NUMBER_STUDENTS, NUMBER_PROFESSORS, NUMBER_SUBJECTS, NUMBER_SCORES))
    insert_data_to_db(groups, students, professors, subjects, grades)
    print(groups,'\n', students,'\n',professors,'\n',subjects,'\n',grades,'\n')
