import unittest
import csv
from unittest.mock import patch
from common import Course, Professor, courses, professors  # Import necessary classes and dictionaries

class TestModifyCourse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up test data before running any tests."""
        # Initialize the courses dictionary
        courses.clear()
        courses["DATA210"] = Course("DATA210", "Digital Marketing", "Learn online marketing strategies and analytics.")
        courses["DATA216"] = Course("DATA216", "Quantum Computing", "An introduction to the principles of quantum computing.")
        courses["DATA201"] = Course("DATA201", "Data Structures and Algorithms", "Understand fundamental data structures and algorithms for programming.")

        # Initialize the professors dictionary
        professors.clear()
        professors["debra.gardner@myscu.edu"] = Professor(
            professor_id="debra.gardner@myscu.edu",
            name="Debra Gardner",
            rank="Senior Professor",
        )
        professors["debra.gardner@myscu.edu"].add_course("DATA201, DATA217, DATA208") 
        

    def setUp(self):
        """Reset test data before each test."""
        # Re-initialize the courses and professors dictionaries
        courses.clear()
        courses["DATA210"] = Course("DATA210", "Digital Marketing", "Learn online marketing strategies and analytics.")
        courses["DATA216"] = Course("DATA216", "Quantum Computing", "An introduction to the principles of quantum computing.")
        courses["DATA201"] = Course("DATA201", "Data Structures and Algorithms", "Understand fundamental data structures and algorithms for programming.")

        professors.clear()
        professors["debra.gardner@myscu.edu"] = Professor(
            professor_id="debra.gardner@myscu.edu",
            name="Debra Gardner",
            rank="Senior Professor",
        )
        professors["debra.gardner@myscu.edu"].add_course("DATA201, DATA217, DATA208") 

    def test_admin_modify_course_name(self):
        """Test admin modifying a course name."""
        # Simulate admin input
        with patch("builtins.input", side_effect=["DATA210", "1", "Advanced Digital Marketing"]):
            course = Course()  # Create a Course instance
            course.modify_course("admin", "danielle.johnson@myscu.edu")

        # Verify that the course name is updated
        self.assertEqual(courses["DATA210"].course_name, "Advanced Digital Marketing")

        # Verify that Course.csv is updated
        with open("Course.csv", "r") as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
        self.assertIn(["DATA210", "Advanced Digital Marketing", "Learn online marketing strategies and analytics."], rows)

    def test_admin_modify_course_description(self):
        """Test admin modifying a course description."""
        # Simulate admin input
        with patch("builtins.input", side_effect=["DATA210", "2", "Advanced strategies for online marketing."]):
            course = Course()  # Create a Course instance
            course.modify_course("admin", "danielle.johnson@myscu.edu")

        # Verify that the course description is updated
        self.assertEqual(courses["DATA210"].description, "Advanced strategies for online marketing.")

        # Verify that Course.csv is updated
        with open("Course.csv", "r") as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
        self.assertIn(["DATA210", "Digital Marketing", "Advanced strategies for online marketing."], rows)

    def test_professor_modify_course_they_teach(self):
        """Test professor modifying a course they teach."""
        # Simulate professor input
        with patch("builtins.input", side_effect=["DATA201", "1", "Advanced Data Structures and Algorithms"]):
            course = Course()  # Create a Course instance
            course.modify_course("professor", "debra.gardner@myscu.edu")

        # Verify that the course name is updated
        self.assertEqual(courses["DATA201"].course_name, "Advanced Data Structures and Algorithms")

        # Verify that Course.csv is updated
        with open("Course.csv", "r") as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
        self.assertIn(["DATA201", "Advanced Data Structures and Algorithms", "Understand fundamental data structures and algorithms for programming."], rows)

    def test_professor_modify_course_they_do_not_teach(self):
        """Test professor attempting to modify a course they do not teach."""
        # Simulate professor input
        with patch("builtins.input", side_effect=["DATA216", "1", "Advanced Quantum Computing"]):
            course = Course()  # Create a Course instance
            course.modify_course("professor", "debra.gardner@myscu.edu")

        # Verify that the course name is not modified
        self.assertEqual(courses["DATA216"].course_name, "Quantum Computing")

    def test_modify_nonexistent_course(self):
        """Test attempting to modify a non-existent course."""
        # Simulate input for a non-existent course ID
        with patch("builtins.input", side_effect=["NONEXISTENT", "1", "New Course Name"]):
            course = Course()  # Create a Course instance
            course.modify_course("admin", "danielle.johnson@myscu.edu")

        # Verify that no changes were made
        self.assertEqual(courses["DATA210"].course_name, "Digital Marketing")
        self.assertEqual(courses["DATA216"].course_name, "Quantum Computing")

    def test_invalid_choice(self):
        """Test invalid choice during modification."""
        # Simulate invalid input choice
        with patch("builtins.input", side_effect=["DATA210", "3"]):
            course = Course()  # Create a Course instance
            course.modify_course("admin", "danielle.johnson@myscu.edu")

        # Verify that the course name and description are not modified
        self.assertEqual(courses["DATA210"].course_name, "Digital Marketing")
        self.assertEqual(courses["DATA210"].description, "Learn online marketing strategies and analytics.")

if __name__ == "__main__":
    unittest.main()