import unittest
import time
from common import students, Student

class TestStudentSorting(unittest.TestCase):
    def setUp(self):
        # Clear the students dictionary before each test
        students.clear()

        # Add sample data to the students dictionary
        student1 = Student(student_id="student1@example.com", first_name="John", last_name="Doe")
        student1.add_course("DATA201")
        student2 = Student(student_id="student2@example.com", first_name="Alice", last_name="Smith")
        student2.add_course("DATA201")
        student3 = Student(student_id="student3@example.com", first_name="Bob", last_name="Johnson")
        student3.add_course("DATA201")
        student4 = Student(student_id="student4@example.com", first_name="Charlie", last_name="Brown")
        student4.add_course("DATA201")

    def test_sort_by_student_id_ascending(self):
        print("\nTesting sorting by student_id in ascending order...")
        start_time = time.time()
        Student().display_all_students_records(sort_by="student_id", reverse=False)
        end_time = time.time()
        print(f"Time taken to sort by student_id (ascending): {end_time - start_time:.6f} seconds")

    def test_sort_by_student_id_descending(self):
        print("\nTesting sorting by student_id in descending order...")
        start_time = time.time()
        Student().display_all_students_records(sort_by="student_id", reverse=True)
        end_time = time.time()
        print(f"Time taken to sort by student_id (descending): {end_time - start_time:.6f} seconds")

    def test_sort_by_first_name_ascending(self):
        print("\nTesting sorting by first_name in ascending order...")
        start_time = time.time()
        Student().display_all_students_records(sort_by="first_name", reverse=False)
        end_time = time.time()
        print(f"Time taken to sort by first_name (ascending): {end_time - start_time:.6f} seconds")

    def test_sort_by_first_name_descending(self):
        print("\nTesting sorting by first_name in descending order...")
        start_time = time.time()
        Student().display_all_students_records(sort_by="first_name", reverse=True)
        end_time = time.time()
        print(f"Time taken to sort by first_name (descending): {end_time - start_time:.6f} seconds")

    def test_sort_by_last_name_ascending(self):
        print("\nTesting sorting by last_name in ascending order...")
        start_time = time.time()
        Student().display_all_students_records(sort_by="last_name", reverse=False)
        end_time = time.time()
        print(f"Time taken to sort by last_name (ascending): {end_time - start_time:.6f} seconds")

    def test_sort_by_last_name_descending(self):
        print("\nTesting sorting by last_name in descending order...")
        start_time = time.time()
        Student().display_all_students_records(sort_by="last_name", reverse=True)
        end_time = time.time()
        print(f"Time taken to sort by last_name (descending): {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    unittest.main()