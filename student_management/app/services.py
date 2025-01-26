from sqlalchemy.orm import joinedload

from .models import Group, Student, Course



def add_new_student(session, first_name, last_name, group_id=None):
    """
    Adds a new student to the database.
    """
    student = Student(first_name=first_name, last_name=last_name, group_id=group_id)
    session.add(student)
    session.commit()
    return student

def delete_student_by_id(session, student_id):
    """
    Deletes a student by ID.
    Returns True if deletion was successful, False otherwise.
    """
    student = session.query(Student).filter(Student.id == student_id).first()
    if not student:
        return False
    session.delete(student)
    session.commit()
    return True

def add_student_to_course(session, student_id, course_id):
    """
    Enrolls a student in a course.
    Returns True if successful, False otherwise.
    """
    student = session.query(Student).filter(Student.id == student_id).first()
    course = session.query(Course).filter(Course.id == course_id).first()
    if not student or not course:
        return False
    if course in student.courses:
        # Already enrolled
        return False
    student.courses.append(course)
    session.commit()
    return True

def remove_student_from_course(session, student_id, course_id):
    """
    Removes a student from a course.
    Returns True if successful, False otherwise.
    """
    student = session.query(Student).filter(Student.id == student_id).first()
    course = session.query(Course).filter(Course.id == course_id).first()
    if not student or not course:
        return False
    if course not in student.courses:
        # Not enrolled in the course
        return False
    student.courses.remove(course)
    session.commit()
    return True

def get_students_by_course_name(session, course_name):
    """
    Retrieves all students enrolled in a course by course name.
    """
    course = session.query(Course).filter(Course.name == course_name).first()
    if not course:
        return []
    return course.students

def get_groups_with_student_count(session, max_count):
    """
    Retrieves all groups with a student count less than or equal to max_count.
    """
    groups = session.query(Group).options(joinedload(Group.students)).all()
    filtered_groups = [group for group in groups if len(group.students) <= max_count]
    return filtered_groups
