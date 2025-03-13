import csv
import time
import statistics
from student import students
from course import courses
from professor import professors

##### Initialize data #####
# Use a dictionary (hash table) to store all the grades, with (student_id, course_id) as the key
grades = {}

##### Class Grades #####
class Grades:

    def __init__(self, student_id=None, course_id=None, grade_input=None, marks_input=None):
        self.student_id = student_id # Unique student ID # Composite primary key (student_id, course_id)
        self.course_id = course_id # Unique course ID # Composite primary key (student_id, course_id)
        self.grade_input = grade_input # Grade input (A, B, C, D, F)
        self.marks_input = marks_input # Marks input (0-100)

    def display_all_grades_records(self, sort_by="name"):
        """
        Display all the grades details, sorted by a specific field.

        Parameters:
            sort_by (str): The field to sort the grades by.
                Options: "name", "grades", "marks". Default is "name".
        """
        if not grades:
            print("No grades records found.")
            return

        # Validate the sort_by field
        if sort_by not in ["student_id", "grades", "marks"]:
            print("Invalid field to sort by. Sorting by student_id by default.")
            sort_by = "student_id"

        # Convert the grades dictionary to a list of grades for sorting
        grades_list = list(grades.values())

        # Sort the grades by the specified field
        if sort_by == "student_id":
            # Sort by student ID
            grades_list.sort(key=lambda grade: grade.student_id)
        elif sort_by == "grades":
            # Sort by grades (e.g., A, B, C)
            grades_list.sort(key=lambda grade: grade.grade_input)
        elif sort_by == "marks":
            # Sort by marks (numerical value)
            grades_list.sort(key=lambda grade: grade.grade_input)

        # Display the sorted grades
        print(f"\nDisplaying all grades records (sorted by {sort_by}):")
        for grade in grades_list:
            print(f"Student ID: {grade.student_id}, Course ID: {grade.course_id}, Grades: {grade.grade_input}, Marks: {grade.marks_input}")
        
    def display_chosen_grade_records(self):
        """ Display the chosen grade's details and measure lookup time """
        student_id = input("Enter the student ID (or leave bland to see all students): ").strip()
        course_id = input("Enter the course ID (or leave blank to see all courses): ").strip()
        start_time = time.time() # Record the start time

        if student_id and course_id:
            # Case 1: Both student_id and course_id are provided
            if (student_id, course_id) in grades:
                grade = grades[(student_id, course_id)]
                print(f"Student ID: {grade.student_id}, Course ID: {grade.course_id}, Grades: {grade.grade_input}, Marks: {grade.marks_input}")
            else:
                print("Grade not found.")
        
        elif student_id:
            # Case 2: Only student_id is provided
            found = False
            for key, grade in grades.items():
                if key[0] == student_id:
                    print(f"Student ID: {grade.student_id}, Course ID: {grade.course_id}, Grades: {grade.grade_input}, Marks: {grade.marks_input}")
                    found = True
            if not found:
                print("No grades found for the student.")
        
        elif course_id:
            # Case 3: Only course_id is provided
            found = False
            for key, grade in grades.items():
                if key[1] == course_id:
                    print(f"Student ID: {grade.student_id}, Course ID: {grade.course_id}, Grades: {grade.grade_input}, Marks: {grade.marks_input}")
                    found = True
            if not found:
                print("No grades found for the course.")
        
        else:
            # Case 4: Both student_id and course_id are not provided
            print("Please provide at least a student ID or course ID to lookup a grade.")

        end_time = time.time() # Record the end time
        elapsed_time = end_time - start_time
        print(f"Time taken to lookup the grade: {elapsed_time:.6f} seconds")

    def display_professor_grades(self, email_id, sort_by="student_id"):
        """
        Display the grades for all courses taught by a professor, with optional sorting.

        Args:
            email_id (str): The email ID of the professor.
            sort_by (str): The sorting criteria. Options: "student_id", "grades", "marks". Default is "name".
        """
        if email_id not in professors:
            print(f"No professor found with email ID: {email_id}")
            return

        professor = professors[email_id]
        professor_course_ids = professor.courses
        print(f"\nDisplaying grades for Professor {professor.name} (Professor ID: {email_id})")

        for course_id in professor_course_ids:
            print(f"\nCourse ID: {course_id}")
            course_grades = [grade for key, grade in grades.items() if key[1] == course_id]

            if not course_grades:
                print("No grades available for this course.")
                continue

            # Sort grades based on the specified criteria
            if sort_by == "student_id":
                # Sort by student ID
                course_grades.sort(key=lambda grade: grade.student_id)
            elif sort_by == "grades":
                # Sort by grades (e.g., A, B, C)
                course_grades.sort(key=lambda grade: grade.grades)
            elif sort_by == "marks":
                # Sort by marks (numerical value)
                course_grades.sort(key=lambda grade: grade.marks)

            # Display sorted grades
            for grade in course_grades:
                if grade.student_id not in students:
                    print(f"  Student ID: {grade.student_id} not found in students database.")
                    continue

                student = students[grade.student_id]
                print(f"  Student ID: {grade.student_id}, Grades: {grade.grade_input}, Marks: {grade.marks_input}")

    def display_professor_chosen_grades(self, email_id, course_id, sort_by="student_id"):
        """
        Display grades for a chosen course taught by a professor, with optional statistics.

        Args:
            email_id (str): The email ID of the professor.
            course_id (str): The ID of the course to display grades for.
            sort_by (str): The field to sort the grades by. Options: "student_id", "grades", "marks". Default is "student_id".
        """
        if email_id not in professors:
            print(f"No professor found with email ID: {email_id}")
            return

        professor = professors[email_id]
        if course_id not in professor.courses:
            print(f"Course ID {course_id} is not taught by Professor {professor.name}.")
            return

        # Get all grades for the chosen course
        course_grades = [grade for key, grade in grades.items() if key[1] == course_id]

        if not course_grades:
            print(f"No grades available for Course ID: {course_id}.")
            return

        # Validate the sort_by field
        if sort_by not in ["student_id", "grades", "marks"]:
            print("Invalid field to sort by. Sorting by student_id by default.")
            sort_by = "student_id"

        # Sort the grades by the specified field
        if sort_by == "student_id":
            # Sort by student name
            course_grades.sort(key=lambda grade: grade.student_id)
        elif sort_by == "grades":
            # Sort by grades (e.g., A, B, C)
            course_grades.sort(key=lambda grade: grade.grades)
        elif sort_by == "marks":
            # Sort by marks (numerical value)
            course_grades.sort(key=lambda grade: grade.marks)

        # Display sorted grades
        print(f"\nDisplaying grades for Course ID: {course_id} (Taught by Professor {professor.name}, Sorted by {sort_by})")
        for grade in course_grades:
            if grade.student_id not in students:
                print(f"  Student ID: {grade.student_id} not found in students database.")
                continue

            student = students[grade.student_id]
            print(f"  Student ID: {grade.student_id}, Grades: {grade.grade_input}, Marks: {grade.marks_input}")

        # Ask the user if they want to see statistics
        while True:
            user_input = input("\nDo you want to see statistics? (yes/no): ").strip().lower()
            if user_input in ["yes", "no"]:
                break
            print("Invalid input. Please enter 'yes' or 'no'.")

        if user_input == "yes":
            # Calculate statistics
            marks_list = [grade.marks_input for grade in course_grades]
            average_mark = sum(marks_list) / len(marks_list)
            median_mark = sorted(marks_list)[len(marks_list) // 2] if len(marks_list) % 2 != 0 else (
                sorted(marks_list)[len(marks_list) // 2 - 1] + sorted(marks_list)[len(marks_list) // 2]) / 2
            highest_mark = max(marks_list)
            lowest_mark = min(marks_list)

            # Display statistics options
            print("\nChoose statistics to display:")
            print("1. Average Mark")
            print("2. Median Mark")
            print("3. Highest Mark")
            print("4. Lowest Mark")
            print("5. All of the above")

            while True:
                try:
                    choice = int(input("Enter your choice (1-5): "))
                    if 1 <= choice <= 5:
                        break
                    print("Invalid choice. Please enter a number between 1 and 5.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            # Display selected statistics
            if choice == 1:
                print(f"\nAverage Mark: {average_mark:.2f}")
            elif choice == 2:
                print(f"\nMedian Mark: {median_mark}")
            elif choice == 3:
                print(f"\nHighest Mark: {highest_mark}")
            elif choice == 4:
                print(f"\nLowest Mark: {lowest_mark}")
            elif choice == 5:
                print(f"\nAll Statistics:")
                print(f"1. Average Mark: {average_mark:.2f}")
                print(f"2. Median Mark: {median_mark}")
                print(f"3. Highest Mark: {highest_mark}")
                print(f"4. Lowest Mark: {lowest_mark}")
    
    def add_new_grade(self, role, email_id):
        # Add a grade for a student in a course by a professor or admin
        student_id = input("Enter the student ID: ").strip()
        course_id = input("Enter the course ID: ").strip()
        grade_input = input("Enter the grades (A, B, C, D, F): ").strip()
        marks_input = input("Enter the marks (0-100): ").strip()

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
        if grade_input not in ["A", "B", "C", "D", "F"]:
            print("Invalid grades. Please enter A, B, C, D, or F.")
            return
        
        # Check if the marks are valid
        if not marks_input.isdigit() or int(marks_input) < 0 or int(marks_input) > 100:
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
            grades[(student_id, course_id)] = Grades(student_id, course_id, grade_input, marks_input)
            # Save the grades to the CSV file
            with open("Grades.csv", "a") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow([student_id, course_id, grade_input, marks_input])
            print("Grade added successfully.")

        elif role == "admin":
            # Admin can add a grade for any course
            grades[(student_id, course_id)] = Grades(student_id, course_id, grade_input, marks_input)
            # Save the grades to the CSV file 
            with open("Grades.csv", "a") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow([student_id, course_id, grade_input, marks_input])
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
                writer.writerow(["Student_id", "Course_id", "Grades", "Marks"])
                for key, grade in grades.items():
                    writer.writerow([grade.student_id, grade.course_id, grade.grade_input, grade.marks_input])
            print("Grade deleted successfully.")
        
        elif role == "admin":
            # Admin can delete a grade for any course
            del grades[(student_id, course_id)]
            # Save the grades to the CSV file
            with open("Grades.csv", "w") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow(["Student_id", "Course_id", "Grades", "Marks"])
                for key, grade in grades.items():
                    writer.writerow([grade.student_id, grade.course_id, grade.grade_input, grade.marks_input])
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
            grade_input = input("Enter the new grades (A, B, C, D, F): ").strip()
            marks_input = input("Enter the new marks (0-100): ").strip()
            # Check if the grades are valid
            if grade_input not in ["A", "B", "C", "D", "F"]:
                print("Invalid grades. Please enter A, B, C, D, or F.")
                return
            # Check if the marks are valid  
            if not marks_input.isdigit() or int(marks_input) < 0 or int(marks_input) > 100:
                print("Invalid marks. Please enter a number between 0 and 100.")
                return
            # Modify the grade
            grades[(student_id, course_id)] = Grades(student_id, course_id, grade_input, marks_input)
            # Save the grades to the CSV file
            with open("Grades.csv", "w") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow(["Student_id", "Course_id", "Grades", "Marks"])
                for key, grade in grades.items():
                    writer.writerow([grade.student_id, grade.course_id, grade.grade_input, grade.marks_input])
            print("Grade modified successfully.")
        
        elif role == "admin":
            # Admin can modify a grade for any course
            grade_input = input("Enter the new grades (A, B, C, D, F): ").strip()
            marks_input = input("Enter the new marks (0-100): ").strip()
            # Check if the grades are valid
            if grade_input not in ["A", "B", "C", "D", "F"]:
                print("Invalid grades. Please enter A, B, C, D, or F.")
                return
            # Check if the marks are valid  
            if not marks_input.isdigit() or int(marks_input) < 0 or int(marks_input) > 100:
                print("Invalid marks. Please enter a number between 0 and 100.")
                return
            # Modify the grade
            grades[(student_id, course_id)] = Grades(student_id, course_id, grade_input, marks_input)
            # Save the grades to the CSV file
            with open("Grades.csv", "w") as grades_file:
                writer = csv.writer(grades_file)
                writer.writerow(["Student_id", "Course_id", "Grades", "Marks"])
                for key, grade in grades.items():
                    writer.writerow([grade.student_id, grade.course_id, grade.grade_input, grade.marks_input])
            print("Grade modified successfully.")
        else:
            print("You do not have the right to modify a grade.")

    def grade_report_student(self, role, email_id):
        """ Generate a grade report for a student by a professor, admin, or the student himself/herself """
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
                student_grade = grades[(student_id, course_id)].grade_input
                student_marks = grades[(student_id, course_id)].marks_input
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
        """ Generate a grade report for a professor by an admin or the professor himself/herself """
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
            marks_list = [float(grade.marks_input) for grade in course_grades]

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
            print(f"  Student ID: {grade.student_id}, Name: {student_name}, Grade: {grade.grade_input}, Marks: {grade.marks_input}")
            marks_list.append(float(grade.marks_input))

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
            student_id, course_id, grade_input, marks_input = row
            # Use (student_id, course_id) as the key
            grades[(student_id, course_id)] = Grades(student_id, course_id, grade_input, marks_input)

# Load grades data when the module is imported
load_grades_data()


