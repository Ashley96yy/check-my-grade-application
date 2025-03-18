from io import StringIO
import unittest
from unittest.mock import patch, mock_open, MagicMock
import csv
from common import Professor, professors, Course, courses

class TestDeleteProfessor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up test data before running any tests."""
        # Initialize courses dictionary
        courses.clear()
        courses["DATA201"] = Course("DATA201", "Data Structures and Algorithms", "Understand fundamental data structures and algorithms for programming.")
        courses["DATA208"] = Course("DATA208", "Game Development", "Learn to design and develop video games.")
        courses["DATA215"] = Course("DATA215", "Machine Learning", "Discover advanced techniques in supervised and unsupervised learning.")
        courses["DATA200"] = Course("DATA200", "Introduction to Artificial Intelligence", "Learn the basics of programming.")
        courses["DATA217"] = Course("DATA217", "Ethical Hacking", "Learn ethical hacking techniques to test and secure systems.")

        # Initialize professors dictionary
        professors.clear()
        professors["debra.gardner@myscu.edu"] = Professor(
            professor_id="debra.gardner@myscu.edu",
            name="Debra Gardner",
            rank="Senior Professor"
        )
        professors["debra.gardner@myscu.edu"].add_course("DATA201, DATA217, DATA208") 

    def setUp(self):
        """Reset test data before each test."""
        # Reinitialize professors dictionary
        professors.clear()
        professors["debra.gardner@myscu.edu"] = Professor(
            professor_id="debra.gardner@myscu.edu",
            name="Debra Gardner",
            rank="Senior Professor"
        )
        professors["debra.gardner@myscu.edu"].add_course("DATA201, DATA217, DATA208") 

    @patch("builtins.input", return_value="debra.gardner@myscu.edu")
    @patch("builtins.open", new_callable=mock_open)
    def test_delete_professor(self, mock_file, mock_input):
        """Test deleting a professor and related data."""
        # Mock CSV data for Professor.csv
        professor_csv_data = [
            ["debra.gardner@myscu.edu", "Debra Gardner", "Senior Professor", "DATA201"]
        ]
        csv_data = "\n".join([",".join(row) for row in professor_csv_data])
        professor_csv_data = StringIO(csv_data)

        mock_file.return_value.__enter__.return_value = professor_csv_data

        # Call the delete_professor method
        professor = Professor()
        professor.delete_professor()

        # Verify the professor is deleted from memory
        self.assertNotIn("debra.gardner@myscu.edu", professors)

        # Verify the professor is deleted from Professor.csv
        updated_professor_csv = [row for row in professor_csv_data if row[0] != "debra.gardner@myscu.edu"]
        self.assertNotIn(["debra.gardner@myscu.edu", "Debra Gardner", "Senior Professor", "DATA201, DATA217, DATA208"], updated_professor_csv)

        # Verify the course is deleted from the courses dictionary
        self.assertNotIn("DATA201", courses)

    @patch("builtins.input", return_value="nonexistent@myscu.edu")
    def test_delete_nonexistent_professor(self, mock_input):
        """Test deleting a professor that does not exist."""
        # Call the delete_professor method
        professor = Professor()
        professor.delete_professor()

        # Verify the professor is not in the professors dictionary
        self.assertNotIn("nonexistent@myscu.edu", professors)

if __name__ == "__main__":
    unittest.main()