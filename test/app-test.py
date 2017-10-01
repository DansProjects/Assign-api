from app import connection_string, app
import unittest
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from helpers import courses_to_json

from models import *


class GeneralTestCases(unittest.TestCase):

    def test_index(self):

        tester = app.test_client(self)
        response = tester.get('/', content_type='application/json')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(data, {'assign': 'api'})

    def test_404(self):

        tester = app.test_client(self)
        response = tester.get('/thisbetternotexistorsomethingisreallyreallywrong', content_type='application/json')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 404)


class CourseTestCase(unittest.TestCase):

    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    client = app.test_client()

    def setUp(self):

        semester = Semester()
        semester.season = 'Fall'
        semester.year = 2017
        self.session.add(semester)
        self.session.commit()
        self.semester = semester

        course = Course()
        course.course_name = "Test Course"
        course.semester_id = semester.id
        self.session.add(course)
        self.session.commit()
        self.course = course

    def test_index(self):

        courses = self.session.query(Course).all()
        courses_json = courses_to_json(courses)

        response = self.client.get('/courses', content_type='application/json')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(data, courses_json)

    def tearDown(self):

        self.session.delete(self.course)
        self.session.commit()
        self.session.delete(self.semester)
        self.session.commit()


if __name__ == '__main__':
    unittest.main()
