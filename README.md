# Student Management Application

## Overview

This application allows you to manage groups, students, and courses using a PostgreSQL database. It provides RESTful
APIs to perform CRUD operations and manage relationships between entities.

## Features

- **Groups:** Create, retrieve, update, and delete groups.
- **Students:** Create, retrieve, update, and delete students. Assign students to groups and courses.
- **Courses:** Create, retrieve, update, and delete courses.
- **Relationships:** Manage many-to-many relationships between students and courses.
- **Test Data:** Generate test data with scripts.
- **Testing:** Includes unit tests using `pytest`.

## Setup Instructions

### Prerequisites

- **Python 3.8+**
- **PostgreSQL**
- **Git** (optional, for version control)

### Steps

1. **Clone the Repository**

    ```bash
    git clone https://github.com/ujer-lou/student_management.git
    cd student_management
    ```

2. **Set Up the PostgreSQL Database**

    - **Method 1: Create User, Database and Tables (Not Recommended 🛑)**
        ```bash
        psql -U postgres
        psql -f create_user_and_db.sql
        psql -d student_management -f create_tables.sql
        exit
        ```

    - **Method 2: Using pgAdmin/Pycharm database (Recommended 🟢)**
        - 1 Connect to your postgres database
        - 2 Create new database
        - 3 Set name for database
        - 4 Make sure you can see that database is created
        - 5 If you can see database you are done


3. **Set Up the Python Environment**

    ```bash
    python3 -m venv .venv # if you already have venv activate it
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    pip install -r requirements.txt # Download requirements
    ```

4. **Configure Environment Variables**

    - Create a `.env` file in the root directory (optional) or in student_management and set the following variables:

        ```bash
        FLASK_APP=run.py
        FLASK_ENV=development
        SQLALCHEMY_DATABASE_URI=postgresql://appuser:app_password@localhost/database_name
        SECRET_KEY=your_secret_key # (Optional)
        ```

      **Important:**
        - Replace `appuser`, `app_password` and `database_name` with your actual PostgreSQL username, password and database name.

5. **Generate Test Data**

   There are two methods to run the `generate_test_data.py` script:

    - **Method 1: Run as a Script**

      Ensure you're in the project root directory and your virtual environment is activated.

        ```bash
        python3 scripts/generate_test_data.py
        ```

      **Note:** If you encounter the `ModuleNotFoundError`, proceed to Method 2.

    - **Method 2: Run Manually**
      
      - Run `generate_test_data` manually


6. **Run the Application**

    ```bash
    python3 run.py
    ```

7. **Run Tests**

    ```bash
    pytest
    ```

## API Endpoints

### **Groups**

- **GET** `/groups` - Retrieve all groups.
- **POST** `/groups` - Create a new group.
- **GET** `/groups/<group_id>/students` - Retrieve all students in a group.
- **GET** `/groups/with_max_students?max_count=<number>` - Retrieve groups with student count ≤ max_count.

### **Students**

- **GET** `/students` - Retrieve all students.
- **POST** `/students` - Create a new student.
- **GET** `/students/<student_id>` - Retrieve a specific student.
- **PUT** `/students/<student_id>` - Update a specific student.
- **DELETE** `/students/<student_id>` - Delete a specific student.
- **POST** `/students/<student_id>/courses/<course_id>` - Add a course to a student.
- **DELETE** `/students/<student_id>/courses/<course_id>` - Remove a course from a student.

### **Courses**

- **GET** `/courses` - Retrieve all courses.
- **POST** `/courses` - Create a new course.
- **GET** `/courses/<course_id>` - Retrieve a specific course.
- **PUT** `/courses/<course_id>` - Update a specific course.
- **DELETE** `/courses/<course_id>` - Delete a specific course.

## API Usage

Below are examples of how to interact with the API using **cURL**. Replace `<UUID>` with the actual UUID of the resource
you are targeting.

### **Groups**

#### **Create a New Group**

```bash
curl -X POST http://localhost:5000/groups \
     -H "Content-Type: application/json" \
     -d '{"name": "Group-123e4567-e89b-12d3-a456-426614174000"}'
```

**Response:**

```json
{
  "id": 1,
  "name": "Group-123e4567-e89b-12d3-a456-426614174000"
}
```

#### **Retrieve All Groups**

```bash
curl http://localhost:5000/groups
```

**Response:**

```json
[
  {
    "id": 1,
    "name": "Group-123e4567-e89b-12d3-a456-426614174000"
  },
  {
    "id": 2,
    "name": "Group-223e4567-e89b-12d3-a456-426614174001"
  }
]
```

#### **Retrieve Students in a Group**

```bash
curl http://localhost:5000/groups/1/students
```

**Response:**

```json
{
  "group_id": 1,
  "group_name": "Group-123e4567-e89b-12d3-a456-426614174000",
  "students": [
    {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "group_id": 1,
      "courses": [
        "Course-123e4567-e89b-12d3-a456-426614174002"
      ]
    }
  ]
}
```

#### **Retrieve Groups with Maximum Student Count**

```bash
curl http://localhost:5000/groups/with_max_students?max_count=10
```

**Response:**

```json
[
  {
    "id": 1,
    "name": "Group-123e4567-e89b-12d3-a456-426614174000",
    "student_count": 5
  },
  {
    "id": 2,
    "name": "Group-223e4567-e89b-12d3-a456-426614174001",
    "student_count": 8
  }
]
```

### **Students**

#### **Create a New Student**

```bash
curl -X POST http://localhost:5000/students \
     -H "Content-Type: application/json" \
     -d '{
           "first_name": "Jane",
           "last_name": "Smith",
           "group_id": 1
         }'
```

**Response:**

```json
{
  "id": 1,
  "first_name": "Jane",
  "last_name": "Smith",
  "group_id": 1
}
```

#### **Retrieve All Students**

```bash
curl http://localhost:5000/students
```

**Response:**

```json
[
  {
    "id": 1,
    "first_name": "Jane",
    "last_name": "Smith",
    "group_id": 1,
    "courses": [
      "Course-123e4567-e89b-12d3-a456-426614174002"
    ]
  },
  {
    "id": 2,
    "first_name": "Emily",
    "last_name": "Johnson",
    "group_id": 2,
    "courses": []
  }
]
```

#### **Retrieve a Specific Student**

```bash
curl http://localhost:5000/students/1
```

**Response:**

```json
{
  "id": 1,
  "first_name": "Jane",
  "last_name": "Smith",
  "group_id": 1,
  "courses": [
    "Course-123e4567-e89b-12d3-a456-426614174002"
  ]
}
```

#### **Update a Specific Student**

```bash
curl -X PUT http://localhost:5000/students/1 \
     -H "Content-Type: application/json" \
     -d '{
           "first_name": "Janet",
           "last_name": "Doe",
           "group_id": 2
         }'
```

**Response:**

```json
{
  "message": "Student updated successfully"
}
```

#### **Delete a Specific Student**

```bash
curl -X DELETE http://localhost:5000/students/1
```

**Response:**

```json
{
  "message": "Student deleted successfully"
}
```

#### **Add a Course to a Student**

```bash
curl -X POST http://localhost:5000/students/1/courses/1
```

**Response:**

```json
{
  "message": "Course added to student"
}
```

#### **Remove a Course from a Student**

```bash
curl -X DELETE http://localhost:5000/students/1/courses/1
```

**Response:**

```json
{
  "message": "Course removed from student"
}
```

### **Courses**

#### **Create a New Course**

```bash
curl -X POST http://localhost:5000/courses \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Course-123e4567-e89b-12d3-a456-426614174002",
           "description": "Introduction to Testing"
         }'
```

**Response:**

```json
{
  "id": 1,
  "name": "Course-123e4567-e89b-12d3-a456-426614174002",
  "description": "Introduction to Testing"
}
```

#### **Retrieve All Courses**

```bash
curl http://localhost:5000/courses
```

**Response:**

```json
[
  {
    "id": 1,
    "name": "Course-123e4567-e89b-12d3-a456-426614174002",
    "description": "Introduction to Testing"
  },
  {
    "id": 2,
    "name": "Course-223e4567-e89b-12d3-a456-426614174003",
    "description": "Advanced Python"
  }
]
```

#### **Retrieve a Specific Course**

```bash
curl http://localhost:5000/courses/1
```

**Response:**

```json
{
  "id": 1,
  "name": "Course-123e4567-e89b-12d3-a456-426614174002",
  "description": "Introduction to Testing"
}
```

#### **Update a Specific Course**

```bash
curl -X PUT http://localhost:5000/courses/1 \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Course-123e4567-e89b-12d3-a456-426614174002",
           "description": "Advanced Testing Techniques"
         }'
```

**Response:**

```json
{
  "message": "Course updated successfully"
}
```

#### **Delete a Specific Course**

```bash
curl -X DELETE http://localhost:5000/courses/1
```

**Response:**

```json
{
  "message": "Course deleted successfully"
}
```

## Testing

The application includes a comprehensive test suite using `pytest` to ensure all API endpoints function as expected.

### Running Tests

1. **Navigate to the Tests Directory**

    ```bash
    cd student_management/tests
    ```

2. **Run the Test Suite**

    ```bash
    pytest test_api.py -v
    ```

### Sample Test Output

```bash
============================= test session starts ==============================
platform linux -- Python 3.11.11, pytest-8.3.4, pluggy-1.5.0
cachedir: .pytest_cache
rootdir: /home/bob/PycharmProjects/Foxtask10/student_management/tests
plugins: Faker-35.0.0
collected 16 items

test_api.py::test_create_group PASSED                                    [  6%]
test_api.py::test_get_groups PASSED                                      [ 12%]
test_api.py::test_get_group_students PASSED                              [ 18%]
test_api.py::test_get_groups_with_max_students PASSED                    [ 25%]
test_api.py::test_create_student PASSED                                  [ 31%]
test_api.py::test_get_students PASSED                                    [ 37%]
test_api.py::test_get_student_details PASSED                             [ 43%]
test_api.py::test_update_student PASSED                                  [ 50%]
test_api.py::test_add_student_to_course PASSED                           [ 56%]
test_api.py::test_remove_student_from_course PASSED                      [ 62%]
test_api.py::test_create_course PASSED                                   [ 68%]
test_api.py::test_get_courses PASSED                                     [ 75%]
test_api.py::test_get_course_details PASSED                              [ 81%]
test_api.py::test_update_course PASSED                                   [ 87%]
test_api.py::test_delete_course PASSED                                   [ 93%]
test_api.py::test_get_students_by_course_name PASSED                     [100%]

============================== 16 passed in 0.78s ===============================
```