import csv
import time
import statistics
from student import Student, students
from course import Course, courses
from professor import Professor, professors

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
        student_id = input("Enter the student ID (or leave bland to see all students): ").strip()
        course_id = input("Enter the course ID (or leave blank to see all courses): ").strip()
        start_time = time.time() # Record the start time

        if student_id and course_id:
            # Case 1: Both student_id and course_id are provided
            if (student_id, course_id) in grades:
                grade = grades[(student_id, course_id)]
                print(f"Student ID: {grade.student_id}, Course ID: {grade.course_id}, Grades: {grade.grades}, Marks: {grade.marks}")
            else:
                print("Grade not found.")
        
        elif student_id:
            # Case 2: Only student_id is provided
            found = False
            for key, grade in grades.items():
                if key[0] == student_id:
                    print(f"Student ID: {grade.student_id}, Course ID: {grade.course_id}, Grades: {grade.grades}, Marks: {grade.marks}")
                    found = True
            if not found:
                print("No grades found for the student.")
        
        elif course_id:
            # Case 3: Only course_id is provided
            found = False
            for key, grade in grades.items():
                if key[1] == course_id:
                    print(f"Student ID: {grade.student_id}, Course ID: {grade.course_id}, Grades: {grade.grades}, Marks: {grade.marks}")
                    found = True
            if not found:
                print("No grades found for the course.")
        
        else:
            # Case 4: Both student_id and course_id are not provided
            print("Please provide at least a student ID or course ID to lookup a grade.")

        end_time = time.time() # Record the end time
        elapsed_time = end_time - start_time
        print(f"Time taken to lookup the grade: {elapsed_time:.6f} seconds")

    def add_new_grade(self, role, email_id):
        # Add a grade for a student in a course by a professor or admin
        student_id = input("Enter the student ID: ").strip()
        course_id = input("Enter the course ID: ").strip()
        grades = input("Enter the grades (A, B, C, D, F): ").strip()
        marks = input("Enter the marks (0-100): ").strip()

        # Check if the student exists
        if student_id not in students:
            print("Student not found.")
            return
        
        # Check if the course exists
        if course_id not in courses:
            print("Course not found.")
            return
        
        # Check if the student is enrolled in the course
        if (student_id, course_id) not in grades:
            print("Student is not enrolled in the course.")
            return

        # Check if the grades are valid
        if grades not in ["A", "B", "C", "D", "F"]:
            print("Invalid grades. Please enter A, B, C, D, or F.")
            return
        
        # Check if the marks are valid
        if not marks.isdigit() or int(marks) < 0 or int(marks) > 100:
            print("Invalid marks. Please enter a number between 0 and 100.")
            return
        
        # Check if the user has the right to add a grade
        if role == "professor":
            # Check if the professor is teaching the course
            professor = professors[email_id]
            professor_course_ids = professor["courses"]
            if course_id not in professor_course_ids:
                print("You do not have the right to add a grade for this course.")
                return
            # Add the grade
            grades[(student_id, course_id)] = Grades(student_id, course_id, grades, marks)
            # Save the grades to the CSV file
            with open("Grades.csv", "a") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow([student_id, course_id, grades, marks])
            print("Grade added successfully.")

        elif role == "admin":
            # Admin can add a grade for any course
            grades[(student_id, course_id)] = Grades(student_id, course_id, grades, marks)
            # Save the grades to the CSV file 
            with open("Grades.csv", "a") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow([student_id, course_id, grades, marks])
            print("Grade added successfully.")

        else:
            print("You do not have the right to add a grade.")

    def delete_grade(self, role, email_id):
        # Delete a grade for a student in a course by a professor or admin
        student_id = input("Enter the student ID of the grade to be deleted: ").strip()
        course_id = input("Enter the course ID of the grade to be deleted: ").strip()
        if (student_id, course_id) not in grades:
            print("Grade not found.")
            return
        
        # Check if the user has the right to delete a grade
        if role == "professor":
            # Check if the professor is teaching the course
            professor = professors[email_id]
            professor_course_ids = professor["courses"]
    
            if course_id not in professor_course_ids:
                print("You do not have the right to delete a grade for this course.")
                return
            
            # Delete the grade
            del grades[(student_id, course_id)]
            # Save the grades to the CSV file
            with open("Grades.csv", "w") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow(["student_id", "course_id", "grades", "marks"])
                for key, grade in grades.items():
                    writer.writerow([grade.student_id, grade.course_id, grade.grades, grade.marks])
            print("Grade deleted successfully.")
        
        elif role == "admin":
            # Admin can delete a grade for any course
            del grades[(student_id, course_id)]
            # Save the grades to the CSV file
            with open("Grades.csv", "w") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow(["student_id", "course_id", "grades", "marks"])
                for key, grade in grades.items():
                    writer.writerow([grade.student_id, grade.course_id, grade.grades, grade.marks])
            print("Grade deleted successfully.")

        else:
            print("You do not have the right to delete a grade.")

    def modify_grade(self, role, email_id):
        # Modify a grade for a student in a course by a professor or admin
        student_id = input("Enter the student ID of the grade to be modified: ").strip()
        course_id = input("Enter the course ID of the grade to be modified: ").strip()
        if (student_id, course_id) not in grades:
            print("Grade not found.")
            return
        # Check if the user has the right to modify a grade
        if role == "professor":
            # Check if the professor is teaching the course
            professor = professors[email_id]
            professor_course_ids = professor["courses"]
    
            if course_id not in professor_course_ids:
                print("You do not have the right to modify a grade for this course.")
                return
            
            # Modify the grade
            grades = input("Enter the new grades (A, B, C, D, F): ").strip()
            marks = input("Enter the new marks (0-100): ").strip()
            # Check if the grades are valid
            if grades not in ["A", "B", "C", "D", "F"]:
                print("Invalid grades. Please enter A, B, C, D, or F.")
                return
            # Check if the marks are valid  
            if not marks.isdigit() or int(marks) < 0 or int(marks) > 100:
                print("Invalid marks. Please enter a number between 0 and 100.")
                return
            # Modify the grade
            grades[(student_id, course_id)] = Grades(student_id, course_id, grades, marks)
            # Save the grades to the CSV file
            with open("Grades.csv", "w") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow(["student_id", "course_id", "grades", "marks"])
                for key, grade in grades.items():
                    writer.writerow([grade.student_id, grade.course_id, grade.grades, grade.marks])
            print("Grade modified successfully.")
        
        elif role == "admin":
            # Admin can modify a grade for any course
            grades = input("Enter the new grades (A, B, C, D, F): ").strip()
            marks = input("Enter the new marks (0-100): ").strip()
            # Check if the grades are valid
            if grades not in ["A", "B", "C", "D", "F"]:
                print("Invalid grades. Please enter A, B, C, D, or F.")
                return
            # Check if the marks are valid  
            if not marks.isdigit() or int(marks) < 0 or int(marks) > 100:
                print("Invalid marks. Please enter a number between 0 and 100.")
                return
            # Modify the grade
            grades[(student_id, course_id)] = Grades(student_id, course_id, grades, marks)
            # Save the grades to the CSV file
            with open("Grades.csv", "w") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow(["student_id", "course_id", "grades", "marks"])
                for key, grade in grades.items():
                    writer.writerow([grade.student_id, grade.course_id, grade.grades, grade.marks])
            print("Grade modified successfully.")
        else:
            print("You do not have the right to modify a grade.")

    def grade_report_student(self, role, email_id):
        # Generate a grade report for a student by a professor, admin, or the student himself/herself
        if role == "admin":
            # Admin can generate a grade report for any student
            student_id = input("Enter the student ID: ").strip()
            if student_id not in students:
                print("Student not found.")
                return
            
        elif role == "professor":
            # Professor can generate a grade report for any student in his/her courses
            student_id = input("Enter the student ID: ").strip()
            if student_id not in students:
                print("Student not found.")
                return
            
            professor_course_ids = professors[email_id].courses
            professor_course_ids = [course_id for course_id in professor_course_ids]
            # Check if the student is enrolled in any of the professor's courses
            student_course_ids = students[student_id].courses
            student_course_ids = [course_id for course_id in student_course_ids if course_id in professor_course_ids]
            if not student_course_ids:
                print("Student is not enrolled in any of your courses.")
                return
            
        elif role == "student":
            # Student can only see their own grades
            student_id = email_id

        else:
            print("You do not have the right to generate a grade report.")
            return
        
        student = students[student_id]
        student_first_name = student.first_name
        student_last_name = student.last_name
        student_course_ids = student.courses

        print(f"\nGrade Report for {student_first_name} {student_last_name} (Student ID: {student_id})")
        
        # Display the student's courses and grades
        grade_list = []
        for course_id in student_course_ids:
            if (student_id, course_id) in grades:
                student_grade = grades[(student_id, course_id)].grades
                student_marks = grades[(student_id, course_id)].marks
                print(f"  Course ID: {course_id}, Grade: {student_grade}, Marks: {student_marks}")
                grade_list.append(float(student_marks))
            else:
                print(f"  Course ID: {course_id}, Grade: Not Available, Marks: Not Available")
        
        # Statistics
        if grade_list:
            print("\nStatistics:")
            print(f"  Total Courses Enrolled: {len(student_course_ids)}")
            print(f"  Average Grade: {statistics.mean(grade_list):.2f}")
            print(f"  Median Grade: {statistics.median(grade_list):.2f}")
            print(f"  Highest Grade: {max(grade_list)}")
            print(f"  Lowest Grade: {min(grade_list)}")
        else:
            print("No grades available for this student.")

    def grade_report_professor(self, role, email_id):
        # Generate a grade report for a professor by an admin or the professor himself/herself
        if role == "admin":
            # Admin can generate a grade report for any professor
            professor_id = input("Enter the professor ID: ").strip()
            if professor_id not in professors:
                print("Professor not found.")
                return
        
        elif role == "professor":
            # Professor can only see their own grades
            professor_id = email_id
        
        else:
            print("You do not have the right to generate a grade report.")
        
        professor_course_ids = professors[professor_id].courses
        professor_name = professors[professor_id].name
        print(f"\nGrade Report for {professor_name} (Professor ID: {professor_id})")

        # Display the professor's courses and grades
        for course_id in professor_course_ids:
            print(f"\n  Course ID: {course_id}")
            course_grades = [grade for key, grade in grades.items() if key[1] == course_id]
            if not course_grades:
                print("    No grades available for this course.")
                continue
            marks_list = [float(grade.marks) for grade in course_grades]

        # Statistics
            print("\nStatistics:")
            print(f"  Total students graded: {len(marks_list)}")
            print(f"  Average Grade: {statistics.mean(marks_list):.2f}")
            print(f"  Median Grade: {statistics.median(marks_list):.2f}")
            print(f"  Highest Grade: {max(marks_list)}")
            print(f"  Lowest Grade: {min(marks_list)}")
    
    def grade_report_course(self, role, email_id):
        # Generate a grade report for a course by an admin or the professor teaching the course
        if role == "admin":
            # Admin can generate a grade report for any course
            course_id = input("Enter the course ID: ").strip()
            if course_id not in courses:
                print("Course not found.")
                return
            
        elif role == "professor":
            # Professor can only see their own grades
            professor = professors[email_id]
            professor_course_ids = professor.courses
            course_id = input("Enter the course ID: ").strip()
            if course_id not in professor_course_ids:
                print("You do not have the right to generate a grade report for this course.")
                return
        
        else:
            print("You do not have the right to generate a grade report.")
            return
        
        course = courses[course_id]
        print(f"\nGrade Report for Course: {course.course_name} (Course ID: {course_id})")
        course_grades = [grade for key, grade in grades.items() if key[1] == course_id]
        if not course_grades:
            print("No grades available for this course.")
            return
        
        # Display the course's students and grades
        marks_list = []
        for grade in course_grades:
            student = students[grade.student_id]
            student_name = f"{student.first_name} {student.last_name}"
            print(f"  Student ID: {grade.student_id}, Name: {student_name}, Grade: {grade.grades}, Marks: {grade.marks}")
            marks_list.append(float(grade.marks))

        # Statistics
        print("\nStatistics:")
        print(f"  Total students graded: {len(marks_list)}")
        print(f"  Average Grade: {statistics.mean(marks_list):.2f}")
        print(f"  Median Grade: {statistics.median(marks_list):.2f}")
        print(f"  Highest Grade: {max(marks_list)}")
        print(f"  Lowest Grade: {min(marks_list)}")

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
