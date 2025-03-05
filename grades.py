import csv

##### Initialize data #####
# Use a dictionary (hash table) to store all the grades, with (student_id, course_id) as the key
grades = {}

##### Class Grades #####
class Grades:

    def __init__(self, student_id, course_id, grades, marks):
        self.student_id = student_id # Unique student ID # Composite primary key (student_id, course_id)
        self.course_id = course_id # Unique course ID # Composite primary key (student_id, course_id)
        self.grades = grades 
        self.marks = marks 

    def display_all_grades_records(self):
        """ Display all the grades details, sorted by specific field
        Parameters:
            sorted_by (str): The field to sort the grades by
            -- Options: "student_id", "course_id", "grades", "marks"
        """

        if not grades:
            print("No grades records found.")
            return
        
        # Validate the sorted_by field
        if sort_by not in ["student_id", "course_id", "grades", "marks"]:
            print("Invalid field to sort by. Sorting by student_id by default.")
            sort_by = "student_id"

        # Conver the grades dictionary to a list of grades for sorting
        grades_list = list(grades.values())

        # Sort the grades by the specified field
        if sort_by == "student_id":
            grades_list.sort(key=lambda x: x.student_id)
        elif sort_by == "course_id":
            grades_list.sort(key=lambda x: x.course_id)
        elif sort_by == "grades":
            grades_list.sort(key=lambda x: x.grades)
        elif sort_by == "marks":
            grades_list.sort(key=lambda x: x.marks)

        # Display the sorted grades
        print(f"\nDisplaying all grades records (sorted by {sort_by}):")
        for grade in grades_list:
            print(f"Student ID: {grade.student_id}, Course ID: {grade.course_id}, Grades: {grade.grades}, Marks: {grade.marks}")
            print("-" * 30)
        
    def display_chosen_grade_records(self):
        # Display the chosen grade's details and measure lookup time
        pass

    def add_grade(self):
        # Add a grade for a student in a course by a professor
        # (student_id, course_id, grade, mark)
        # Check if the student is enrolled in the course
        # Check if the professor is teaching the course
        pass

    def delete_grade(self):
        # Delete a grade for a student in a course by a professor
        # (student_id, course_id)
        # Check if the student is enrolled in the course
        # Check if the professor is teaching the course
        pass

    def modify_grade(self):
        # Modify a grade for a student in a course by a professor
        # (student_id, course_id, grade, mark)
        # Check if the student is enrolled in the course
        # Check if the professor is teaching the course
        pass

    def calculateAverageMark(self):
        # Calculate the average of all the marks for a student
        pass

    def calculateMedianMark(self):
        # Calculate the median of all the marks for a student
        pass

    def save_grades_to_csv(self, filename):
        # Save the grades to a CSV file
        pass

##### Read the Grades CSV file #####
def load_grades_data():
    """ Load grades data from CSV file """
    with open("Grades.csv", "r") as grades_file:
        reader = csv.reader(grades_file)
        next(reader)
        for row in reader:
            student_id, course_id, grades, marks = row
            # Use (student_id, course_id) as the key
            grades[(student_id, course_id)] = Grades(student_id, course_id, grades, marks)

# Load grades data when the module is imported
load_grades_data()
