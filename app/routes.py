# app/routes.py

from flask_restful import Resource, Api, reqparse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from flask import abort
from .database import SessionLocal
from .models import Group, Student, Course
from .services import (
    get_groups_with_student_count,
    get_students_by_course_name,
    add_new_student,
    delete_student_by_id,
    add_student_to_course,
    remove_student_from_course
)


def initialize_routes(api: Api):
    """
    Registers all the resource routes with the Flask-RESTful API.
    """
    api.add_resource(GroupListResource, '/groups')
    api.add_resource(StudentListResource, '/students')
    api.add_resource(StudentResource, '/students/<int:student_id>')
    api.add_resource(CourseListResource, '/courses')
    api.add_resource(CourseResource, '/courses/<int:course_id>')
    api.add_resource(StudentCourseResource, '/students/<int:student_id>/courses/<int:course_id>')
    api.add_resource(GroupStudentsResource, '/groups/<int:group_id>/students')
    api.add_resource(GroupWithMaxStudentsResource, '/groups/with_max_students')
    api.add_resource(StudentsByCourseResource, '/students_by_course/<string:course_name>')  # Newly Added


class GroupListResource(Resource):
    """
    Resource for handling operations on the collection of groups.
    """
    def get(self):
        session = SessionLocal()
        try:
            groups = session.query(Group).all()
            return [{'id': g.id, 'name': g.name} for g in groups], 200
        finally:
            session.close()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Group name is required')
        args = parser.parse_args()

        session = SessionLocal()
        try:
            group = Group(name=args['name'])
            session.add(group)
            session.commit()
            return {'id': group.id, 'name': group.name}, 201
        except IntegrityError:
            session.rollback()
            return {'message': 'Group with this name already exists'}, 400
        finally:
            session.close()


class StudentListResource(Resource):
    """
    Resource for handling operations on the collection of students.
    """
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('course', type=str, location='args', help='Filter by course name')
        parser.add_argument('max_group_size', type=int, location='args', help='Filter groups with max student count')
        args = parser.parse_args()

        session = SessionLocal()
        try:
            if args['course']:
                # Get students related to the specified course
                students = get_students_by_course_name(session, args['course'])
            elif args['max_group_size'] is not None:
                # Get groups with student count <= max_group_size
                groups = get_groups_with_student_count(session, args['max_group_size'])
                students = []
                for group in groups:
                    students.extend(group.students)
            else:
                # Get all students
                students = session.query(Student).options(joinedload(Student.courses)).all()

            result = []
            for s in students:
                result.append({
                    'id': s.id,
                    'first_name': s.first_name,
                    'last_name': s.last_name,
                    'group_id': s.group_id,
                    'courses': [c.name for c in s.courses]
                })
            return result, 200
        finally:
            session.close()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True, help='First name is required')
        parser.add_argument('last_name', type=str, required=True, help='Last name is required')
        parser.add_argument('group_id', type=int, required=False, help='Group ID must be an integer')
        args = parser.parse_args()

        session = SessionLocal()
        try:
            if args.get('group_id'):
                group = session.query(Group).filter(Group.id == args['group_id']).first()
                if not group:
                    return {'message': 'Group not found'}, 404

            student = add_new_student(session, args['first_name'], args['last_name'], args.get('group_id'))
            return {
                'id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'group_id': student.group_id
            }, 201
        except IntegrityError:
            session.rollback()
            return {'message': 'Error creating student'}, 400
        finally:
            session.close()


class StudentResource(Resource):
    """
    Resource for handling operations on individual students.
    """
    def get(self, student_id):
        session = SessionLocal()
        try:
            student = session.query(Student).options(joinedload(Student.courses)).filter(Student.id == student_id).first()
            if not student:
                return {'message': 'Student not found'}, 404
            return {
                'id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'group_id': student.group_id,
                'courses': [c.name for c in student.courses]
            }, 200
        finally:
            session.close()

    def put(self, student_id):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=False)
        parser.add_argument('last_name', type=str, required=False)
        parser.add_argument('group_id', type=int, required=False)
        args = parser.parse_args()

        session = SessionLocal()
        try:
            student = session.query(Student).filter(Student.id == student_id).first()
            if not student:
                return {'message': 'Student not found'}, 404

            if args.get('first_name'):
                student.first_name = args['first_name']
            if args.get('last_name'):
                student.last_name = args['last_name']
            if 'group_id' in args:
                if args['group_id'] is not None:
                    group = session.query(Group).filter(Group.id == args['group_id']).first()
                    if not group:
                        return {'message': 'Group not found'}, 404
                student.group_id = args['group_id']

            session.commit()
            return {'message': 'Student updated successfully'}, 200
        except IntegrityError:
            session.rollback()
            return {'message': 'Error updating student'}, 400
        finally:
            session.close()

    def delete(self, student_id):
        session = SessionLocal()
        try:
            success = delete_student_by_id(session, student_id)
            if success:
                return {'message': 'Student deleted successfully'}, 200
            else:
                return {'message': 'Student not found'}, 404
        finally:
            session.close()


class CourseListResource(Resource):
    """
    Resource for handling operations on the collection of courses.
    """
    def get(self):
        session = SessionLocal()
        try:
            courses = session.query(Course).all()
            return [{'id': c.id, 'name': c.name, 'description': c.description} for c in courses], 200
        finally:
            session.close()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Course name is required')
        parser.add_argument('description', type=str, required=False)
        args = parser.parse_args()

        session = SessionLocal()
        try:
            course = Course(name=args['name'], description=args.get('description'))
            session.add(course)
            session.commit()
            return {'id': course.id, 'name': course.name, 'description': course.description}, 201
        except IntegrityError:
            session.rollback()
            return {'message': 'Course with this name already exists'}, 400
        finally:
            session.close()


class CourseResource(Resource):
    """
    Resource for handling operations on individual courses.
    """
    def get(self, course_id):
        session = SessionLocal()
        try:
            course = session.query(Course).filter(Course.id == course_id).first()
            if not course:
                return {'message': 'Course not found'}, 404
            return {'id': course.id, 'name': course.name, 'description': course.description}, 200
        finally:
            session.close()

    def put(self, course_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=False)
        parser.add_argument('description', type=str, required=False)
        args = parser.parse_args()

        session = SessionLocal()
        try:
            course = session.query(Course).filter(Course.id == course_id).first()
            if not course:
                return {'message': 'Course not found'}, 404

            if args.get('name'):
                course.name = args['name']
            if args.get('description'):
                course.description = args['description']

            session.commit()
            return {'message': 'Course updated successfully'}, 200
        except IntegrityError:
            session.rollback()
            return {'message': 'Error updating course'}, 400
        finally:
            session.close()

    def delete(self, course_id):
        session = SessionLocal()
        try:
            course = session.query(Course).filter(Course.id == course_id).first()
            if not course:
                return {'message': 'Course not found'}, 404
            session.delete(course)
            session.commit()
            return {'message': 'Course deleted successfully'}, 200
        finally:
            session.close()


class StudentCourseResource(Resource):
    """
    Resource for handling the association between students and courses.
    """
    def post(self, student_id, course_id):
        session = SessionLocal()
        try:
            success = add_student_to_course(session, student_id, course_id)
            if success:
                return {'message': 'Course added to student'}, 200
            else:
                return {'message': 'Student or Course not found'}, 404
        finally:
            session.close()

    def delete(self, student_id, course_id):
        session = SessionLocal()
        try:
            success = remove_student_from_course(session, student_id, course_id)
            if success:
                return {'message': 'Course removed from student'}, 200
            else:
                return {'message': 'Student or Course not found or not associated'}, 404
        finally:
            session.close()


class GroupStudentsResource(Resource):
    """
    Resource for retrieving all students within a specific group.
    """
    def get(self, group_id):
        session = SessionLocal()
        try:
            group = session.query(Group).options(joinedload(Group.students)).filter(Group.id == group_id).first()
            if not group:
                return {'message': 'Group not found'}, 404
            students = [{
                'id': s.id,
                'first_name': s.first_name,
                'last_name': s.last_name,
                'group_id': s.group_id,
                'courses': [c.name for c in s.courses]
            } for s in group.students]
            return {'group_id': group.id, 'group_name': group.name, 'students': students}, 200
        finally:
            session.close()


class GroupWithMaxStudentsResource(Resource):
    """
    Resource for retrieving groups with a student count less than or equal to a specified maximum.
    """
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('max_count', type=int, required=True, help='max_count is required and must be an integer', location='args')
        args = parser.parse_args()
        if args['max_count'] < 0:
            return {'message': 'max_count must be a non-negative integer'}, 400

        session = SessionLocal()
        try:
            groups = get_groups_with_student_count(session, args['max_count'])
            result = []
            for g in groups:
                result.append({
                    'id': g.id,
                    'name': g.name,
                    'student_count': len(g.students)
                })
            return result, 200
        finally:
            session.close()


class StudentsByCourseResource(Resource):
    """
    Resource for retrieving all students enrolled in a specific course by course name.
    """
    def get(self, course_name):
        session = SessionLocal()
        try:
            # Query the course by name
            course = session.query(Course).filter(Course.name == course_name).first()
            if not course:
                return {'message': 'Course not found'}, 404

            # Retrieve all students enrolled in the course
            students = course.students  # Assuming a relationship is defined
            students_data = [{
                'id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'group_id': student.group_id,
                'courses': [c.name for c in student.courses]
            } for student in students]

            return students_data, 200
        finally:
            session.close()
