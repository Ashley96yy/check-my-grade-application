import unittest
import csv
from unittest.mock import patch
from common import Course, courses  # Import Course class and courses dictionary

class TestCourse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load test data from CSV files."""
        # Clear the courses dictionary
        courses.clear()

        # Clear or initialize Course.csv
        with open("Course.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Course_id", "Course_name", "Description"])  # Write header

    def setUp(self):
        """Initialize test data before each test method runs."""
        # Clear the courses dictionary
        courses.clear()

        # Clear or initialize Course.csv
        with open("Course.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Course_id", "Course_name", "Description"])  # Write header

    def test_add_new_course(self):
        """Test adding a new course using the add_new_course method."""
        # Simulate user input
        new_course_id = "CSCI102"
        new_course_name = "Advanced Programming"
        new_description = "Learn advanced programming concepts."

        with patch("builtins.input", side_effect=[new_course_id, new_course_name, new_description]):
            # Create a Course instance and call add_new_course
            course = Course()  # Create a Course instance
            course.add_new_course()

        # Verify the course was added to the courses dictionary
        self.assertIn(new_course_id, courses)
        self.assertEqual(courses[new_course_id].course_name, new_course_name)
        self.assertEqual(courses[new_course_id].description, new_description)

    def test_add_existing_course(self):
        """Test adding a course with an existing ID."""
        # Add an existing course
        existing_course_id = "CSCI101"
        courses[existing_course_id] = Course(existing_course_id, "Existing Course", "This is an existing course.")

        # Simulate user input (attempt to add an existing course ID)
        with patch("builtins.input", side_effect=[existing_course_id, "New Course", "New Description"]):
            course = Course()  # Create a Course instance
            course.add_new_course()

        # Verify the course was not duplicated
        self.assertEqual(len(courses), 1)  # Ensure only one course exists in the dictionary
        self.assertEqual(courses[existing_course_id].course_name, "Existing Course")  # Ensure the course name is unchanged

    def test_save_courses_to_csv(self):
        """Test saving courses to a CSV file."""
        # Add a test course
        test_course_id = "TEST101"
        test_course_name = "Test Course"
        test_description = "This is a test course."
        courses[test_course_id] = Course(test_course_id, test_course_name, test_description)

        # Save the course to the CSV file
        course = Course()  # Create a Course instance
        course.save_courses_to_csv(test_course_id, test_course_name, test_description)

        # Verify the CSV file content
        with open("Course.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Check the header
        self.assertEqual(rows[0], ["Course_id", "Course_name", "Description"])

        # Check the data row
        self.assertEqual(len(rows), 2)  # Header + one data row
        self.assertEqual(rows[1], [test_course_id, test_course_name, test_description])

if __name__ == "__main__":
    unittest.main()