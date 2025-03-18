import unittest
import csv
from unittest.mock import patch
from common import Course, Professor, courses, professors 

class TestDeleteCourse(unittest.TestCase):

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
            rank="Senior Professor"
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
            rank="Senior Professor"
        )
        professors["debra.gardner@myscu.edu"].add_course("DATA201, DATA217, DATA208") 

    def test_admin_delete_course(self):
        """Test admin deleting a course."""
        # Simulate admin input
        with patch("builtins.input", return_value="DATA210"):
            course = Course()  # Create a Course instance
            course.delete_course("admin", "danielle.johnson@myscu.edu")

        # Verify that the course is removed from the courses dictionary
        self.assertNotIn("DATA210", courses)

        # Verify that the course is removed from Course.csv
        with open("Course.csv", "r") as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
        self.assertNotIn(["DATA210", "Digital Marketing", "Learn online marketing strategies and analytics."], rows)

        # Verify that the course is removed from Professor.csv
        with open("Professor.csv", "r") as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
        self.assertNotIn(["matthew.moore@myscu.edu", "Matthew Moore", "Senior Professor", "DATA210, DATA207"], rows)

        # Verify that the course is removed from Student.csv
        with open("Student.csv", "r") as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
        self.assertNotIn(["nancy.edwards@myscu.edu", "Nancy", "Edwards", "DATA210, DATA218"], rows)

        # Verify that the course is removed from Grades.csv
        with open("Grades.csv", "r") as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
        self.assertNotIn(["nancy.edwards@myscu.edu", "DATA210", "F", "28"], rows)

    def test_professor_delete_course_they_teach(self):
        """Test professor deleting a course they teach."""
        # Simulate professor input
        with patch("builtins.input", return_value="DATA201"):
            course = Course()  # Create a Course instance
            course.delete_course("professor", "debra.gardner@myscu.edu")

        # Verify that the course is removed from the courses dictionary
        self.assertNotIn("DATA201", courses)

        # Verify that the course is removed from Professor.csv
        with open("Professor.csv", "r") as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
        self.assertNotIn(["debra.gardner@myscu.edu", "Debra Gardner", "Senior Professor", "DATA201"], rows)

    def test_professor_delete_course_they_do_not_teach(self):
        """Test professor attempting to delete a course they do not teach."""
        # Simulate professor input
        with patch("builtins.input", return_value="DATA216"):
            course = Course()  # Create a Course instance
            course.delete_course("professor", "debra.gardner@myscu.edu")

        # Verify that the course is not deleted
        self.assertIn("DATA216", courses)

    def test_delete_nonexistent_course(self):
        """Test attempting to delete a non-existent course."""
        # Simulate input for a non-existent course ID
        with patch("builtins.input", return_value="NONEXISTENT"):
            course = Course()  # Create a Course instance
            course.delete_course("admin", "danielle.johnson@myscu.edu")

        # Verify that no changes were made
        self.assertIn("DATA210", courses)
        self.assertIn("DATA201", courses)

if __name__ == "__main__":
    unittest.main()