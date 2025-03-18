import csv
import time
import unittest
from unittest.mock import patch
from common import Grades, grades  # Import Grade class and grades dictionary

# Load grade data from CSV file
def load_grades_from_csv(file_path):
    """Load grade data from a CSV file"""
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)  # Use DictReader to read the CSV file
        for row in reader:
            student_id = row["Email_address"]
            course_id = row["Course_id"]
            grade_input = row["Grades"]
            marks_input = row["Marks"]

            # Create a Grade object
            grade = Grades(student_id, course_id, grade_input, marks_input)
            grades[(student_id, course_id)] = grade  # Add the grade object to the dictionary
    print(f"Loaded {len(grades)} grade records from {file_path}.")


# Unit test class
class TestGradeSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run before all tests to load grade data"""
        cls.file_path = "Grades.csv"
        load_grades_from_csv(cls.file_path)
        # Print loaded grade data for debugging
        for key, grade in grades.items():
            print(f"Loaded Grade: Student ID: {grade.student_id}, Course ID: {grade.course_id}, Grade: {grade.grade_input}, Marks: {grade.marks_input}")

    def test_search_grade_by_student_and_course(self):
        """Test searching for a grade by student ID and course ID"""
        student_id = "nicholas.arnold@myscu.edu"
        course_id = "DATA211"
        with patch("builtins.input", side_effect=[student_id, course_id]):
            if (student_id, course_id) in grades:
                grades[(student_id, course_id)].display_chosen_grade_records()
            else:
                self.fail(f"Grade not found for Student ID: {student_id}, Course ID: {course_id}.")

    def test_search_grades_by_student(self):
        """Test searching for grades by student ID"""
        student_id = "michelle.ray@myscu.edu"
        course_id = ""  # Leave blank to search by student ID only
        with patch("builtins.input", side_effect=[student_id, course_id]):
            found = False
            for key, grade in grades.items():
                if key[0] == student_id:
                    found = True
                    break
            if not found:
                self.fail(f"No grades found for Student ID: {student_id}.")

    def test_search_grades_by_course(self):
        """Test searching for grades by course ID"""
        student_id = ""  # Leave blank to search by course ID only
        course_id = "DATA218"
        with patch("builtins.input", side_effect=[student_id, course_id]):
            found = False
            for key, grade in grades.items():
                if key[1] == course_id:
                    found = True
                    break
            if not found:
                self.fail(f"No grades found for Course ID: {course_id}.")

# Main program
if __name__ == "__main__":
    grades.clear()  
    unittest.main()