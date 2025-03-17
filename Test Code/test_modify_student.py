import unittest
from unittest.mock import patch, call
from common import Student, students  # Import the Student class and students dictionary

class TestStudent(unittest.TestCase):

    def setUp(self):
        """Initialize test data before each test method runs."""
        # Clear the students dictionary
        students.clear()

        # Add additional students used in the tests
        students["amanda.dudley@myscu.edu"] = Student("amanda.dudley@myscu.edu", "Amanda", "Dudley")
        students["amanda.dudley@myscu.edu"].add_course("DATA202")

        students["joseph.zuniga@myscu.edu"] = Student("joseph.zuniga@myscu.edu", "Joseph", "Zuniga")
        students["joseph.zuniga@myscu.edu"].add_course("DATA205,DATA218,DATA206")

        students["leslie.adams@myscu.edu"] = Student("leslie.adams@myscu.edu", "Leslie", "Adams")
        students["leslie.adams@myscu.edu"].add_course("DATA213")

    @patch("builtins.input")
    def test_modify_student_first_name(self, mock_input):
        """Test modifying the student's first name."""
        # Simulate user input
        mock_input.side_effect = [
            "leslie.adams@myscu.edu",  # Student ID
            "1",  # Choose to modify first name
            "Jane",  # New first name
        ]

        # Create a Student instance and call modify_student_records
        student = Student("dummy_id", "dummy_first", "dummy_last")
        student.modify_student_records("admin", "danielle.johnson@myscu.edu")

        # Verify that the first name is updated successfully
        self.assertEqual(students["leslie.adams@myscu.edu"].first_name, "Jane")

    @patch("builtins.input")
    def test_modify_student_last_name(self, mock_input):
        """Test modifying the student's last name."""
        # Simulate user input
        mock_input.side_effect = [
            "leslie.adams@myscu.edu",  # Student ID
            "2",  # Choose to modify last name
            "Smith",  # New last name
        ]

        # Create a Student instance and call modify_student_records
        student = Student("dummy_id", "dummy_first", "dummy_last")
        student.modify_student_records("admin", "danielle.johnson@myscu.edu")

        # Verify that the last name is updated successfully
        self.assertEqual(students["leslie.adams@myscu.edu"].last_name, "Smith")

    @patch("builtins.input")
    def test_modify_student_course_ids(self, mock_input):
        """Test modifying the student's course IDs."""
        # Simulate user input
        mock_input.side_effect = [
            "amanda.dudley@myscu.edu",  # Student ID
            "3",  # Choose to modify course IDs
            "1",  # Choose to modify a course ID
            "DATA202",  # Old course ID
            "DATA208",  # New course ID
        ]

        # Create a Student instance and call modify_student_records
        student = Student("dummy_id", "dummy_first", "dummy_last")
        student.modify_student_records("admin", "danielle.johnson@myscu.edu")

        # Verify that the course ID is updated successfully
        self.assertIn({"course_id": "DATA208"}, students["amanda.dudley@myscu.edu"].courses)
        self.assertNotIn({"course_id": "DATA200"}, students["amanda.dudley@myscu.edu"].courses)

    @patch("builtins.input")
    def test_modify_student_add_course(self, mock_input):
        """Test adding a new course ID."""
        # Simulate user input
        mock_input.side_effect = [
            "amanda.dudley@myscu.edu",  # Student ID
            "3",  # Choose to modify course IDs
            "3",  # Choose to add a new course ID
            "DATA213",  # New course ID
            "",
            ""
        ]

        # Create a Student instance and call modify_student_records
        student = Student("dummy_id", "dummy_first", "dummy_last")
        student.modify_student_records("admin", "danielle.johnson@myscu.edu")

        # Verify that the new course ID is added successfully
        expected_course = {"course_id": "DATA213"}
        self.assertIn(expected_course, students["amanda.dudley@myscu.edu"].courses)

    @patch("builtins.input")
    def test_modify_student_delete_course(self, mock_input):
        """Test deleting a course ID."""
        # Simulate user input
        mock_input.side_effect = [
            "joseph.zuniga@myscu.edu",  # Student ID
            "3",  # Choose to modify course IDs
            "2",  # Choose to delete a course ID
            "DATA205",  # Course ID to delete
        ]

        # Create a Student instance and call modify_student_records
        student = Student("dummy_id", "dummy_first", "dummy_last")
        student.modify_student_records("admin", "danielle.johnson@myscu.edu")

        # Verify that the course ID is deleted successfully
        self.assertNotIn({"course_id": "DATA205"}, students["joseph.zuniga@myscu.edu"].courses)

    @patch("builtins.input")
    def test_modify_student_invalid_choice(self, mock_input):
        """Test an invalid choice."""
        # Simulate user input
        mock_input.side_effect = [
            "joseph.zuniga@myscu.edu",  # Student ID
            "4",  # Invalid choice
        ]

        # Create a Student instance and call modify_student_records
        student = Student("dummy_id", "dummy_first", "dummy_last")
        student.modify_student_records("admin", "danielle.johnson@myscu.edu")

        # Verify that the student's information remains unchanged
        self.assertEqual(students["joseph.zuniga@myscu.edu"].first_name, "Joseph")
        self.assertEqual(students["joseph.zuniga@myscu.edu"].last_name, "Zuniga")
        self.assertEqual(
            [course["course_id"] for course in students["joseph.zuniga@myscu.edu"].courses],
            ["DATA205", "DATA218", "DATA206"]  # Original course IDs
        )

if __name__ == "__main__":
    unittest.main()