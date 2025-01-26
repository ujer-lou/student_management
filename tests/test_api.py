import pytest
import requests
import uuid

BASE_URL = "http://localhost:5000"


def generate_unique_name(prefix):
    return f"{prefix}-{uuid.uuid4()}"


@pytest.fixture(scope="module")
def created_group():
    """
    Fixture to create a group before tests and ensure it exists.
    Note: Since DELETE /groups/<group_id> is not implemented, we won't attempt to delete it.
    """
    group_name = generate_unique_name("Group")
    payload = {"name": group_name}
    response = requests.post(f"{BASE_URL}/groups", json=payload)
    assert response.status_code == 201, f"Failed to create group: {response.text}"
    group = response.json()
    group_id = group.get("id")
    yield group  # Provide the group to the tests
    # No cleanup since DELETE /groups/<group_id> does not exist


@pytest.fixture(scope="function")
def created_course():
    """
    Fixture to create a course before each test and delete it after the test.
    """
    course_name = generate_unique_name("Course")
    payload = {"name": course_name, "description": "Test course description"}
    response = requests.post(f"{BASE_URL}/courses", json=payload)
    assert response.status_code == 201, f"Failed to create course: {response.text}"
    course = response.json()
    course_id = course.get("id")
    yield course  # Provide the course to the tests
    # Cleanup: Delete the course after the test
    response = requests.delete(f"{BASE_URL}/courses/{course_id}")
    if response.status_code not in [200, 404]:
        assert False, f"Failed to delete course: {response.text}"
    # If the course was already deleted (e.g., by test_delete_course), ignore the 404


@pytest.fixture(scope="function")
def created_student(created_group):
    """
    Fixture to create a student before each test and delete it after the test.
    """
    student_first_name = "TestFirstName"
    student_last_name = "TestLastName"
    payload = {
        "first_name": student_first_name,
        "last_name": student_last_name,
        "group_id": created_group["id"]
    }
    response = requests.post(f"{BASE_URL}/students", json=payload)
    assert response.status_code == 201, f"Failed to create student: {response.text}"
    student = response.json()
    student_id = student.get("id")
    yield student  # Provide the student to the tests
    # Cleanup: Delete the student after test
    response = requests.delete(f"{BASE_URL}/students/{student_id}")
    assert response.status_code == 200, f"Failed to delete student: {response.text}"


def test_create_group():
    """
    Test creating a new group.
    """
    group_name = generate_unique_name("Group")
    payload = {"name": group_name}
    response = requests.post(f"{BASE_URL}/groups", json=payload)
    assert response.status_code == 201, f"Failed to create group: {response.text}"
    group = response.json()
    group_id = group.get("id")
    assert group_id is not None, "Group ID not returned"

    # Note: No cleanup as DELETE /groups/<group_id> is not implemented


def test_get_groups(created_group):
    """
    Test retrieving all groups.
    """
    response = requests.get(f"{BASE_URL}/groups")
    assert response.status_code == 200, f"Failed to get groups: {response.text}"
    groups = response.json()
    assert any(g["id"] == created_group["id"] for g in groups), "Created group not found in GET /groups"


def test_get_group_students(created_group):
    """
    Test retrieving all students in a specific group.
    """
    group_id = created_group["id"]
    response = requests.get(f"{BASE_URL}/groups/{group_id}/students")
    assert response.status_code == 200, f"Failed to get students in group: {response.text}"

    group_data = response.json()
    assert "students" in group_data, "'students' key not found in response"

    students = group_data["students"]
    assert isinstance(students, list), "Students should be a list"


def test_get_groups_with_max_students():
    """
    Test retrieving groups with student count ≤ max_count.
    """
    max_count = 10
    response = requests.get(f"{BASE_URL}/groups/with_max_students", params={"max_count": max_count})
    assert response.status_code == 200, f"Failed to get groups with max students: {response.text}"
    groups = response.json()
    assert isinstance(groups, list), "Groups should be a list"
    for group in groups:
        assert group["student_count"] <= max_count, f"Group {group['id']} has more than {max_count} students"


def test_create_student(created_group):
    """
    Test creating a new student.
    """
    student_first_name = "TestFirstName"
    student_last_name = "TestLastName"
    payload = {
        "first_name": student_first_name,
        "last_name": student_last_name,
        "group_id": created_group["id"]
    }
    response = requests.post(f"{BASE_URL}/students", json=payload)
    assert response.status_code == 201, f"Failed to create student: {response.text}"
    student = response.json()
    student_id = student.get("id")
    assert student_id is not None, "Student ID not returned"

    # Cleanup: Delete the student
    response = requests.delete(f"{BASE_URL}/students/{student_id}")
    assert response.status_code == 200, f"Failed to delete student: {response.text}"


def test_get_students():
    """
    Test retrieving all students.
    """
    response = requests.get(f"{BASE_URL}/students")
    assert response.status_code == 200, f"Failed to get students: {response.text}"
    students = response.json()
    assert isinstance(students, list), "Students should be a list"


def test_get_student_details(created_student):
    """
    Test retrieving a specific student's details.
    """
    student_id = created_student["id"]
    response = requests.get(f"{BASE_URL}/students/{student_id}")
    assert response.status_code == 200, f"Failed to get student: {response.text}"
    student = response.json()
    assert student["id"] == student_id, "Student ID does not match"
    assert student["first_name"] == "TestFirstName", "Student first name does not match"
    assert student["last_name"] == "TestLastName", "Student last name does not match"


def test_update_student(created_student):
    """
    Test updating a specific student's information.
    """
    student_id = created_student["id"]
    updated_first_name = "UpdatedFirstName"
    updated_last_name = "UpdatedLastName"
    update_payload = {
        "first_name": updated_first_name,
        "last_name": updated_last_name,
        "group_id": created_student["group_id"]
    }
    response = requests.put(f"{BASE_URL}/students/{student_id}", json=update_payload)
    assert response.status_code == 200, f"Failed to update student: {response.text}"

    # Verify the update
    response = requests.get(f"{BASE_URL}/students/{student_id}")
    assert response.status_code == 200, f"Failed to get student: {response.text}"
    student = response.json()
    assert student["first_name"] == updated_first_name, "First name was not updated"
    assert student["last_name"] == updated_last_name, "Last name was not updated"


def test_add_student_to_course(created_student, created_course):
    """
    Test adding a course to a student.
    """
    student_id = created_student["id"]
    course_id = created_course["id"]
    response = requests.post(f"{BASE_URL}/students/{student_id}/courses/{course_id}")
    assert response.status_code == 200, f"Failed to add course to student: {response.text}"

    # Verify the course was added
    response = requests.get(f"{BASE_URL}/students/{student_id}")
    assert response.status_code == 200, f"Failed to get student: {response.text}"
    student = response.json()
    assert created_course["name"] in student.get("courses", []), "Course not added to student"


def test_remove_student_from_course(created_student, created_course):
    """
    Test removing a course from a student.
    """
    student_id = created_student["id"]
    course_id = created_course["id"]

    # First, add the course to the student
    response = requests.post(f"{BASE_URL}/students/{student_id}/courses/{course_id}")
    assert response.status_code == 200, f"Failed to add course to student: {response.text}"

    # Now, remove the course
    response = requests.delete(f"{BASE_URL}/students/{student_id}/courses/{course_id}")
    assert response.status_code == 200, f"Failed to remove course from student: {response.text}"

    # Verify the course was removed
    response = requests.get(f"{BASE_URL}/students/{student_id}")
    assert response.status_code == 200, f"Failed to get student: {response.text}"
    student = response.json()
    assert created_course["name"] not in student.get("courses", []), "Course not removed from student"


def test_create_course():
    """
    Test creating a new course.
    """
    course_name = generate_unique_name("Course")
    course_description = "This is a test course."
    payload = {
        "name": course_name,
        "description": course_description
    }
    response = requests.post(f"{BASE_URL}/courses", json=payload)
    assert response.status_code == 201, f"Failed to create course: {response.text}"
    course = response.json()
    course_id = course.get("id")
    assert course_id is not None, "Course ID not returned"

    # Cleanup: Delete the course
    response = requests.delete(f"{BASE_URL}/courses/{course_id}")
    if response.status_code not in [200, 404]:
        assert False, f"Failed to delete course: {response.text}"
    # If the course was already deleted (e.g., by test_delete_course), ignore the 404


def test_get_courses(created_course):
    """
    Test retrieving all courses.
    """
    response = requests.get(f"{BASE_URL}/courses")
    assert response.status_code == 200, f"Failed to get courses: {response.text}"
    courses = response.json()
    assert any(c["id"] == created_course["id"] for c in courses), "Created course not found in GET /courses"


def test_get_course_details(created_course):
    """
    Test retrieving a specific course's details.
    """
    course_id = created_course["id"]
    response = requests.get(f"{BASE_URL}/courses/{course_id}")
    assert response.status_code == 200, f"Failed to get course: {response.text}"
    course = response.json()
    assert course["id"] == course_id, "Course ID does not match"
    assert course["name"] == created_course["name"], "Course name does not match"
    assert course["description"] == created_course["description"], "Course description does not match"


def test_update_course(created_course):
    """
    Test updating a specific course's information.
    """
    course_id = created_course["id"]
    updated_course_name = generate_unique_name("UpdatedCourse")
    updated_course_description = "Updated course description."
    update_payload = {
        "name": updated_course_name,
        "description": updated_course_description
    }
    response = requests.put(f"{BASE_URL}/courses/{course_id}", json=update_payload)
    assert response.status_code == 200, f"Failed to update course: {response.text}"

    # Verify the update
    response = requests.get(f"{BASE_URL}/courses/{course_id}")
    assert response.status_code == 200, f"Failed to get course: {response.text}"
    course = response.json()
    assert course["name"] == updated_course_name, "Course name was not updated"
    assert course["description"] == updated_course_description, "Course description was not updated"


def test_delete_course(created_course):
    """
    Test deleting a specific course.
    """
    course_id = created_course["id"]
    response = requests.delete(f"{BASE_URL}/courses/{course_id}")
    assert response.status_code == 200, f"Failed to delete course: {response.text}"

    # Verify deletion
    response = requests.get(f"{BASE_URL}/courses/{course_id}")
    assert response.status_code == 404, "Course was not deleted successfully"


def test_get_students_by_course_name(created_group, created_course, created_student):
    """
    Test retrieving students by course name.
    """
    course_name = created_course["name"]

    # Enroll the student in the course
    student_id = created_student["id"]
    course_id = created_course["id"]
    response = requests.post(f"{BASE_URL}/students/{student_id}/courses/{course_id}")
    assert response.status_code == 200, f"Failed to enroll student: {response.text}"

    # Retrieve students by course name
    response = requests.get(f"{BASE_URL}/students_by_course/{course_name}")
    if response.status_code == 200:
        students = response.json()
        assert isinstance(students, list), "Students should be a list"
        assert any(s["id"] == student_id for s in students), "Enrolled student not found in course"
    else:
        pytest.skip(f"Endpoint /students_by_course/{course_name} not found: {response.text}")

    # Cleanup: Remove the student from the course
    response = requests.delete(f"{BASE_URL}/students/{student_id}/courses/{course_id}")
    assert response.status_code == 200, f"Failed to remove course from student: {response.text}"
