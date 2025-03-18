import unittest
import time
from common import grades, Grades

class TestGradesSorting(unittest.TestCase):
    def setUp(self):
        # Clear the grades dictionary before each test
        grades.clear()

        # Add sample data to the grades dictionary
        # Since student_id is email_address, we use email-like values for student_id
        grades1 = Grades(student_id="student1@example.com", course_id="DATA200", grade_input="A", marks_input="95")
        grades2 = Grades(student_id="student2@example.com", course_id="DATA200", grade_input="B", marks_input="85")
        grades3 = Grades(student_id="student3@example.com", course_id="DATA200", grade_input="C", marks_input="75")
        grades4 = Grades(student_id="student4@example.com", course_id="DATA200", grade_input="D", marks_input="65")
        grades5 = Grades(student_id="student5@example.com", course_id="DATA200", grade_input="F", marks_input="55")

    def test_sort_by_marks_ascending(self):
        print("\nTesting sorting by marks in ascending order...")
        start_time = time.time()
        Grades().display_all_grades_records(sort_by="marks", reverse=False)
        end_time = time.time()
        print(f"Time taken to sort by marks (ascending): {end_time - start_time:.6f} seconds")

    def test_sort_by_marks_descending(self):
        print("\nTesting sorting by marks in descending order...")
        start_time = time.time()
        Grades().display_all_grades_records(sort_by="marks", reverse=True)
        end_time = time.time()
        print(f"Time taken to sort by marks (descending): {end_time - start_time:.6f} seconds")

    def test_sort_by_email_ascending(self):
        print("\nTesting sorting by email (student_id) in ascending order...")
        start_time = time.time()
        Grades().display_all_grades_records(sort_by="student_id", reverse=False)
        end_time = time.time()
        print(f"Time taken to sort by email (ascending): {end_time - start_time:.6f} seconds")

    def test_sort_by_email_descending(self):
        print("\nTesting sorting by email (student_id) in descending order...")
        start_time = time.time()
        Grades().display_all_grades_records(sort_by="student_id", reverse=True)
        end_time = time.time()
        print(f"Time taken to sort by email (descending): {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    unittest.main()