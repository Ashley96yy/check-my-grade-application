import unittest
import csv
from unittest.mock import patch, call
from common import Student, students  # Import Student class and students dictionary from common.py

class TestStudent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load test data from CSV files."""
        # Load Student.csv
        with open("Student.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                student_id, first_name, last_name, course_ids_str = row
                students[student_id] = Student(student_id, first_name, last_name)
                students[student_id].add_course(course_ids_str)

    @patch("builtins.input", return_value="mitchell.clark@myscu.edu")
    def test_delete_student(self, mock_input):
        """Test deleting a student."""
        # Use delete_student function to delete the student
        student_to_delete = students["mitchell.clark@myscu.edu"]
        student_to_delete.delete_student()

        # Verify the student was deleted
        self.assertNotIn("mitchell.clark@myscu.edu", students)
    
    def test_delete_nonexistent_student(self):
        """Test deleting a student that does not exist."""
        # Attempt to delete a non-existent student
        nonexistent_student_id = "S9999"

        # Check if the student exists
        self.assertNotIn(nonexistent_student_id, students)

        # Attempt to get the student instance
        with self.assertRaises(KeyError):
            student_to_delete = students[nonexistent_student_id]

if __name__ == "__main__":
    unittest.main()