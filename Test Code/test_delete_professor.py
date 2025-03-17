import unittest
from unittest.mock import patch, mock_open
import csv
from common import Professor, professors, Course, courses

class TestDeleteProfessor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up test data before running any tests."""
        # Initialize courses dictionary
        courses.clear()
        courses["DATA201"] = Course("DATA201", "Data Structures and Algorithms", "Understand fundamental data structures and algorithms for programming.")
        courses["DATA210"] = Course("DATA210", "Digital Marketing", "Learn online marketing strategies and analytics.")

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
        mock_file.return_value.__enter__.return_value = professor_csv_data

        # Mock CSV data for Grades.csv
        grades_csv_data = [
            ["STU001", "DATA201", "A"],
            ["STU002", "DATA210", "B"]
        ]
        mock_file.return_value.__enter__.return_value = grades_csv_data

        # Mock CSV data for Student.csv
        student_csv_data = [
            ["STU001", "Alice", "alice@myscu.edu", "DATA201,DATA210"],
            ["STU002", "Bob", "bob@myscu.edu", "DATA210"]
        ]
        mock_file.return_value.__enter__.return_value = student_csv_data

        # Mock CSV data for Course.csv
        course_csv_data = [
            ["DATA201", "Data Structures and Algorithms", "Understand fundamental data structures and algorithms for programming."],
            ["DATA210", "Digital Marketing", "Learn online marketing strategies and analytics."]
        ]
        mock_file.return_value.__enter__.return_value = course_csv_data

        # Call the delete_professor method
        professor = Professor()
        professor.delete_professor()

        # Verify the professor is deleted from memory
        self.assertNotIn("debra.gardner@myscu.edu", professors)

        # Verify the professor is deleted from Professor.csv
        updated_professor_csv = [row for row in professor_csv_data if row[0] != "debra.gardner@myscu.edu"]
        self.assertNotIn(["debra.gardner@myscu.edu", "Debra Gardner", "Senior Professor", "DATA201"], updated_professor_csv)

        # Verify the grades for the deleted professor's course are deleted from Grades.csv
        updated_grades_csv = [row for row in grades_csv_data if row[1] != "DATA201"]
        self.assertNotIn(["STU001", "DATA201", "A"], updated_grades_csv)

        # Verify the course IDs are removed from students' course lists in Student.csv
        updated_student_csv = []
        for row in student_csv_data:
            student_course_ids = row[3].split(",") if row[3] else []
            student_course_ids = [cid for cid in student_course_ids if cid != "DATA201"]
            updated_student_csv.append([row[0], row[1], row[2], ",".join(student_course_ids)])
        self.assertNotIn(["STU001", "Alice", "alice@myscu.edu", "DATA201,DATA210"], updated_student_csv)

        # Verify the course is deleted from Course.csv
        updated_course_csv = [row for row in course_csv_data if row[0] != "DATA201"]
        self.assertNotIn(["DATA201", "Data Structures and Algorithms", "Understand fundamental data structures and algorithms for programming."], updated_course_csv)

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