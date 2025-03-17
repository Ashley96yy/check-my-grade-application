import csv
import time
import unittest
from unittest.mock import patch
from common import Professor, professors  

# Load professor data from CSV file
def load_professors_from_csv(file_path):
    """Load professor data from a CSV file"""
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)  # Use DictReader to read the CSV file
        for row in reader:
            professor_id = row["Professor_id"]
            name = row["Professor_Name"]
            rank = row["Rank"]
            courses = row["Course_id"].split(",")  # Split course IDs into a list

            # Create a Professor object
            professor = Professor(professor_id, name, rank)
            for course in courses:
                professor.courses.append({"course_id": course.strip()})
            professors[professor_id] = professor 
    print(f"Loaded {len(professors)} professor records from {file_path}.")


# Unit test class
class TestProfessorSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run before all tests to load professor data"""
        cls.file_path = "Professor.csv"
        load_professors_from_csv(cls.file_path)
        # Print loaded professor data for debugging
        for professor_id, professor in professors.items():
            print(f"Loaded Professor: {professor_id}, {professor.name}, {professor.rank}, Courses: {professor.courses}")

    def test_search_existing_professor(self):
        """Test searching for an existing professor"""
        professor_id = "matthew.moore@myscu.edu"
        with patch("builtins.input", return_value=professor_id):
            if professor_id in professors:
                professors[professor_id].display_chosen_professor_records()
            else:
                self.fail(f"Professor ID: {professor_id} not found.")

    def test_search_non_existing_professor(self):
        """Test searching for a non-existing professor"""
        professor_id = "P999"
        with patch("builtins.input", return_value=professor_id):
            if professor_id in professors:
                self.fail(f"Professor ID: {professor_id} should not exist.")
            else:
                print(f"Professor ID: {professor_id} not found (expected).")

    def test_search_another_existing_professor(self):
        """Test searching for another existing professor"""
        professor_id = "christopher.davis@myscu.edu"
        with patch("builtins.input", return_value=professor_id):
            if professor_id in professors:
                professors[professor_id].display_chosen_professor_records()
            else:
                self.fail(f"Professor ID: {professor_id} not found.")


# Main program
if __name__ == "__main__":
    professors.clear() 
    unittest.main()