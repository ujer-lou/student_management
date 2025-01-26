import random
import string

from faker import Faker

from app.database import SessionLocal, engine
from app.models import Base, Group, Student, Course

fake = Faker()

def generate_group_name():
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = ''.join(random.choices(string.digits, k=2))
    return f"{letters}-{numbers}"

def generate_test_data():
    session = SessionLocal()

    try:
        group_names = set()
        while len(group_names) < 10:
            name = generate_group_name()
            group_names.add(name)

        groups = [Group(name=name) for name in group_names]
        session.add_all(groups)
        session.commit()
        print("10 groups created.")
        course_names = ['Mathematics', 'Biology', 'Chemistry', 'Physics', 'History',
                       'Geography', 'Literature', 'Art', 'Computer Science', 'Philosophy']
        courses = [Course(name=name, description=fake.text(max_nb_chars=200)) for name in course_names]
        session.add_all(courses)
        session.commit()
        print("10 courses created.")
        first_names = [fake.first_name() for _ in range(20)]
        last_names = [fake.last_name() for _ in range(20)]

        students = []
        for _ in range(200):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            group = random.choice(groups + [None])  # Some students without groups
            student = Student(first_name=first_name, last_name=last_name, group=group)
            students.append(student)

        session.add_all(students)
        session.commit()
        print("200 students created.")
        all_courses = session.query(Course).all()
        for student in students:
            num_courses = random.randint(1, 3)
            student.courses = random.sample(all_courses, num_courses)
        session.commit()
        print("Courses assigned to students.")

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    generate_test_data()
