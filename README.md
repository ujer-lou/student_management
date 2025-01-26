# Student Management Application

## Overview

This application allows you to manage groups, students, and courses using a PostgreSQL database. It provides RESTful APIs to perform CRUD operations and manage relationships between entities.

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

    - **Create User and Database**

        ```bash
        psql -U postgres
        psql -f create_user_and_db.sql
        exit
        ```

    - **Create Tables**

        ```bash
        psql -U postgres
        psql -d student_management -f create_tables.sql
        exit
        ```

3. **Set Up the Python Environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables**

    - Create a `.env` file in the root directory (optional) and set the following variables:

        ```bash
        FLASK_APP=run.py
        FLASK_ENV=development
        SQLALCHEMY_DATABASE_URI=postgresql://appuser:app_password@localhost/student_management
        SECRET_KEY=your_secret_key
        ```

        **Important:**
        - Replace `appuser` and `app_password` with your actual PostgreSQL username and password.
        - Ensure there are **no typos** in the variable names. It should be `SQLALCHEMY_DATABASE_URI`, **not** `DATABASE_URL`.

5. **Generate Test Data**

    There are two methods to run the `generate_test_data.py` script:

    - **Method 1: Run as a Script**

        Ensure you're in the project root directory and your virtual environment is activated.

        ```bash
        python3 scripts/generate_test_data.py
        ```

        **Note:** If you encounter the `ModuleNotFoundError`, proceed to Method 2.

    - **Method 2: Run Manually**
         ```
         run the generate_test_data.py
         ```


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

Below are examples of how to interact with the API using **cURL**. Replace `<UUID>` with the actual UUID of the resource you are targeting.

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
      "courses": ["Course-123e4567-e89b-12d3-a456-426614174002"]
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
    "courses": ["Course-123e4567-e89b-12d3-a456-426614174002"]
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
  "courses": ["Course-123e4567-e89b-12d3-a456-426614174002"]
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

1. **Activate the Virtual Environment**

    ```bash
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2. **Navigate to the Tests Directory**

    ```bash
    cd student_management/tests
    ```

3. **Run the Test Suite**

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

## Additional Information

### Environment Variables

- **`SQLALCHEMY_DATABASE_URI`**: The connection string for the PostgreSQL database.
- **`SECRET_KEY`**: A secret key for securing sessions and other security-related needs.

### Logging

Comprehensive logging has been implemented to monitor application behavior and troubleshoot issues effectively. Logs capture important events, warnings, and errors.

### Marshmallow Integration

For advanced serialization and input validation, **Marshmallow** schemas have been integrated. This ensures that data adheres to defined structures and simplifies the conversion between Python objects and JSON.

### Security

While the current setup is suitable for development, consider implementing authentication and authorization mechanisms (e.g., JWT-based authentication) to secure your API endpoints in production environments.

### Continuous Integration (CI)

Integrate the test suite into a CI pipeline (e.g., GitHub Actions, GitLab CI/CD) to automate testing on code changes, ensuring ongoing reliability and preventing regressions.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or support, please contact [your.email@example.com](mailto:your.email@example.com).
```

---

**Additional Troubleshooting for `generate_test_data.py` Error**

If you continue to encounter the following error when running `generate_test_data.py`:

```
sqlalchemy.exc.ArgumentError: Expected string or URL object, got None
```

Please follow these steps to ensure your environment is correctly configured:

1. **Verify `.env` File Configuration**

   Ensure that your `.env` file is correctly set up in the root directory of your project (`student_management/`) and contains the following:

   ```bash
   SQLALCHEMY_DATABASE_URI=postgresql://appuser:app_password@localhost/student_management
   SECRET_KEY=your_secret_key
   ```

   **Note:**
   - Replace `appuser` and `app_password` with your actual PostgreSQL username and password.
   - Ensure there are no typos in the variable names.

2. **Confirm `config.py` Loads Environment Variables**

   Your `config.py` should correctly load the environment variables using `python-dotenv`. Here's an example:

   ```python
   # student_management/app/config.py

   import os
   from dotenv import load_dotenv

   # Load environment variables from .env file
   load_dotenv()

   class Config:
       SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
       SECRET_KEY = os.getenv("SECRET_KEY") or "default_secret_key"
       # Add other configuration variables as needed
   ```

3. **Ensure `python-dotenv` is Installed**

   Make sure `python-dotenv` is installed in your virtual environment:

   ```bash
   pip install python-dotenv
   ```

   Also, verify it's listed in your `requirements.txt`:

   ```bash
   echo "python-dotenv" >> requirements.txt
   ```

4. **Remove Temporary Debug Statements**

   If you added print statements for debugging in `config.py`, remove or comment them out after verification to prevent exposing sensitive information.

5. **Activate Virtual Environment and Navigate Correctly**

   Activate your virtual environment and navigate to the project root directory before running the script:

   ```bash
   source /home/bob/PycharmProjects/Foxtask10/.venv/bin/activate
   cd /home/bob/PycharmProjects/Foxtask10/student_management/
   ```

6. **Run the `generate_test_data.py` Script Again**

   ```bash
   python3 scripts/generate_test_data.py
   ```

   **Expected Outcome:**  
   The script should execute without errors, successfully connecting to your PostgreSQL database and generating the test data.

7. **Manual Environment Variable Setting (If Needed)**

   As a temporary workaround, you can manually set the environment variables in your shell before running the script:

   ```bash
   export SQLALCHEMY_DATABASE_URI=postgresql://appuser:app_password@localhost/student_management
   export SECRET_KEY=your_secret_key
   python3 scripts/generate_test_data.py
   ```

   **Note:** This approach bypasses the `.env` file and directly sets the environment variables for the current shell session.

8. **Verify Environment Variable Loading with a Test Script**

   Create a simple test script to confirm that environment variables are loaded correctly:

   ```python
   # test_env.py

   import os
   from dotenv import load_dotenv

   load_dotenv()

   print(f"SQLALCHEMY_DATABASE_URI: {os.getenv('SQLALCHEMY_DATABASE_URI')}")
   print(f"SECRET_KEY: {os.getenv('SECRET_KEY')}")
   ```

   Run the test script:

   ```bash
   python3 test_env.py
   ```

   **Expected Output:**

   ```
   SQLALCHEMY_DATABASE_URI: postgresql://appuser:app_password@localhost/student_management
   SECRET_KEY: your_secret_key
   ```

   If the output shows `None` for any variable, revisit the `.env` file and ensure it's correctly configured.

---

**Happy Coding!** 🚀
```