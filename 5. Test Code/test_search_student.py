import csv
import time
import unittest
from unittest.mock import patch
from common import Student, students  # Import Student class and students dictionary

# Load student data from CSV file
def load_students_from_csv(file_path):
    """Load student data from a CSV file"""
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)  # Use DictReader to read the CSV file
        for row in reader:
            student_id = row["Email_address"]
            first_name = row["First_name"]
            last_name = row["Last_name"]
            courses = row["Course_ids"].split(",")  # Split course IDs into a list

            # Create a Student object
            student = Student(student_id, first_name, last_name)
            for course in courses:
                student.add_course(course)
            students[student_id] = student  # Add the student object to the dictionary
    print(f"Loaded {len(students)} student records from {file_path}.")


# Unit test class
class TestStudentSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run before all tests to load student data"""
        cls.file_path = "Student.csv"
        load_students_from_csv(cls.file_path)

    def test_search_existing_student(self):
        """Test searching for an existing student"""
        student_id = "lindsay.blair@myscu.edu"
        with patch("builtins.input", return_value=student_id):
            if student_id in students:
                students[student_id].display_chosen_student_records()
            else:
                self.fail(f"Student ID: {student_id} not found.")

    def test_search_non_existing_student(self):
        """Test searching for a non-existing student"""
        student_id = "nonexist@myscu.edu"
        with patch("builtins.input", return_value=student_id):
            if student_id in students:
                self.fail(f"Student ID: {student_id} should not exist.")
            else:
                print(f"Student ID: {student_id} not found (expected).")

    def test_search_another_existing_student(self):
        """Test searching for another existing student"""
        student_id = "amanda.dudley@myscu.edu"
        with patch("builtins.input", return_value=student_id):
            if student_id in students:
                students[student_id].display_chosen_student_records()
            else:
                self.fail(f"Student ID: {student_id} not found.")


# Main program
if __name__ == "__main__":
    students.clear()  # Clear the global dictionary to ensure a clean test environment
    unittest.main()