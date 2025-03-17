import unittest
from unittest.mock import patch
from common import Professor, professors, Course, courses 

class TestAddProfessor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up test data before running any tests."""
        # Initialize the courses dictionary
        courses.clear()
        courses["DATA201"] = Course("DATA201", "Data Structures and Algorithms", "Understand fundamental data structures and algorithms for programming.")
        courses["DATA210"] = Course("DATA210", "Digital Marketing", "Learn online marketing strategies and analytics.")
        courses["DATA216"] = Course("DATA216", "Quantum Computing", "An introduction to the principles of quantum computing.")

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
        # Re-initialize the professors dictionary
        professors.clear()
        professors["debra.gardner@myscu.edu"] = Professor(
            professor_id="debra.gardner@myscu.edu",
            name="Debra Gardner",
            rank="Senior Professor"
        )
        professors["debra.gardner@myscu.edu"].add_course("DATA201, DATA217, DATA208") 

    def test_add_new_professor(self):
        """Test adding a new professor."""
        # Simulate user input
        with patch("builtins.input", side_effect=["john.doe@myscu.edu", "John Doe", "Assistant Professor", "DATA220"]):
            professor = Professor()  # Create a Professor instance
            professor.add_new_professor()

        # Verify that the new professor is added to the professors dictionary
        self.assertIn("john.doe@myscu.edu", professors)
        self.assertEqual(professors["john.doe@myscu.edu"].name, "John Doe")
        self.assertEqual(professors["john.doe@myscu.edu"].rank, "Assistant Professor")
        self.assertEqual([course["course_id"] for course in professors["john.doe@myscu.edu"].courses], ["DATA220"])

    def test_add_existing_professor(self):
        """Test adding an existing professor."""
        # Simulate user input
        with patch("builtins.input", side_effect=["debra.gardner@myscu.edu", "Debra Gardner", "Senior Professor", "DATA201"]):
            professor = Professor()  # Create a Professor instance
            professor.add_new_professor()

        # Verify that the professor is not duplicated
        self.assertEqual(len(professors), 1)  # Ensure there is only one professor in the dictionary

    def test_add_professor_with_invalid_course_id(self):
        """Test adding a professor with invalid course IDs."""
        # Simulate user input
        with patch("builtins.input", side_effect=["john.doe@myscu.edu", "John Doe", "Assistant Professor", "INVALID_COURSE"]):
            professor = Professor()  # Create a Professor instance
            professor.add_new_professor()

        # Verify that the professor is not added
        self.assertNotIn("john.doe@myscu.edu", professors)

    def test_add_professor_with_assigned_course_id(self):
        """Test adding a professor with course IDs already assigned to another professor."""
        # Simulate user input
        with patch("builtins.input", side_effect=["john.doe@myscu.edu", "John Doe", "Assistant Professor", "DATA201"]):
            professor = Professor()  # Create a Professor instance
            professor.add_new_professor()

        # Verify that the professor is not added
        self.assertNotIn("john.doe@myscu.edu", professors)

    def test_add_professor_without_course_ids(self):
        """Test adding a professor without course IDs."""
        # Simulate user input
        with patch("builtins.input", side_effect=["john.doe@myscu.edu", "John Doe", "Assistant Professor", ""]):
            professor = Professor()  # Create a Professor instance
            professor.add_new_professor()

        # Verify that the new professor is added to the professors dictionary
        self.assertIn("john.doe@myscu.edu", professors)
        self.assertEqual(professors["john.doe@myscu.edu"].name, "John Doe")
        self.assertEqual(professors["john.doe@myscu.edu"].rank, "Assistant Professor")
        self.assertEqual(professors["john.doe@myscu.edu"].courses, []) 

if __name__ == "__main__":
    unittest.main()