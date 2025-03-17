import csv
import time
import unittest
from unittest.mock import patch
from common import Course, courses  # Import Course class and courses dictionary

# Load course data from CSV file
def load_courses_from_csv(file_path):
    """Load course data from a CSV file"""
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)  # Use DictReader to read the CSV file
        for row in reader:
            course_id = row["Course_id"]
            course_name = row["Course_name"]
            description = row["Description"]

            # Create a Course object
            course = Course(course_id, course_name, description)
            courses[course_id] = course  # Add the course object to the dictionary
    print(f"Loaded {len(courses)} course records from {file_path}.")


# Unit test class
class TestCourseSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run before all tests to load course data"""
        cls.file_path = "Course.csv"
        load_courses_from_csv(cls.file_path)
        # Print loaded course data for debugging
        for course_id, course in courses.items():
            print(f"Loaded Course: {course_id}, {course.course_name}, {course.description}")

    def test_search_existing_course(self):
        """Test searching for an existing course"""
        course_id = "DATA218"
        with patch("builtins.input", return_value=course_id):
            if course_id in courses:
                courses[course_id].display_chosen_course_records()
            else:
                self.fail(f"Course ID: {course_id} not found.")

    def test_search_non_existing_course(self):
        """Test searching for a non-existing course"""
        course_id = "PHYS101"
        with patch("builtins.input", return_value=course_id):
            if course_id in courses:
                self.fail(f"Course ID: {course_id} should not exist.")
            else:
                print(f"Course ID: {course_id} not found (expected).")


# Main program
if __name__ == "__main__":
    courses.clear()  # Clear the global dictionary to ensure a clean test environment
    unittest.main()