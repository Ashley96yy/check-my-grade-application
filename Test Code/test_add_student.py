import unittest
from unittest.mock import patch, call
from common import Student, students  # Import Student class and students dictionary from common.py

class TestStudent(unittest.TestCase):

    def setUp(self):
        """Reset the students dictionary before each test."""
        # Clear the students dictionary
        students.clear()

    @patch("builtins.input")
    @patch("common.Student.save_grades_to_csv")
    @patch("common.Student.save_students_to_csv")
    def test_add_student(self, mock_save_students_to_csv, mock_save_grades_to_csv, mock_input):
        """Test adding a new student."""
        # Mock user input
        mock_input.side_effect = [
            "S1001@myscu.edu",  # Student ID
            "Alice",  # First name
            "Johnson",  # Last name
            "DATA200,DATA201",  # Course IDs
            "A",  # Grade for DATA200
            "90",  # Marks for DATA200 (as string)
            "B",  # Grade for DATA201
            "85",  # Marks for DATA201 (as string)
        ]

        # Create a Student instance and call add_new_student
        student = Student("dummy_id", "dummy_first", "dummy_last")  # Create a dummy instance
        student.add_new_student()

        # Verify the student was added to the students dictionary
        self.assertIn("S1001@myscu.edu", students)
        self.assertEqual(students["S1001@myscu.edu"].first_name, "Alice")
        self.assertEqual(students["S1001@myscu.edu"].last_name, "Johnson")
        self.assertEqual(
            [course["course_id"] for course in students["S1001@myscu.edu"].courses],
            ["DATA200", "DATA201"]
        )

        # Verify save_grades_to_csv was called correctly
        expected_calls = [
            call("S1001@myscu.edu", "DATA200", "A", 90),  # Marks as integer
            call("S1001@myscu.edu", "DATA201", "B", 85),  # Marks as integer
        ]
        mock_save_grades_to_csv.assert_has_calls(expected_calls, any_order=True)

        # Verify save_students_to_csv was called correctly
        mock_save_students_to_csv.assert_called_once_with("S1001@myscu.edu", "Alice", "Johnson", ["DATA200", "DATA201"])

    @patch("builtins.input")
    def test_add_new_student_invalid_course(self, mock_input):
        """Test adding a new student with invalid course IDs."""
        # Mock user input
        mock_input.side_effect = [
            "S1002@myscu.edu",  # Student ID
            "Bob",  # First name
            "Smith",  # Last name
            "DATE999",  # Invalid course ID
        ]

        # Create a Student instance and call add_new_student
        student = Student("dummy_id", "dummy_first", "dummy_last")
        student.add_new_student()

        # Verify the student was not added to the students dictionary
        self.assertNotIn("S1002@myscu.edu", students)

    @patch("builtins.input")
    def test_add_new_student_duplicate_id(self, mock_input):
        """Test adding a student with a duplicate ID."""
        # Add an existing student
        students["deborah.lynch@myscu.edu"] = Student("deborah.lynch@myscu.edu", "Deborah", "Lynch")

        # Mock user input
        mock_input.side_effect = [
            "deborah.lynch@myscu.edu",  # Duplicate student ID
            "Deborah",  # First name
            "Lynch",  # Last name
            "DATA207,DATA217,DATA201",  # Course IDs
        ]

        # Create a Student instance and call add_new_student
        student = Student("dummy_id", "dummy_first", "dummy_last")
        student.add_new_student()

        # Verify the student was not added again
        self.assertEqual(len(students), 1)  # Only the original student should exist

if __name__ == "__main__":
    unittest.main()