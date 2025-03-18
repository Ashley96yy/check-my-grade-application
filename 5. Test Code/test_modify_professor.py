import unittest
from unittest.mock import patch
import csv
import os
from common import Professor, professors

class TestModifyProfessorDetails(unittest.TestCase):

    def setUp(self):
        # Initialize test data
        self.professor_id = "susan.rogers@myscu.edu"
        self.professor = Professor(professor_id=self.professor_id, name="Susan Rogers", rank="Senior Professor")
        professors[self.professor_id] = self.professor

    @patch('builtins.input', side_effect=["1", "Jane Doe"])
    def test_modify_professor_name(self, mock_input):
        # Test modifying professor's name
        self.professor.modify_professor_details(self.professor_id)
        self.assertEqual(self.professor.name, "Jane Doe")

    @patch('builtins.input', side_effect=["2", "Assistant Professor"])
    def test_modify_professor_rank(self, mock_input):
        # Test modifying professor's rank
        self.professor.modify_professor_details(self.professor_id)
        self.assertEqual(self.professor.rank, "Assistant Professor")

    @patch('builtins.input', side_effect=["3", "1", "DATA206", "DATA201"])
    def test_modify_course_id(self, mock_input):
        # Test modifying course ID
        self.professor.add_course("DATA206")
        self.professor.modify_professor_details(self.professor_id)
        self.assertEqual(self.professor.courses[0]["course_id"], "DATA206")

    @patch('builtins.input', side_effect=["3", "3", "C001"])
    def test_delete_course_id(self, mock_input):
        # Test deleting course ID
        self.professor.add_course("DATA206,DATA213")
        self.professor.modify_professor_details(self.professor_id)
        self.assertEqual(len(self.professor.courses), 2)
        self.assertEqual(self.professor.courses[0]["course_id"], "DATA206")

    def verify_csv_files(self):
        with open("Student.csv", mode="r") as student_file:
            student_reader = csv.reader(student_file)
            student_data = list(student_reader)
            for row in student_data:
                if row[0] == "DATA213":
                    self.assertNotIn("DATA213", row[3].split(",")) 

        with open("Course.csv", mode="r") as course_file:
            course_reader = csv.reader(course_file)
            course_data = list(course_reader)
            self.assertNotIn(["DATA213", "Operating Systems", "Understand the principles and functions of operating systems."], course_data) 

if __name__ == "__main__":
    unittest.main()